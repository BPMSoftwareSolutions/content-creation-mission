const {readFileSync,readdirSync}=require('node:fs');
const vm=require('node:vm');
const assert=require('node:assert/strict');
const test=require('node:test');
const context={module:{exports:{}}};
vm.runInNewContext(readFileSync('templates/estate-topology/viewer.js','utf8'),context);
const {planTrace}=context.module.exports;
function covers(graph,steps){
 assert.equal(new Set(steps.filter(s=>s.edgeId).map(s=>s.edgeId)).size,graph.edges.length);
 assert.equal(steps.filter(s=>s.edgeId).length,graph.edges.length);
 const nodes=new Set(steps.flatMap(s=>s.nodeId?[s.nodeId]:[s.source,s.target]));
 assert.equal(nodes.size,graph.nodes.length);
}
test('trace crosses every fan-out member before continuing beyond convergence',()=>{
 const graph={nodes:['a','b','c','d','end'].map(id=>({id,kind:id==='d'?'convergence':'event'})),edges:[['ab','a','b','FAN_OUT_MEMBER'],['ac','a','c','FAN_OUT_MEMBER'],['bd','b','d','CONVERGENCE_REQUIREMENT'],['cd','c','d','CONVERGENCE_REQUIREMENT'],['de','d','end','TRANSITION']].map(([id,source,target,kind])=>({id,source,target,kind}))};
 const steps=planTrace(graph);covers(graph,steps);const ids=steps.map(s=>s.edgeId);
 assert.ok(ids.indexOf('de')>ids.indexOf('bd')&&ids.indexOf('de')>ids.indexOf('cd'));
});
test('cycles, disconnected routes, references and isolated nodes all finish exactly once',()=>{
 const graph={nodes:['a','b','c','d','provider','alone'].map(id=>({id,kind:'event'})),edges:[['ab','a','b','sequence'],['ba','b','a','recurrence'],['cd','c','d','sequence'],['pa','provider','a','provider-binding']].map(([id,source,target,kind])=>({id,source,target,kind}))};
 covers(graph,planTrace(graph,'b'));
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
