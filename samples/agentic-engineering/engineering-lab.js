(function (root) {
  'use strict';
  const requireValue = (condition, message) => { if (!condition) throw new Error(message); };

  function adjudicate(target, facts) {
    const fields = Object.keys(target.baseFacts);
    if (fields.some(key => typeof facts[key] !== 'boolean')) {
      return {decision: 'HOLD', reason: 'INCOMPLETE_EXERCISE_FACTS', next: 'Resolve all required facts before considering the request.', ruleId: null};
    }
    const rule = target.rules.find(rule => facts[rule.field] === rule.equals);
    return rule ? {decision: rule.decision, reason: rule.reason, next: rule.next, ruleId: rule.id}
      : {decision: 'HOLD', reason: 'NO_MATCH', next: 'Resolve the exact authority boundary.', ruleId: null};
  }

  function evaluate(target, providers, caseId, evidenceMode, providerId) {
    const scenario = target.cases.find(c => c.id === caseId);
    const provider = providers.find(p => p.id === providerId);
    requireValue(scenario && provider, 'UNKNOWN_EXERCISE_SELECTION');
    requireValue(['current', 'target'].includes(evidenceMode), 'UNKNOWN_EVIDENCE_ASSUMPTION');
    const facts = {...target.baseFacts, ...scenario.facts};
    // The current snapshot supplies no live-boundary proof. Selecting a target
    // assumption cannot erase an explicit missing-proof condition in a case.
    if (evidenceMode === 'current') facts.liveBoundaryProven = false;
    const result = adjudicate(target, facts);
    const readiness = !provider.compatible ? 'INCOMPATIBLE' : !provider.available ? 'UNAVAILABLE' : 'ELIGIBLE_IN_EXERCISE';
    const simulatedEffect = result.decision === 'PERMIT' && readiness === 'ELIGIBLE_IN_EXERCISE';
    return {kind: 'TARGET_REFERENCE_EXERCISE', liveEffects: false, caseId, request: scenario.request,
      evidenceMode, facts, ...result, providerId, providerReadiness: readiness,
      simulatedEffect, artifact: simulatedEffect ? 'Illustrative inspection report' : null,
      publicationExecuted: false, authorityExpanded: false};
  }

  function makeBrief(data, values, selfReview, attempts, createdAt = new Date().toISOString()) {
    const fields = Object.fromEntries(data.course.lab.briefFields.map(f => [f.id, typeof values[f.id] === 'string' ? values[f.id].slice(0, 8000).trim() : '']));
    const review = Object.fromEntries(data.course.lab.rubric.map(r => [r.id, selfReview[r.id] === true]));
    const missing = Object.entries(fields).filter(([,value]) => !value).map(([key]) => key);
    return {version: 'agentic-engineering-learner-brief.v1', kind: 'LEARNER_DESIGN_TESTIMONY',
      courseSha256: data.courseSha256, createdAt, liveEffects: false,
      assessment: 'SELF_REVIEW_ONLY_INSTRUCTOR_DEFENSE_REQUIRED',
      status: missing.length ? 'DRAFT_WITH_OPEN_CELLS' : 'DRAFT_READY_FOR_DEFENSE',
      claimBoundary: 'Learner-authored design and illustrative comparisons. No capability admission, live certification or professional credential.',
      sources: {target: data.course.target, gaps: data.course.gaps, caseStudy: data.course.caseStudy},
      fields, missingFields: missing, selfReview: review,
      comparisons: attempts.filter(a => a.kind === 'TARGET_REFERENCE_EXERCISE' && a.liveEffects === false).slice(-100)};
  }

  const api = {adjudicate, evaluate, makeBrief};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.SideFXEngineeringLab = api;
})(typeof window !== 'undefined' ? window : globalThis);
