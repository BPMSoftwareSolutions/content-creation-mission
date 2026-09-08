const {readFileSync,readdirSync}=require('node:fs');
const vm=require('node:vm');
const assert=require('node:assert/strict');
const test=require('node:test');
const context={module:{exports:{}}};
vm.runInNewContext(readFileSync('templates/estate-topology/viewer.js','utf8'),context);
const {planTrace}=context.module.exports;
function covers(graph,waves){
 const steps=waves.flat();
 assert.equal(new Set(steps.filter(s=>s.edgeId).map(s=>s.edgeId)).size,graph.edges.length);
 assert.equal(steps.filter(s=>s.edgeId).length,graph.edges.length);
 const nodes=new Set(steps.flatMap(s=>s.nodeId?[s.nodeId]:[s.source,s.target]));
 assert.equal(nodes.size,graph.nodes.length);
}
test('trace crosses every fan-out member before continuing beyond convergence',()=>{
 const graph={nodes:['a','b','c','d','end'].map(id=>({id,kind:id==='d'?'convergence':'event'})),edges:[['ab','a','b','FAN_OUT_MEMBER'],['ac','a','c','FAN_OUT_MEMBER'],['bd','b','d','CONVERGENCE_REQUIREMENT'],['cd','c','d','CONVERGENCE_REQUIREMENT'],['de','d','end','TRANSITION']].map(([id,source,target,kind])=>({id,source,target,kind}))};
 const steps=planTrace(graph);covers(graph,steps);const ids=steps.flat().map(s=>s.edgeId);
 assert.deepEqual(Array.from(steps[0],s=>s.edgeId),['ab','ac']);
 assert.deepEqual(Array.from(steps[1],s=>s.edgeId),['bd','cd']);
 assert.ok(ids.indexOf('de')>ids.indexOf('bd')&&ids.indexOf('de')>ids.indexOf('cd'));
});
test('unequal fan-out paths stay parallel and convergence waits for the longer branch',()=>{
 const graph={nodes:['start','short','long','middle','join','end'].map(id=>({id,kind:id==='join'?'convergence':'event'})),edges:[['s','start','short','FAN_OUT_MEMBER'],['l','start','long','FAN_OUT_MEMBER'],['sj','short','join','CONVERGENCE_REQUIREMENT'],['lm','long','middle','TRANSITION'],['mj','middle','join','CONVERGENCE_REQUIREMENT'],['je','join','end','TRANSITION']].map(([id,source,target,kind])=>({id,source,target,kind}))};
 const waves=planTrace(graph);covers(graph,waves);
 assert.deepEqual(Array.from(waves[1],e=>e.edgeId),['sj','lm']);
 const waveOf=id=>waves.findIndex(w=>w.some(e=>e.edgeId===id));assert.ok(waveOf('je')>waveOf('mj'));
});
test('operation continuation and scenario-call traces fork in the same visual step',()=>{
 const graph={nodes:['operation','scenario-input','next-operation'].map(id=>({id,kind:'event'})),edges:[{id:'call',source:'operation',target:'scenario-input',kind:'scenario-call'},{id:'next',source:'operation',target:'next-operation',kind:'operation-order'}]};
 const waves=planTrace(graph,'operation');covers(graph,waves);
 assert.equal(waves[0].length,2);assert.deepEqual(Array.from(waves[0],e=>e.edgeId),['call','next']);
});
test('independent mechanic operands flow together and their result waits for both',()=>{
 const graph={kind:'expression',nodes:['a','b','result','end'].map(id=>({id,kind:'event'})),edges:[['a','a','result'],['b','b','result'],['end','result','end']].map(([id,source,target])=>({id,source,target,kind:'argument-dependency'}))};
 const waves=planTrace(graph);covers(graph,waves);assert.equal(waves[0].length,2);assert.equal(waves[1][0].edgeId,'end');
});
test('cycles, disconnected routes, references and isolated nodes all finish exactly once',()=>{
 const graph={nodes:['a','b','c','d','provider','alone'].map(id=>({id,kind:'event'})),edges:[['ab','a','b','sequence'],['ba','b','a','recurrence'],['cd','c','d','sequence'],['pa','provider','a','provider-binding']].map(([id,source,target,kind])=>({id,source,target,kind}))};
 covers(graph,planTrace(graph,'b'));
});

test('a provider binding arrives alongside the input and completes before the port continues',()=>{
 const graph={nodes:['input','port','provider','end'].map(id=>({id,kind:id==='port'?'provider-port':'event'})),edges:[['enter','input','port','operation-order'],['bind','provider','port','provider-binding'],['leave','port','end','operation-order']].map(([id,source,target,kind])=>({id,source,target,kind}))};
 const waves=planTrace(graph);covers(graph,waves);
 assert.deepEqual(Array.from(waves[0],e=>e.edgeId),['enter','bind']);
 assert.deepEqual(Array.from(waves[1],e=>e.edgeId),['leave']);
});

test('each port uses its own bindings on arrival even when ports share a provider',()=>{
 const graph={nodes:['input','first','second','provider','other','end'].map(id=>({id,kind:'event'})),edges:[['enter','input','first','operation-order'],['next','first','second','operation-order'],['leave','second','end','operation-order'],['bind-first','provider','first','provider-binding'],['bind-second','provider','second','provider-binding'],['bind-other','other','second','provider-binding']].map(([id,source,target,kind])=>({id,source,target,kind}))};
 const waves=planTrace(graph);covers(graph,waves);
 assert.deepEqual(Array.from(waves[0],e=>e.edgeId),['enter','bind-first']);
 assert.deepEqual(Array.from(waves[1],e=>e.edgeId),['next','bind-second','bind-other']);
 assert.deepEqual(Array.from(waves[2],e=>e.edgeId),['leave']);
});

test('parallel ports receive their bindings in the same fork wave',()=>{
 const graph={nodes:['start','left','right','provider','join','end'].map(id=>({id,kind:id==='join'?'convergence':'event'})),edges:[['left','start','left','FAN_OUT_MEMBER'],['right','start','right','FAN_OUT_MEMBER'],['bind-left','provider','left','provider-binding'],['bind-right','provider','right','provider-binding'],['left-join','left','join','CONVERGENCE_REQUIREMENT'],['right-join','right','join','CONVERGENCE_REQUIREMENT'],['end','join','end','TRANSITION']].map(([id,source,target,kind])=>({id,source,target,kind}))};
 const waves=planTrace(graph);covers(graph,waves);
 assert.deepEqual(Array.from(waves[0],e=>e.edgeId),['left','right','bind-left','bind-right']);
 assert.deepEqual(Array.from(waves[1],e=>e.edgeId),['left-join','right-join']);
 assert.equal(waves[2][0].edgeId,'end');
});

test('starting at a bound port traces its binding before downstream flow',()=>{
 const graph={nodes:['port','provider','end'].map(id=>({id,kind:'event'})),edges:[['leave','port','end','operation-order'],['bind','provider','port','provider-binding']].map(([id,source,target,kind])=>({id,source,target,kind}))};
 for(const selected of [undefined,'port']){
  const waves=planTrace(graph,selected);covers(graph,waves);
  assert.deepEqual(Array.from(waves[0],e=>e.edgeId),['bind']);
  assert.deepEqual(Array.from(waves[1],e=>e.edgeId),['leave']);
 }
 const onlyBinding={nodes:graph.nodes.filter(n=>n.id!=='end'),edges:graph.edges.filter(e=>e.kind==='provider-binding')};
 const waves=planTrace(onlyBinding);covers(onlyBinding,waves);assert.equal(waves.length,1);
});
test('every compiled estate diagram has a finite trace covering its entire topology',()=>{
 const index=JSON.parse(readFileSync('outputs/estate-topology/index.json','utf8'));let count=0;
 for(const file of Object.keys(index.files)){
  if(!file.startsWith('outputs/estate-topology/')||!file.endsWith('.js'))continue;
  const text=readFileSync(file,'utf8'),prefix='window.ESTATE_TOPOLOGY_VIEW=';if(!text.startsWith(prefix))continue;
  const graph=JSON.parse(text.slice(prefix.length,-1));covers(graph,planTrace(graph));count++;
 }
 assert.ok(count>1500);
});
