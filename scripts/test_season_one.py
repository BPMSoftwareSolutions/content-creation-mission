"""Check the episode's evidence boundary, target invariants, and delivered artifacts."""
import hashlib
import itertools
import json
import unittest
import wave
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from compile_content_products import validate_contracts
from mechanics_gate import resolve

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'samples/content-catalog/interlock-agent-operation'
def read(p):return json.loads((ROOT/p).read_bytes())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.ids=set()
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if 'id' in attrs:self.ids.add(attrs['id'])
        for name in ('src','href','poster'):
            if attrs.get(name):self.links.append(attrs[name])

class SeasonOne(unittest.TestCase):
    def test_season_and_reality_contract(self):
        season=read('declarations/season-1.json');direction=read('declarations/episode-01-direction.json')
        self.assertEqual([c['section'] for c in direction['chapters']],season['trainingStructure'])
        self.assertEqual(len(season['episodes']),10)
        self.assertEqual({c['reality'] for c in direction['chapters']},{'CURRENT','TARGET','GAP'})
        contracts=validate_contracts()
        interlock=next(c for c in contracts if c['capabilityId']=='interlock-agent-operation')
        self.assertIn('TARGET_DESIGN',{c['kind'] for c in interlock['claims']})
        self.assertEqual(len(interlock['permittedSurfaces']),9)

    def test_current_evidence_bytes_and_scope(self):
        gap=read('evaluations/episode-01-platform-gap.json')
        resolved=[resolve(item['sourceRef']) for item in gap['currentEvidence']]
        branch=json.dumps(resolved[0])
        self.assertIn('dangerous-tool',branch)
        self.assertIn('OPERATOR_REQUIRED',branch)
        self.assertIn('ALLOW',branch)
        self.assertNotIn('PERMIT',branch)
        self.assertEqual(len(gap['gaps']),6)
        self.assertIn('No live interception',gap['currentEvidenceLimit'])

    def test_all_target_combinations_fail_closed(self):
        target=read('declarations/episode-01-target-interlock.json')
        def decision(facts):return next((r['decision'] for r in target['rules'] if facts.get(r['field']) is r['equals']),'HOLD')
        for case in target['cases']:
            self.assertEqual(decision({**target['baseFacts'],**case['facts']}),case['expected'])
        for values in itertools.product((False,True),repeat=len(target['baseFacts'])):
            facts=dict(zip(target['baseFacts'],values));outcome=decision(facts)
            if not all(facts[k] for k in ('identityBound','coveredPath','liveBoundaryProven')):
                self.assertEqual(outcome,'HOLD')
            if outcome=='PERMIT':
                self.assertTrue(facts['withinAuthority'])
                self.assertFalse(facts['operatorRequired'])
                self.assertFalse(facts['legalAlternativeAvailable'])
            if not facts['withinAuthority']:
                self.assertNotEqual(outcome,'PERMIT')

    def test_audio_timeline_matches_authored_narration(self):
        direction=read('declarations/episode-01-direction.json');tl=read(OUT/'timeline.json')
        self.assertEqual(tl['directionDigest'],digest(ROOT/'declarations/episode-01-direction.json'))
        end=0
        for c,authored in zip(tl['chapters'],direction['chapters'],strict=True):
            self.assertAlmostEqual(c['start'],end,places=2)
            self.assertEqual(c['narration'],authored['narration'])
            self.assertEqual(c['audioDigest'],digest(OUT/c['audioFile']))
            receipt=read(OUT/c['audioFile'].replace('.wav','.receipt.json'))
            self.assertEqual(receipt['script'],c['narration'])
            with wave.open(str(OUT/c['audioFile'])) as audio:
                self.assertAlmostEqual(c['duration'],audio.getnframes()/audio.getframerate()+1,places=2)
            end=c['start']+c['duration']
        self.assertAlmostEqual(tl['durationSeconds'],end,places=2)

    def test_product_surfaces_are_hash_bound(self):
        manifest=read('outputs/capability-content-products.json')
        self.assertEqual(manifest['compiledSurfaceCount'],18)
        self.assertEqual(set(manifest['products']),{'generate-governed-narration','interlock-agent-operation'})
        for cid,product in manifest['products'].items():
            self.assertEqual(product['contractSha256'],digest(ROOT/f'declarations/capability-content/{cid}.json'))
            contract=read(f'declarations/capability-content/{cid}.json')
            self.assertEqual(set(product['surfaces']),set(contract['permittedSurfaces']))
            for asset in product['surfaces'].values():
                path=(ROOT/asset['path']).resolve();self.assertTrue(path.is_relative_to(ROOT))
                self.assertEqual(asset['sha256'],digest(path))
        for name,video in [('film.receipt.json','episode-01.mp4'),('short.receipt.json','short.mp4')]:
            receipt=read(OUT/name)
            self.assertFalse(receipt['liveEnforcementClaimed'])
            self.assertEqual(receipt['filmDigest'],digest(OUT/video))

    def test_all_local_navigation_targets_exist(self):
        pages=list(OUT.glob('*.html'))+[ROOT/'samples/season-1/index.html',ROOT/'samples/content-catalog/index.html',ROOT/'samples/content-catalog/editorial-ranking.html']
        for path in pages:
            parser=Links();parser.feed(path.read_text(encoding='utf-8'))
            for link in parser.links:
                url=urlsplit(link)
                if url.scheme or url.netloc:continue
                target=(path.parent/unquote(url.path)).resolve() if url.path else path
                self.assertTrue(target.is_file(),f'{path.name}: missing {link}')
                self.assertTrue(target.is_relative_to(ROOT))
                if url.fragment and target.suffix=='.html':
                    target_parser=Links();target_parser.feed(target.read_text(encoding='utf-8'))
                    self.assertIn(url.fragment,target_parser.ids)

if __name__=='__main__':unittest.main(verbosity=2)
