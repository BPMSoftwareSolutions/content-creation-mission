/* Run with node --test scripts/circuit-flow.test.cjs. No browser or provider calls. */
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {plan, route} = require('../templates/circuit-flow.js');
const projection = id => JSON.parse(fs.readFileSync(path.join(__dirname, '../samples/infographic-grammar', id, 'projection.json')));
const lengths = p => Object.fromEntries(p.edges.map(e => [e.id, 260]));

test('ALL join cannot release before the slower arrival; fan-out releases both legs together', () => {
  const p = projection('scenario-target'), l = lengths(p);
  l.e03 = 26; l.e04 = 780;
  const result = plan(p, l), edge = id => result.flights.find(f => f.id === id);
  assert.equal(edge('e01').start, edge('e02').start);
  assert.ok(edge('e03').end < edge('e04').end);
  assert.equal(result.nodes.join.start, edge('e04').end);
  assert.ok(edge('e05').start > edge('e04').end);
  assert.equal(result.nodes.join.required, 2);
  assert.deepEqual(result.terminals, ['certified']);
});

test('speed determines elapsed distance; playback rate cannot change graph schedule', () => {
  const p = projection('scenario-target'), l = lengths(p), a = plan(p, l, 260), b = plan(p, l, 130);
  for (let i = 0; i < a.flights.length; i++) {
    assert.ok(Math.abs(a.flights[i].end - a.flights[i].start - 1) < 1e-10);
    assert.ok(Math.abs(b.flights[i].end - b.flights[i].start - 2) < 1e-10);
  }
  assert.deepEqual(a.selectedEdges, b.selectedEdges);
});

test('the authored decision follows ALLOW only, never both alternatives', () => {
  const p = projection('scenario-current'), result = plan(p, lengths(p));
  assert.ok(result.selectedEdges.includes('e03'));
  assert.ok(!result.selectedEdges.includes('e02'));
  assert.deepEqual(result.terminals, ['allow']);
  p.animationBeats[3].edgeIds.push('e02');
  assert.throws(() => plan(p, lengths(p)), /FLOW_BRANCH_NEEDS_ONE_ALTERNATIVE/);
});

test('provider and evidence connectors never become execution tracks', () => {
  const p = projection('scenario-target'), before = JSON.stringify(p), result = plan(p, lengths(p));
  assert.deepEqual(result.selectedEdges, ['e00', 'e01', 'e02', 'e03', 'e04', 'e05', 'e06']);
  assert.ok(!result.nodes.proof && !result.nodes.provider && !result.nodes.port);
  assert.equal(JSON.stringify(p), before);
  assert.equal(p.nodes.find(n => n.id === 'proof').basis, 'GAP');
});

test('incomplete fan-out and missing ALL input fail closed', () => {
  const p = projection('scenario-target');
  p.animationBeats.forEach(b => b.edgeIds = b.edgeIds.filter(id => id !== 'e02'));
  assert.throws(() => plan(p, lengths(p)), /FLOW_INCOMPLETE_FANOUT/);
  const q = projection('scenario-target');
  q.animationBeats.forEach(b => b.edgeIds = b.edgeIds.filter(id => id !== 'e04'));
  assert.throws(() => plan(q, lengths(q)), /FLOW_INCOMPLETE_JOIN/);
});

test('junction routing passes through exact hubs and preserves the edge curve', () => {
  const p = projection('scenario-target'), d = 'M547 484 C600 440 665 403 719.75 403';
  assert.equal(route(p, p.edges.find(e => e.id === 'e01'), d), 'M495 515 L547 484 C600 440 665 403 719.75 403');
  const intoJoin = route(p, p.edges.find(e => e.id === 'e03'), 'M1019 403 C1040 403 1060 474 1084.8 484');
  assert.ok(intoJoin.endsWith('L1164.8 516'));
  const outJoin = route(p, p.edges.find(e => e.id === 'e05'), 'M1224.8 516 C1240 516 1260 516 1280 516');
  assert.ok(outJoin.startsWith('M1164.8 516 L1224.8 516'));
});

test('capability overview keeps seven disconnected scenario paths independent', () => {
  const p = projection('capability-current'), result = plan(p, lengths(p));
  assert.equal(result.roots.length, 7); assert.equal(result.terminals.length, 7);
  for (const f of result.flights) assert.equal(f.source.slice(0, 2), f.target.slice(0, 2));
});

test('invalid speed, missing path length and attempted GAP execution are refused', () => {
  const p = projection('scenario-target');
  assert.throws(() => plan(p, lengths(p), 0), /INVALID_FLOW_SPEED/);
  assert.throws(() => plan(p, {}), /FLOW_INVALID_PATH_LENGTH/);
  p.nodes.find(n => n.id === 'check').basis = 'GAP';
  assert.throws(() => plan(p, lengths(p)), /FLOW_CANNOT_EXECUTE_GAP/);
});

test('ANY and quorum joins preserve their declared thresholds', () => {
  const p = projection('scenario-target'), l = lengths(p); l.e04 = 780;
  p.junctions.find(n => n.id === 'join').join = 'any';
  const any = plan(p, l); assert.equal(any.nodes.join.start, Math.min(...any.nodes.join.arrivals));
  const join = p.junctions.find(n => n.id === 'join'); join.join = 'quorum'; join.quorum = 2;
  const quorum = plan(p, l); assert.equal(quorum.nodes.join.start, Math.max(...quorum.nodes.join.arrivals));
});
