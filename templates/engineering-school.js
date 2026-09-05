(function () {
  'use strict';
  const data = window.ENGINEERING_COURSE;
  const $ = id => document.getElementById(id);
  const text = (id, value) => { $(id).textContent = value; };
  const attempts = [];

  function concept(id) {
    const c = data.course.concepts.find(c => c.id === id);
    document.querySelectorAll('[data-concept]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.concept === id)));
    text('concept-number', `${String(data.course.concepts.indexOf(c)+1).padStart(2,'0')} / ${c.title}`);
    for (const field of ['question','meaning','example','failure']) text('concept-'+field, c[field]);
  }
  document.querySelectorAll('[data-concept]').forEach(b => b.addEventListener('click', () => concept(b.dataset.concept)));
  concept(data.course.concepts[0].id);

  const film = $('lesson-film');
  document.querySelectorAll('[data-film-time]').forEach(b => b.addEventListener('click', () => {
    film.currentTime = Number(b.dataset.filmTime); film.scrollIntoView({block: 'center'});
    film.play().catch(() => { /* Native play controls remain available. */ });
  }));

  let player;
  try {
    const svg = $('circuit-stage').querySelector('svg');
    svg.setAttribute('role', 'group');
    svg.setAttribute('viewBox', '30 270 2159.2 790');
    svg.setAttribute('width', '2159.2'); svg.setAttribute('height', '790');
    const stamp = time => `0:${String(Math.floor(time)).padStart(2,'0')}`;
    player = new window.SideFXCircuitFlow.Player(svg, data.projection, state => {
      $('flow-position').max = state.duration; $('flow-position').value = state.time;
      text('flow-time', stamp(state.time)+' / '+stamp(state.duration));
      text('flow-play', state.running ? 'Pause the circuit' : state.finished ? 'Replay the circuit' : 'Play the circuit');
      const waiting = state.joins.find(j => j.arrived < j.required);
      text('flow-status', waiting ? `${waiting.arrived} / ${waiting.required} results arrived. The ALL join waits.`
        : state.finished ? 'Target flow complete. Required testimony is still GAP; live certification remains unproven.'
        : 'Illustrative motion. No live execution or completed certification is claimed.');
    });
    ['flow-play','flow-restart','flow-position'].forEach(id => { $(id).disabled = false; });
    $('flow-play').onclick = () => {
      if (player.running) player.pause();
      else { document.querySelector('.circuit-theater').scrollIntoView({block:'start'}); player.play(); }
    };
    $('flow-restart').onclick = () => player.seek(0);
    $('flow-position').oninput = event => player.seek(Number(event.target.value));
    // Node activation is a local inspection, never an action request.
    svg.querySelectorAll('[data-entity]').forEach(node => {
      node.setAttribute('tabindex', '0'); node.setAttribute('role', 'button');
      const inspect = () => { player.pause(); text('flow-status', node.getAttribute('aria-label') || node.querySelector('title')?.textContent || 'Inspect the complete source circuit using the link above.'); };
      node.addEventListener('click', inspect);
      node.addEventListener('keydown', e => { if (['Enter',' '].includes(e.key)) { e.preventDefault(); inspect(); } });
    });
    document.addEventListener('visibilitychange', () => { if (document.hidden) player.pause(); });
    window.addEventListener('pagehide', () => player.pause());
  } catch (error) {
    text('flow-status', 'The source circuit is available for inspection. Motion could not start: '+error.message);
  }

  function invalidate() {
    $('lab-after').hidden = true; $('lab-before').hidden = false;
    const provider = data.course.lab.providers.find(p => p.id === $('lab-provider').value);
    text('provider-explanation', provider.explanation);
  }
  ['lab-case','lab-evidence','lab-provider'].forEach(id => $(id).addEventListener('change', invalidate));
  invalidate();
  $('lab-controls').addEventListener('submit', event => {
    event.preventDefault();
    const prediction = new FormData(event.currentTarget).get('prediction');
    if (!prediction) return;
    const result = window.SideFXEngineeringLab.evaluate(data.target, data.course.lab.providers,
      $('lab-case').value, $('lab-evidence').value, $('lab-provider').value);
    const attempt = {...result, prediction, predictionCorrect: prediction === result.decision};
    attempts.push(attempt); if (attempts.length > 100) attempts.shift();
    $('lab-before').hidden = true; $('lab-after').hidden = false;
    text('prediction-feedback', attempt.predictionCorrect ? 'YOUR PREDICTION MATCHES THE RULE' : `YOU CHOSE ${prediction} / REVISIT THE BOUNDARY`);
    text('decision-result', result.decision);
    text('decision-reason', result.reason.replaceAll('_',' ').toLowerCase());
    text('authority-result', result.decision + ' / ' + (result.evidenceMode === 'current' ? 'live proof is not supplied by the current snapshot' : 'under the stated target assumptions'));
    const provider = data.course.lab.providers.find(p => p.id === result.providerId);
    text('provider-result', provider.label+' / '+result.providerReadiness.replaceAll('_',' ').toLowerCase());
    text('effect-result', result.simulatedEffect ? 'An illustrative inspection report can be represented. No live artifact was produced.'
      : result.decision !== 'PERMIT' ? 'No effect. Resolve the authority decision before considering execution.'
      : 'No effect. The request is permitted in the exercise, but this provider cannot realize it.');
    text('next-action', result.decision === 'PERMIT' && !result.simulatedEffect ? 'Next: resolve a compatible, available provider without changing the request or authority.' : result.next);
    const labels = {identityBound:'Exact identities', coveredPath:'Tool-path coverage', liveBoundaryProven:'Live-boundary proof',operatorRequired:'Separate operator required',legalAlternativeAvailable:'Legal alternative',withinAuthority:'Within authority'};
    $('assumed-facts').replaceChildren(...Object.entries(result.facts).map(([key,value]) => {
      const row=document.createElement('div'),term=document.createElement('dt'),detail=document.createElement('dd');
      term.textContent=labels[key];detail.textContent=value?'ASSUMED YES':'NO';row.append(term,detail);return row;
    }));
    text('attempt-testimony', JSON.stringify(attempt,null,2));
    text('attempt-count', `${attempts.length} comparison${attempts.length===1?'':'s'} recorded for your design brief. These are illustrative exercise results.`);
    $('lab-after').scrollIntoView({block:'start'});
  });

  const values = () => Object.fromEntries(data.course.lab.briefFields.map(f => [f.id, $('brief-'+f.id).value]));
  const checks = () => Object.fromEntries(data.course.lab.rubric.map(r => [r.id, document.querySelector(`#brief-form input[name="${r.id}"]`).checked]));
  const brief = () => window.SideFXEngineeringLab.makeBrief(data, values(), checks(), attempts);
  const storageKey = 'sidefx-engineering-brief.v1.'+data.courseSha256;
  $('save-draft').onclick = () => {
    try { localStorage.setItem(storageKey,JSON.stringify(brief())); text('brief-status','Draft saved in this browser for this exact course edition.'); }
    catch { text('brief-status','Browser storage is unavailable. Export the brief to keep your work.'); }
  };
  $('load-draft').onclick = () => {
    try {
      const saved = JSON.parse(localStorage.getItem(storageKey) || 'null');
      if (!saved) { text('brief-status','No saved draft exists for this course edition.'); return; }
      if (saved.courseSha256 !== data.courseSha256 || saved.kind !== 'LEARNER_DESIGN_TESTIMONY') throw new Error('Stale draft');
      data.course.lab.briefFields.forEach(f => { $('brief-'+f.id).value = typeof saved.fields?.[f.id] === 'string' ? saved.fields[f.id].slice(0,8000) : ''; });
      data.course.lab.rubric.forEach(r => { document.querySelector(`#brief-form input[name="${r.id}"]`).checked = saved.selfReview?.[r.id] === true; });
      // Saved comparisons are untrusted learner records; recompute each selection
      // against the pinned exercise instead of restoring supplied decisions.
      attempts.length=0;
      for (const item of (Array.isArray(saved.comparisons)?saved.comparisons:[]).slice(-100)) {
        try { const result=window.SideFXEngineeringLab.evaluate(data.target,data.course.lab.providers,item.caseId,item.evidenceMode,item.providerId);
          if (['HOLD','PERMIT','DENY','RESOLVE','OPERATOR_REQUIRED'].includes(item.prediction)) attempts.push({...result,prediction:item.prediction,predictionCorrect:item.prediction===result.decision});
        } catch { /* Skip records outside the current exercise contract. */ }
      }
      invalidate();text('attempt-count',`${attempts.length} comparison${attempts.length===1?'':'s'} restored and recalculated for this course edition.`);
      text('brief-status','Saved draft restored. Review its claims before exporting.');
    } catch { text('brief-status','The saved draft could not be read for this course edition. Your current entries are intact.'); }
  };
  $('export-brief').onclick = () => {
    const report=brief();const url=URL.createObjectURL(new Blob([JSON.stringify(report,null,2)+'\n'],{type:'application/json'}));
    const a=document.createElement('a');a.href=url;a.download='sidefx-authority-boundary-brief.json';document.body.append(a);a.click();a.remove();
    setTimeout(()=>URL.revokeObjectURL(url),1000);
    text('brief-status',report.missingFields.length ? `Draft exported with ${report.missingFields.length} open fields. No completion or certification is claimed.` : 'Design brief exported for instructor defense. Your self-review is included; live capability certification is not claimed.');
  };
})();
