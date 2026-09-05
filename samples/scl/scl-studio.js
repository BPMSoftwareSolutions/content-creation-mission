'use strict';
(() => {
  const $=id=>document.getElementById(id), make=(tag,text)=>{const n=document.createElement(tag);n.textContent=text;return n;};
  let catalog, examples, mode='reveal', result=null, flow=null, busy=false, generation=0, online=false;
  const option=(value,label)=>{const n=make('option',label);n.value=value;return n;};
  async function api(path,body){const r=await fetch('/api/'+path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});const data=await r.json();if(!r.ok)throw Error(data.error);return data;}
  function fail(error){$('error').hidden=false;$('error').textContent=String(error.message||error);}
  function stop(){flow?.destroy();flow=null;$('play').disabled=true;$('position').disabled=true;}
  function show(data){
    stop();result=data;$('stage').innerHTML=data.svg;$('stage').classList.remove('native');$('material').disabled=false;$('error').hidden=true;$('error').textContent='';
    const g=data.graph,p=data.projection,r=data.receipt;
    $('basis').textContent=mode==='draft'?'TARGET / CANDIDATE DESIGN':'SOURCE / DECLARED';
    $('scope').textContent=`${r.visibleNodes} visible nodes / ${r.totalNodes} retained · ${r.retainedNativeRecords} native records`;
    $('status').textContent=`${g?.title||p.title} · Graph ${r.graphSha256.slice(0,12)} · No capability execution`;
    $('receipt').textContent=JSON.stringify(r,null,2);
    if(g){
      const native=g.records.filter(x=>x.kind==='cell');$('native-controls').hidden=mode!=='reveal'||!native.length;
      $('native-cell').replaceChildren(...native.map(x=>option(x.nativeId,`${x.nativeType} / ${x.nativeId}`)));
      $('scenario').replaceChildren(...g.scenarios.map(s=>option(s.id,s.label)));$('scenario').value=r.scenarioId;
      const records=g.records.filter(x=>!x.scenarioIds.length||x.scenarioIds.includes(r.scenarioId));
      $('records-summary').textContent=`${records.length} exact records in this scenario scope. Source declarations retain native port identities and control-flow kinds.`;
      $('record').replaceChildren(...records.map(x=>option(x.id,`${x.kind} / ${x.nativeType} / ${x.nativeId||x.id}`)));
      $('inspect-record').disabled=mode==='draft'||!records.length||!online;
      $('record-detail').textContent=records.length?'Select a record to inspect its exact source.':'No native records are attached to this draft. Its typed circuit is in the SCL editor.';
      $('findings').replaceChildren(...g.findings.map(f=>{const a=make('article','');a.append(make('b',f.code.replaceAll('_',' ')),make('p',f.detail),make('p','Closure: '+f.closure));return a;}));
      if(!g.findings.length)$('findings').append(make('p','Structurally valid candidate. Semantic review, provider qualification, proof and platform admission remain separate.'));
    }
    const chosen=p.animationBeats.flatMap(b=>b.edgeIds);
    $('flow-caption').textContent=chosen.length?'Illustrative trace / not execution testimony':'No trace selected. Source structure remains visible.';
    if(chosen.length){
      try{flow=new SideFXCircuitFlow.Player($('stage').firstElementChild,p,state=>{
        $('play').textContent=state.running?'Pause flow':matchMedia('(prefers-reduced-motion: reduce)').matches?'Step selected flow':'Play selected flow';
        $('position').max=state.duration;$('position').value=state.time;
        $('flow-caption').textContent=state.joins.length?state.joins.map(j=>`${j.arrived} / ${j.required} arrivals`).join(' · '):`${state.time.toFixed(1)} / ${state.duration.toFixed(1)}s · illustrative`;
      });$('play').disabled=false;$('position').disabled=false;}catch(e){$('flow-caption').textContent='Trace held: '+e.message;}
    }
  }
  async function load(resetScenario=false){
    if(!online)return;const request=++generation;busy=true;stop();$('status').textContent='Validating source identities and compiling the selected lens…';$('compile').disabled=true;
    try{const data=await api(mode==='draft'?'draft':'reveal',{...(mode==='draft'?{scl:$('editor').value}:{capabilityId:$('capability').value}),scenarioId:resetScenario?null:$('scenario').value,enhanced:$('material').checked});if(request===generation)show(data);}
    catch(e){if(request===generation){fail(e);$('status').textContent='Compilation held. The previous preview has been cleared.';$('stage').replaceChildren();result=null;}}
    finally{if(request===generation){busy=false;$('compile').disabled=false;}}
  }
  async function switchMode(next){mode=next;$('reveal-tab').setAttribute('aria-pressed',String(next==='reveal'));$('draft-tab').setAttribute('aria-pressed',String(next==='draft'));$('reveal-controls').hidden=next==='draft';$('draft-controls').hidden=next!=='draft';$('editor-panel').hidden=next!=='draft';document.querySelector('.work-layout').classList.toggle('editing',next==='draft');await load(true);}
  function download(name,content,type){if(!result)return;const url=URL.createObjectURL(new Blob([content],{type}));const a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
  $('download-scl').onclick=()=>result&&download('circuit.scl',result.scl||$('editor').value,'text/plain');
  $('download-json').onclick=()=>result?.graph&&download('circuit.json',JSON.stringify(result.graph,null,2),'application/json');
  $('download-svg').onclick=()=>result&&download('infographic.svg',result.svg,'image/svg+xml');
  $('reveal-tab').onclick=()=>switchMode('reveal');$('draft-tab').onclick=()=>switchMode('draft');
  $('capability').onchange=()=>load(true);$('scenario').onchange=()=>load();$('material').onchange=()=>load();$('compile').onclick=()=>load(true);
  $('example').onchange=()=>{$('editor').value=examples.find(e=>e.id===$('example').value).scl;load(true);};
  $('editor').oninput=()=>{stop();$('status').textContent='Draft changed. Compile to validate and refresh the projection.';result=null;};
  let searchTimer;
  $('search').oninput=()=>{clearTimeout(searchTimer);const previous=$('capability').value,q=$('search').value.toLowerCase();$('capability').replaceChildren(...catalog.results.filter(c=>(c.id+' '+c.title).toLowerCase().includes(q)).map(c=>option(c.id,c.title)));if([...$('capability').options].some(o=>o.value===previous))$('capability').value=previous;else if($('capability').options.length)searchTimer=setTimeout(()=>load(true),250);else{++generation;stop();result=null;$('stage').replaceChildren();$('status').textContent='No capabilities match that search.';$('native-controls').hidden=true;}};
  $('inspect-record').onclick=async()=>{try{const data=await api('record',{capabilityId:$('capability').value,recordId:$('record').value});$('record-detail').textContent=JSON.stringify(data,null,2);}catch(e){fail(e);}};
  function nativeZoom(){const svg=$('stage').querySelector('svg');if(svg&&$('stage').classList.contains('native'))svg.style.width=svg.viewBox.baseVal.width*Number($('native-zoom').value)+'px';}
  $('native-zoom').oninput=nativeZoom;
  $('native-view').onclick=async()=>{stop();const request=++generation;$('status').textContent='Opening the exact native cell neighborhood…';try{const data=await api('native',{capabilityId:$('capability').value,cellId:$('native-cell').value});if(request!==generation)return;$('stage').innerHTML=data.svg;$('stage').classList.add('native');nativeZoom();$('material').checked=false;$('material').disabled=true;$('receipt').textContent=JSON.stringify(data.receipt,null,2);$('scope').textContent=`${data.receipt.visibleCellIds.length} native cells visible / ${data.receipt.hiddenCellCount} outside this lens`;$('status').textContent='Native topology / exact ports / base vectors / scroll to inspect or adjust native zoom';$('flow-caption').textContent='Native control flow is inspection only. Its animation profile remains open.';if(result)result={...result,svg:data.svg,receipt:data.receipt};}catch(e){if(request===generation)fail(e);}};
  $('scenario-view').onclick=()=>load();
  $('play').onclick=()=>{if(flow?.running)flow.pause();else flow?.play();};$('position').oninput=()=>flow?.seek(Number($('position').value));
  document.addEventListener('visibilitychange',()=>{if(document.hidden)flow?.pause();});
  (async()=>{try{
    [catalog,examples]=await Promise.all(['catalog.json','examples.json'].map(p=>fetch(p).then(r=>r.json())));
    $('cap-count').textContent=catalog.capabilities;$('scenario-count').textContent=catalog.scenarios;$('cell-count').textContent=catalog.native.cells.toLocaleString();
    $('capability').replaceChildren(...catalog.results.map(c=>option(c.id,c.title)));$('capability').value='interlock-agent-operation';
    $('example').replaceChildren(...examples.map(e=>option(e.id,e.label)));$('editor').value=examples[0].scl;
    try{online=(await fetch('/api/health').then(r=>r.json())).compiler==='scl.v0.1';}catch(e){online=false;}
    $('connection').textContent=online?'Local compiler connected · no live effects':'Saved preview · start scripts/serve_scl.py for compilation';
    if(online)await load(true);else{mode='draft';const saved=await fetch('scenario-target.preview.json').then(r=>r.json());saved.graph=await fetch('../../declarations/scl/scenario-target.json').then(r=>r.json());saved.scl=examples[0].scl;show(saved);$('basis').textContent='TARGET / SAVED DRAFT';for(const id of ['reveal-tab','draft-tab','capability','scenario','material','compile','example'])$(id).disabled=true;$('editor').readOnly=true;$('status').textContent='Saved target preview. Run .venv\\Scripts\\python.exe scripts/serve_scl.py and open http://127.0.0.1:8766/samples/scl/index.html';}
  }catch(e){fail(e);}})();
})();
