const test=require('node:test');
const assert=require('node:assert/strict');
const Compiler=require('../templates/scl-live.js');

function harness(){
  let next=0;const callbacks=new Map(),requests=[],shown=[],errors=[];
  const timers={setTimeout:fn=>{callbacks.set(++next,fn);return next;},clearTimeout:id=>callbacks.delete(id)};
  const compiler=new Compiler({timers,execute:value=>new Promise((resolve,reject)=>requests.push({value,resolve,reject})),success:value=>shown.push(value),error:e=>errors.push(e.message)});
  return {compiler,requests,shown,errors,tick:()=>{const pending=[...callbacks.values()];callbacks.clear();pending.forEach(fn=>fn());}};
}
const settled=()=>new Promise(resolve=>setImmediate(resolve));

test('typing a burst submits only the final source after its debounce',async()=>{
  const h=harness();h.compiler.schedule('first',650);h.compiler.schedule('second',650);h.compiler.schedule('final',650);
  assert.equal(h.requests.length,0);h.tick();assert.deepEqual(h.requests.map(r=>r.value),['final']);
  h.requests[0].resolve('final SVG');await settled();assert.deepEqual(h.shown,['final SVG']);
});
test('slow renders cannot overwrite newer edits or create concurrent requests',async()=>{
  const h=harness();h.compiler.schedule('old');h.compiler.schedule('middle',650);h.tick();h.compiler.schedule('latest',650);h.tick();
  assert.deepEqual(h.requests.map(r=>r.value),['old']);
  h.requests[0].resolve('old SVG');await settled();assert.deepEqual(h.shown,[]);assert.deepEqual(h.requests.map(r=>r.value),['old','latest']);
  h.requests[1].resolve('latest SVG');await settled();assert.deepEqual(h.shown,['latest SVG']);
});
test('new input is allowed its full debounce even when the preceding render finishes',async()=>{
  const h=harness();h.compiler.schedule('old');h.compiler.schedule('typing',650);h.requests[0].resolve('old SVG');await settled();
  assert.equal(h.requests.length,1);assert.deepEqual(h.shown,[]);h.tick();assert.equal(h.requests[1].value,'typing');
  h.requests[1].resolve('new SVG');await settled();assert.deepEqual(h.shown,['new SVG']);
});
test('pausing live preview or switching views cancels pending and in-flight publication',async()=>{
  const h=harness();h.compiler.schedule('old');h.compiler.schedule('pending',650);h.compiler.invalidate();h.tick();
  h.requests[0].reject(Error('obsolete error'));await settled();assert.equal(h.requests.length,1);assert.deepEqual(h.errors,[]);assert.deepEqual(h.shown,[]);
  h.compiler.schedule('other view');h.requests[1].resolve('other SVG');await settled();assert.deepEqual(h.shown,['other SVG']);
});
test('syntax failure is reported once and a subsequent correction recovers',async()=>{
  const h=harness();h.compiler.schedule('invalid');h.requests[0].reject(Error('syntax error'));await settled();assert.deepEqual(h.errors,['syntax error']);
  h.compiler.schedule('fixed');h.requests[1].resolve('fixed SVG');await settled();assert.deepEqual(h.shown,['fixed SVG']);
});
test('Update now replaces a pending automatic compile without a duplicate request',async()=>{
  const h=harness();h.compiler.schedule('draft',650);h.compiler.schedule('draft');h.tick();assert.equal(h.requests.length,1);
  h.requests[0].resolve('SVG');await settled();assert.deepEqual(h.shown,['SVG']);
});
