'use strict';
(() => {
  const $=id=>document.getElementById(id), make=(tag,text)=>{const n=document.createElement(tag);n.textContent=text;return n;};
  let catalog, examples, mode='draft', result=null, flow=null, generation=0, online=false, previousDraft=null;
  const draftKey='sidefx.scl.playground.v1';
  const option=(value,label)=>{const n=make('option',label);n.value=value;return n;};
  async function api(path,body){const r=await fetch('/api/'+path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});const data=await r.json();if(!r.ok)throw Error(data.error);return data;}
  function fail(error){$('error').hidden=false;$('error').textContent=String(error.message||error);}
  function stop(){flow?.destroy();flow=null;$('play').disabled=true;$('position').disabled=true;}
  function clearPreview(){
    stop();result=null;$('stage').replaceChildren();$('scope').textContent='';$('receipt').textContent='';
    $('findings').replaceChildren();$('record').replaceChildren();$('records-summary').textContent='';$('record-detail').textContent='';
    $('inspect-record').disabled=true;$('native-controls').hidden=true;$('download-json').disabled=true;$('download-svg').disabled=true;
    $('flow-caption').textContent='Waiting for a valid circuit.';$('error').hidden=true;$('error').textContent='';
  }
  function state(label,kind='pending'){$('compile-state').textContent=label;$('compile-state').dataset.state=kind;}
  function saveDraft(){
    try{localStorage.setItem(draftKey,JSON.stringify({text:$('editor').value,example:$('example').value,previous:previousDraft}));$('save-state').textContent='Draft saved in this browser';}
    catch(e){$('save-state').textContent='Browser storage unavailable. Use Save SCL to keep your draft.';}
  }
  const compiler=new SCLLiveCompiler({
    execute:task=>api(task.path,task.body),
    start:()=>{state('Compiling…');$('status').textContent='Validating the circuit and updating its infographic…';},
    success:data=>{show(data);state('Preview up to date','valid');},
    error:e=>{clearPreview();fail(e);state('Check your SCL','error');$('status').textContent='Fix the error below. Your text is preserved; the preview returns when the circuit is valid.';}
  });
  function show(data){
    stop();result=data;$('stage').innerHTML=data.svg;$('stage').classList.remove('native');$('material').disabled=false;$('error').hidden=true;$('error').textContent='';
    $('download-json').disabled=!data.graph;$('download-svg').disabled=false;
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
  function load(resetScenario=false,delay=0){
    if(!online)return;++generation;
    const body={...(mode==='draft'?{scl:$('editor').value}:{capabilityId:$('capability').value}),scenarioId:resetScenario?null:$('scenario').value,enhanced:$('material').checked};
    clearPreview();state(delay?'Waiting for your next edit…':'Queued…');
    $('status').textContent=delay?'Live preview updates after you pause typing.':'Preparing the latest circuit…';
    compiler.schedule({path:mode==='draft'?'draft':'reveal',body},delay);
  }
  function switchMode(next){mode=next;$('reveal-tab').setAttribute('aria-pressed',String(next==='reveal'));$('draft-tab').setAttribute('aria-pressed',String(next==='draft'));$('reveal-controls').hidden=next==='draft';$('draft-controls').hidden=next!=='draft';$('editor-panel').hidden=next!=='draft';document.querySelector('.work-layout').classList.toggle('editing',next==='draft');$('basis').textContent=next==='draft'?'TARGET / CANDIDATE DESIGN':'SOURCE / DECLARED';history.replaceState(null,'',next==='draft'?'#playground':'#workbench');load(true);}
  function download(name,content,type){const url=URL.createObjectURL(new Blob([content],{type}));const a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
  $('download-scl').onclick=()=>{if(mode==='draft')download('my-circuit.scl',$('editor').value,'text/plain');else if(result)download('circuit.scl',result.scl,'text/plain');};
  $('download-json').onclick=()=>result?.graph&&download('circuit.json',JSON.stringify(result.graph,null,2),'application/json');
  $('download-svg').onclick=()=>result&&download('infographic.svg',result.svg,'image/svg+xml');
  $('reveal-tab').onclick=()=>switchMode('reveal');$('draft-tab').onclick=()=>switchMode('draft');
  $('capability').onchange=()=>load(true);$('scenario').onchange=()=>load();$('material').onchange=()=>load();$('compile').onclick=()=>load(true);
  function replaceDraft(text,example=''){
    previousDraft=$('editor').value;$('restore-draft').disabled=false;$('editor').value=text;$('example').value=example;
    saveDraft();load(true);
  }
  $('example').onchange=()=>{const example=examples.find(e=>e.id===$('example').value);if(example)replaceDraft(example.scl,example.id);};
  $('new-draft').onclick=()=>{replaceDraft(examples[0].scl,examples[0].id);$('editor').focus();};
  $('restore-draft').onclick=()=>{if(previousDraft!==null)replaceDraft(previousDraft);};
  $('import-scl').onclick=()=>$('scl-file').click();
  $('scl-file').onchange=async()=>{const file=$('scl-file').files[0];if(!file)return;try{if(file.size>2_000_000)throw Error('Choose an SCL draft smaller than 2 MB.');replaceDraft(await file.text());}catch(e){fail(e);}finally{$('scl-file').value='';}};
  $('editor').oninput=()=>{
    $('example').value='';saveDraft();++generation;compiler.invalidate();clearPreview();
    if($('live').checked)load(true,650);else{state('Uncompiled edits');$('status').textContent='Live preview is paused. Use Update now or Ctrl+Enter to compile.';}
  };
  $('editor').onkeydown=e=>{if(e.key==='Enter'&&(e.ctrlKey||e.metaKey)){e.preventDefault();load(true);}};
  $('live').onchange=()=>{if($('live').checked)load(true);else{++generation;compiler.invalidate();state('Live preview paused');$('status').textContent='Use Update now or Ctrl+Enter whenever you want to compile.';}};
  let searchTimer;
  $('search').oninput=()=>{clearTimeout(searchTimer);const previous=$('capability').value,q=$('search').value.toLowerCase();$('capability').replaceChildren(...catalog.results.filter(c=>(c.id+' '+c.title).toLowerCase().includes(q)).map(c=>option(c.id,c.title)));if([...$('capability').options].some(o=>o.value===previous))$('capability').value=previous;else{++generation;compiler.invalidate();clearPreview();if($('capability').options.length)searchTimer=setTimeout(()=>{if(mode==='reveal')load(true);},250);else $('status').textContent='No capabilities match that search.';}};
  $('inspect-record').onclick=async()=>{const request=generation;try{const data=await api('record',{capabilityId:$('capability').value,recordId:$('record').value});if(request===generation)$('record-detail').textContent=JSON.stringify(data,null,2);}catch(e){if(request===generation)fail(e);}};
  function nativeZoom(){const svg=$('stage').querySelector('svg');if(svg&&$('stage').classList.contains('native'))svg.style.width=svg.viewBox.baseVal.width*Number($('native-zoom').value)+'px';}
  $('native-zoom').oninput=nativeZoom;
  $('native-view').onclick=async()=>{stop();compiler.invalidate();const request=++generation;$('status').textContent='Opening the exact native cell neighborhood…';try{const data=await api('native',{capabilityId:$('capability').value,cellId:$('native-cell').value});if(request!==generation)return;$('stage').innerHTML=data.svg;$('stage').classList.add('native');nativeZoom();$('material').checked=false;$('material').disabled=true;$('receipt').textContent=JSON.stringify(data.receipt,null,2);$('scope').textContent=`${data.receipt.visibleCellIds.length} native cells visible / ${data.receipt.hiddenCellCount} outside this lens`;$('status').textContent='Native topology / exact ports / base vectors / scroll to inspect or adjust native zoom';$('flow-caption').textContent='Native control flow is inspection only. Its animation profile remains open.';if(result)result={...result,svg:data.svg,receipt:data.receipt};}catch(e){if(request===generation)fail(e);}};
  $('scenario-view').onclick=()=>load();
  $('play').onclick=()=>{if(flow?.running)flow.pause();else flow?.play();};$('position').oninput=()=>flow?.seek(Number($('position').value));
  document.addEventListener('visibilitychange',()=>{if(document.hidden)flow?.pause();});
  (async()=>{try{
    [catalog,examples]=await Promise.all(['catalog.json','examples.json'].map(p=>fetch(p).then(r=>r.json())));
    $('cap-count').textContent=catalog.capabilities;$('scenario-count').textContent=catalog.scenarios;$('cell-count').textContent=catalog.native.cells.toLocaleString();
    $('capability').replaceChildren(...catalog.results.map(c=>option(c.id,c.title)));$('capability').value='interlock-agent-operation';
    $('example').replaceChildren(option('','Your edited draft'),...examples.map(e=>option(e.id,e.label)));$('example').value=examples[0].id;$('editor').value=examples[0].scl;
    try{const saved=JSON.parse(localStorage.getItem(draftKey));if(saved&&typeof saved.text==='string'){$('editor').value=saved.text;$('example').value=saved.example||'';previousDraft=typeof saved.previous==='string'?saved.previous:null;$('restore-draft').disabled=previousDraft===null;$('save-state').textContent='Your saved draft has been restored';}}catch(e){$('save-state').textContent='Browser storage unavailable. Use Save SCL to keep your draft.';}
    try{online=(await fetch('/api/health').then(r=>r.json())).compiler==='scl.v0.1';}catch(e){online=false;}
    $('connection').textContent=online?'Local compiler connected · no live effects':'Saved preview · start scripts/serve_scl.py for compilation';
    switchMode(location.hash==='#workbench'?'reveal':'draft');
    if(online){if(location.hash==='#playground')$('workbench').scrollIntoView();}
    else{const saved=await fetch('scenario-target.preview.json').then(r=>r.json());saved.graph=await fetch('../../declarations/scl/scenario-target.json').then(r=>r.json());saved.scl=examples.find(e=>e.id==='scenario-target').scl;show(saved);$('basis').textContent='TARGET / SAVED EXAMPLE';state('Compiler offline','error');for(const id of ['reveal-tab','draft-tab','capability','scenario','material','compile','example','new-draft','import-scl','restore-draft','live'])$(id).disabled=true;$('editor').readOnly=true;$('status').textContent='Saved target example (not a preview of editor text). Run .venv\\Scripts\\python.exe scripts/serve_scl.py and open http://127.0.0.1:8766/samples/scl/index.html';}
  }catch(e){fail(e);}})();
})();
