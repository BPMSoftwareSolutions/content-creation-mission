const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const {plan}=require('../templates/circuit-flow.js');
const sample=JSON.parse(fs.readFileSync(path.join(__dirname,'../samples/scl/certification.v02.preview.json'),'utf8'));

test('SCL 0.2 structured parallel projects concurrent departures and a real ALL wait',()=>{
  const p=sample.projection,lengths=Object.fromEntries(p.edges.map(e=>[e.id,e.target==='unmanaged-probe'?150:300]));
  const timeline=plan(p,lengths),branches=timeline.flights.filter(f=>f.source==='both-probes');
  assert.equal(branches.length,2);assert.equal(branches[0].start,branches[1].start);
  const arrivals=timeline.flights.filter(f=>f.target==='both-results').map(f=>f.end);
  assert.equal(timeline.nodes['both-results'].start,Math.max(...arrivals));
  const onward=timeline.flights.find(f=>f.source==='both-results');
  assert.ok(onward.start>Math.max(...arrivals));
});
test('proof and provider dependencies remain outside the illustrative execution trace',()=>{
  const p=sample.projection,timeline=plan(p,Object.fromEntries(p.edges.map(e=>[e.id,200])));
  const moving=new Set(timeline.selectedEdges);
  assert.ok(p.edges.filter(e=>['dependency','provider-binding','evidence-attachment'].includes(e.type)).every(e=>!moving.has(e.id)));
  assert.equal(sample.receipt.proofDisposition,'NOT_ESTABLISHED');
  assert.ok(sample.receipt.evidenceRequirements.every(r=>r.established===false));
  assert.equal(p.nodes.find(n=>n.id==='probe-testimony').basis,'GAP');
});
