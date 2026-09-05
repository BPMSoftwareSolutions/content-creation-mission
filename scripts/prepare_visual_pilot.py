"""Prepare one deliberately art-directed eight-scenario visual proof."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
collection = json.loads((ROOT / 'declarations/governed-routing.visual-experiences.v1.json').read_text())
directions = [
 ('What may happen next?', 'Three distinct objects: a small admitted outcome card, an indigo route blueprint, and a transparent frozen state tablet. Keep all three in the same positions across all panels.', 'A precise inspection beam aligns the same three documents; the route map is highlighted but nothing travels along it.', 'FOUR objects must be visible: the original admitted outcome card, the original indigo route blueprint, the original transparent frozen-state tablet, PLUS a new small teal authorization certificate BELOW them. Never replace or hide the frozen-state tablet. Label the fourth object AUTHORIZED, not executed.'),
 ('Find the declared variant', 'An outcome card labeled B sits before three declared slots A, B and C. These labels are illustrative.', 'A fine inspection line compares card B with the declared B slot; the other slots remain distinct.', 'Only B is outlined in teal, labeled VARIANT RESOLVED. No provider runs and no downstream operation starts.'),
 ('Resolve the declared routes', 'A selected variant B is attached to its own indigo route map, with one declared outgoing connection.', 'A lens traces the printed connection within that supplied document, without moving an execution token.', 'A teal outline identifies the single declared route, labeled ROUTE RESOLVED. It is still a static map.'),
 ('Use the supplied snapshot', 'A request envelope contains a transparent state tablet with three rows: PRODUCTS, MEMBERS, ITERATIONS, and an indigo identity badge.', 'A glass frame encloses that exact same tablet; its identity badge aligns with the supplied blueprint badge.', 'The same tablet is framed and labeled IMMUTABLE SNAPSHOT. All rows remain unchanged; no counters advance.'),
 ('All fan-out members count', 'An indigo authority card declares A, B, C. Beside it is a tray with exactly TWO solid ceramic blocks: A and B. The third C position is ONLY an empty printed outline, with no solid block, no blank block and no object in it.', 'Preserve the exact TWO blocks A and B and the EMPTY printed C outline. A thin comparison line connects declared C to the empty outline. No third block exists anywhere.', 'Keep the same TWO blocks A and B clearly visible in their original tray, and keep the C outline EMPTY. Add a SMALL coral MISSING MEMBER plaque BELOW the tray as a fourth separate document; NEVER replace the tray or remove A and B. No member executes.'),
 ('A missing product means pending', 'An indigo convergence diagram requires products A, B and C. The frozen snapshot contains only A and B.', 'A lens compares the existing A and B products with their required slots; C is visibly missing and never arrives.', 'The join stays stationary with an empty C slot and a prominent amber PENDING plaque. Never show a completed join or success.'),
 ('A return needs authority', 'A printed loop arrow sits beside a declared bound card and an unchanged observation card labeled BOUND EXHAUSTED.', 'A comparison lens checks the observation against the bound without incrementing any counter.', 'The loop remains untraveled and a coral evidence card reads RETURN REJECTED. No retry occurs.'),
 ('Carry the decision and its evidence', 'Three evidence cards for membership, readiness and return authority share one indigo identity strip. Readiness explicitly says PENDING.', 'The evidence is assembled into a single continuation record with visible source-route and identity fields.', 'One amber continuation card reads CONVERGENCE PENDING and retains the lineage strip. No downstream invocation starts.')
]
jobs = []
for index, (spec, direction) in enumerate(zip(collection['experiences'], directions)):
    title, before, event, outcome = direction
    prompt = f'''Create a premium editorial architectural storyboard, 16:9 canvas, three exactly equal full-height columns. The panel boundaries must be at one-third and two-thirds of the width. Each column is its own view of the SAME miniature architectural exhibit from the SAME orthographic elevated camera angle. No shared objects crossing panel boundaries.
Art direction: warm ivory background, deep ink typography, tactile off-white ceramic blocks, translucent glass evidence tablets, precise indigo printed authority, fine graphite lines, restrained teal authorization / amber pending / coral rejection. Soft studio lighting and quiet museum-exhibit quality, generous negative space, elegant contemporary information design. NOT a futuristic server room. No people, robots, neon or decorative circuitry. Make the changing relationship unmistakable through matching objects and framing.
Top of each column: small typeset INPUT, EVENT, OUTCOME respectively. No other header or footer. Short labels only, no paragraphs. Large readable objects. Each panel has the same tabletop, camera and objects; change only the stated comparison and outcome indicators.
INPUT: {before}
EVENT: {event}
OUTCOME: {outcome}
All A/B/C labels and three-item counts are illustrative. The source scenario is {spec['scenarioId']}. Preserve this meaning: {json.dumps(spec['outcomeExperience']['observableState'])}
Render the one concrete example described above, not all possible alternatives. The lens is an editorial metaphor for evaluation. The capability resolves authorization and NEVER executes scenarios, mutates route state or performs downstream effects. An empty slot must remain empty if described. Avoid check marks on pending or rejected outcomes. Maintain visual continuity with any provided style reference, but do not copy its scenario content.'''
    payload = {'contents': [{'role':'user','parts':[{'text':prompt}]}], 'generationConfig': {'responseModalities':['TEXT','IMAGE'], 'imageConfig':{'aspectRatio':'16:9','imageSize':'2K'}}}
    jobs.append({'id':hashlib.sha256(prompt.encode()).hexdigest()[:24], 'scenarioKey':'resolve-governed-scenario-route::'+spec['scenarioId'],
                 'title':title,'index':index,'model':'gemini-3-pro-image','format':'scenario-triptych','request':payload,
                 'phases':[before,event,outcome], 'source':collection['source'], 'spec':spec})
path = ROOT / 'samples/visual-pilot'
path.mkdir(parents=True,exist_ok=True)
(path/'generation-manifest.json').write_text(json.dumps(jobs,indent=2),encoding='utf-8')
print('Prepared',len(jobs),'art-directed scenario triptychs')
