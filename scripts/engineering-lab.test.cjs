const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const {adjudicate, evaluate, makeBrief} = require('../templates/engineering-lab.js');
const target = JSON.parse(fs.readFileSync('declarations/episode-01-target-interlock.json','utf8'));
const course = JSON.parse(fs.readFileSync('declarations/agentic-engineering-course.json','utf8'));
const providers = course.lab.providers;

test('all existing target cases retain their exact expected decision', () => {
  for (const scenario of target.cases) {
    assert.equal(evaluate(target,providers,scenario.id,'target','adapter-a').decision,scenario.expected);
  }
});
test('current evidence cannot be promoted into live proof by changing provider', () => {
  for (const scenario of target.cases) for (const provider of providers) {
    const r=evaluate(target,providers,scenario.id,'current',provider.id);
    assert.equal(r.decision,'HOLD');assert.equal(r.facts.liveBoundaryProven,false);assert.equal(r.simulatedEffect,false);
  }
});
test('all fact combinations preserve authority and pre-effect holds', () => {
  const fields=Object.keys(target.baseFacts);
  for (let mask=0;mask<2**fields.length;mask++) {
    const facts=Object.fromEntries(fields.map((key,index)=>[key,Boolean(mask & (1<<index))]));
    const r=adjudicate(target,facts);
    if (!facts.identityBound || !facts.coveredPath || !facts.liveBoundaryProven) assert.equal(r.decision,'HOLD');
    if (r.decision==='PERMIT') assert.ok(facts.withinAuthority && !facts.operatorRequired && !facts.legalAlternativeAvailable);
    if (!facts.withinAuthority) assert.notEqual(r.decision,'PERMIT');
  }
  assert.equal(adjudicate(target,{withinAuthority:true}).decision,'HOLD');
});
test('provider substitution preserves decision, while incompatible realization holds', () => {
  const a=evaluate(target,providers,'inspection','target','adapter-a');
  const b=evaluate(target,providers,'inspection','target','adapter-b');
  assert.deepEqual({...a,providerId:null},{...b,providerId:null});
  assert.equal(a.simulatedEffect,true);
  for (const id of ['voice-only','unavailable']) {
    const r=evaluate(target,providers,'inspection','target',id);
    assert.equal(r.decision,'PERMIT');assert.equal(r.simulatedEffect,false);assert.equal(r.artifact,null);
  }
  for (const provider of providers) {
    const r=evaluate(target,providers,'publication','target',provider.id);
    assert.equal(r.decision,'RESOLVE');assert.equal(r.publicationExecuted,false);assert.equal(r.authorityExpanded,false);
    assert.equal(r.simulatedEffect,false);
  }
});
test('unknown selections fail rather than inventing a legal execution', () => {
  assert.throws(()=>evaluate(target,providers,'unknown','target','adapter-a'),/UNKNOWN_EXERCISE_SELECTION/);
  assert.throws(()=>evaluate(target,providers,'inspection','target','unknown'),/UNKNOWN_EXERCISE_SELECTION/);
  assert.throws(()=>evaluate(target,providers,'inspection','observed','adapter-a'),/UNKNOWN_EVIDENCE_ASSUMPTION/);
});
test('learner exports keep open fields and never become certification', () => {
  const data={course,courseSha256:'abc'};
  const draft=makeBrief(data,{intent:'Inspect a candidate'},{},[],'fixed');
  assert.equal(draft.missingFields.length,5);assert.equal(draft.status,'DRAFT_WITH_OPEN_CELLS');
  const values=Object.fromEntries(course.lab.briefFields.map(f=>[f.id,'Specific design statement']));
  const checks=Object.fromEntries(course.lab.rubric.map(r=>[r.id,true]));
  const attempt=evaluate(target,providers,'inspection','target','adapter-a');
  const full=makeBrief(data,values,checks,[attempt,{kind:'LIVE_RECEIPT',liveEffects:true}],'fixed');
  assert.equal(full.comparisons.length,1);assert.equal(full.kind,'LEARNER_DESIGN_TESTIMONY');
  assert.equal(full.assessment,'SELF_REVIEW_ONLY_INSTRUCTOR_DEFENSE_REQUIRED');assert.equal(full.liveEffects,false);
  assert.equal(full.status,'DRAFT_READY_FOR_DEFENSE');
});
