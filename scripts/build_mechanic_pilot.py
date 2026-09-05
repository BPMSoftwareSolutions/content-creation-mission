"""Author one evidence-grounded convergence sequence and an inspectable workbench."""
import hashlib,json
from pathlib import Path
from mechanics_gate import resolve,validate_grounding
ROOT=Path(__file__).resolve().parents[1]
cid='resolve-governed-scenario-route';sid='resolve-convergence-readiness'
p=json.loads((ROOT/f'outputs/scenario-visual-evidence/{cid}/{sid}.json').read_text(encoding='utf-8'))
mechanic=next(x for x in p['evidence']['mechanics'] if x['value']['bindingId']=='port:'+sid+'-port')
fixture=next(x for x in p['evidence']['fixtures'] if x['value']['fixture']['fixtureId']=='holds-convergence-pending')
base=mechanic['source']; fixed=fixture['source']
p['selectedFixture']=fixture
def expression_ref(name): return {**base,'pointer':base['pointer']+'/configuration/expression/bindings/'+name}
steps=[
 ('Input','A decision is waiting','An operator has an approved outcome and a declared route to a convergence node. The route requires p1 and p2; the supplied state contains only p1.',
  'The request, declared requirements, and supplied snapshot enter three separate areas. Keep p2 visibly absent.',[fixed]),
 ('Event','Confirm this is a convergence request','The transformation checks that routes resolved and requiredProducts exists on the selected route.',
  'Reveal the selected route and its two required products. Do not animate an invocation moving down the route.',[expression_ref('routesResolved'),expression_ref('reachesConvergence')]),
 ('Event','Compare the governing identities','Readiness compares the admitted snapshot blueprintAuthorityDigest with the route authority digest. The snapshot is an intermediate product, not a freshly queried external system.',
  'Bring the two identity fields together for comparison while the supplied snapshot stays in place.',[expression_ref('identityBound')]),
 ('Event','Check every required product','The every/includes expression checks each required product against establishedConvergenceProducts.',
  'Align p1 with the supplied p1. Move the required p2 to the inspection position; its supplied-state position stays empty.',[expression_ref('productPresent'),fixed]),
 ('Event','Collect what is missing','The flat-map expression retains each required product absent from the snapshot. The fixture expects p2 to remain missing.',
  'Copy p2 into a missing-products report; never fill the empty supplied-state position.',[expression_ref('missingProducts'),fixed]),
 ('Outcome','The operator knows why it cannot advance','Readiness requires a declared convergence, matching identity, and every product present. The fixture expects CONVERGENCE_PENDING and an empty invocationSet.',
  'The missing-products report settles beside the unchanged source snapshot. The operator stops attempting to advance and can inspect the precise missing requirement.',[expression_ref('ready'),expression_ref('disposition'),fixed])]
p['animationBeats']=[{'ordinal':i,'phase':phase,'title':title,'mechanicalMeaning':meaning,'visibleChange':motion,'sourceRefs':refs}
 for i,(phase,title,meaning,motion,refs) in enumerate(steps)]
p['visualDirection']={
 'foreground':'An operator trying to understand why a declared continuation cannot advance; identity and environment are editorial choices.',
 'input':{'camera':'wide over-shoulder establishing view','action':'Operator compares a waiting request with its required products and supplied snapshot.'},
 'event':{'camera':'close view of an active evidence inspection','action':'Operator follows identity comparison, every-product membership checking, and missing-product extraction.'},
 'outcome':{'camera':'reverse medium view of operator and settled report','action':'Operator reads p2 missing and an empty invocation set; the unresolved work stays pending.'},
 'continuity':['Same operator, same request and immutable supplied snapshot','p1 is present and p2 absent in every phase'],
 'materialChange':'Unexplained waiting becomes an explicit pending decision with p2 identified as missing.',
 'mechanicalOverlays':['Readiness predicate','Required versus established product membership','Missing-products report','Empty invocation set'],
 'providerReality':'Declared local sda-authority-transformation-port.v1 plus sda-schema-contract-admission.v1 at boundaries; no external service selection or fallback.',
 'simulationReality':'Selected fixture supplies input and expected assertions; it declares no substituted provider response. This sequence is an explanation, not a recorded execution.'}
p['groundingReview']={'gherkinOnlyInsufficient':True,'reviewer':'Codex inspection of exact plan expression and fixture bytes',
 'specificMechanicalFacts':['every/includes product membership','flat-map missing-product extraction','two required products p1/p2 and only p1 supplied','fixture invocationSet is empty'],
 'limitations':['No fixture was executed in this lab','Visual audience review remains separate','Root capability fixture supplies the example; this is not an isolated-node execution receipt']}
p['disposition']='MECHANICS_DIRECTION_REVIEWED'
target=ROOT/'declarations/convergence.mechanic-grounded.json'
target.write_text(json.dumps(p,indent=2),encoding='utf-8')
binding={'path':str(target.relative_to(ROOT)).replace('\\','/'),'sha256':hashlib.sha256(target.read_bytes()).hexdigest()}
validate_grounding({'scenarioKey':p['key'],'mechanicsEvidence':binding})
data={'package':p,'binding':binding,'fixture':fixture['value']['fixture'],
      'resolvedSources':{ref['entryDigest']+ref['pointer']:resolve(ref) for beat in p['animationBeats'] for ref in beat['sourceRefs']},
      'index':json.loads((ROOT/'outputs/scenario-visual-evidence-index.json').read_text(encoding='utf-8'))}
template=(ROOT/'scripts/mechanics_workbench.template.html').read_text(encoding='utf-8')
out=ROOT/'samples/mechanics-workbench';out.mkdir(parents=True,exist_ok=True)
(out/'index.html').write_text(template.replace('__DATA__',json.dumps(data).replace('</','<\\/')),encoding='utf-8')
print('Reviewed convergence direction, six source-linked beats, evidence workbench built. No runtime execution claimed.')
