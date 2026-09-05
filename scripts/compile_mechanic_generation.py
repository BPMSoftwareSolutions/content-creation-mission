"""Compile the reviewed convergence package into a bounded Gemini job (no request)."""
import hashlib,json
from pathlib import Path
from mechanics_gate import validate_grounding
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'declarations/convergence.mechanic-grounded.json';raw=path.read_bytes();p=json.loads(raw)
job={'scenarioKey':p['key'],'mechanicsEvidence':{'path':str(path.relative_to(ROOT)).replace('\\','/'),
     'sha256':hashlib.sha256(raw).hexdigest()},'director':p['visualDirection'],
     'directorVersion':'mechanic-grounded.v1','model':'gemini-3-pro-image','format':'scenario-triptych'}
validate_grounding(job)
prompt='''Create three distinct cinematic shots, input/event/outcome, as three equal vertical panels in one landscape image. A consistent operator investigates a pending continuation in a believable control workspace. Foreground: uncertainty becomes focused investigation, then an understanding of the missing requirement. Background: show a real inspection interface comparing two required products to one supplied product; the second product remains absent. The event must visualize identity comparison, membership checking, and extraction of missing evidence, not a glowing transition. No external provider selection, restored service, completed join, extra product, or invocation. Preserve the same operator and input identities. Use distinct wide, close, and reverse camera blocking. Restrained warm editorial cinema with navy and amber, credible screens and natural human behavior. Human setting is editorial, not a literal runtime claim. The exact mechanics and animation direction are attached by the generation runner. This is a candidate storyboard for subsequent review, not proof.'''
job['id']=hashlib.sha256(raw+prompt.encode()).hexdigest()[:24]
job['request']={'contents':[{'role':'user','parts':[{'text':prompt}]}],
 'generationConfig':{'responseModalities':['TEXT','IMAGE'],'imageConfig':{'aspectRatio':'16:9','imageSize':'2K'}}}
out=ROOT/'samples/mechanics-workbench/generation-manifest.json';out.write_text(json.dumps([job],indent=2))
print('Compiled one mechanically grounded candidate request. No provider call made.')
