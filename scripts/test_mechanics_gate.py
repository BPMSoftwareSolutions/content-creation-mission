import copy,hashlib,json,unittest
from pathlib import Path
from mechanics_gate import validate_grounding,resolve
ROOT=Path(__file__).resolve().parents[1]
class MechanicsGateTests(unittest.TestCase):
    def setUp(self):
        self.path=ROOT/'declarations/convergence.mechanic-grounded.json'
        self.package=json.loads(self.path.read_text(encoding='utf-8'))
        self.job={'scenarioKey':self.package['key'],'mechanicsEvidence':{'path':str(self.path.relative_to(ROOT)),
                  'sha256':hashlib.sha256(self.path.read_bytes()).hexdigest()}}
    def test_feature_only_job_is_rejected(self):
        with self.assertRaisesRegex(ValueError,'MECHANICS_EVIDENCE_REQUIRED'):validate_grounding({'scenarioKey':'anything'})
    def test_stale_package_is_rejected(self):
        self.job['mechanicsEvidence']['sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'MECHANICS_PACKAGE_STALE'):validate_grounding(self.job)
    def test_wrong_scenario_is_rejected(self):
        self.job['scenarioKey']='wrong'
        with self.assertRaisesRegex(ValueError,'MECHANICS_SCENARIO_MISMATCH'):validate_grounding(self.job)
    def test_changed_entry_digest_is_rejected(self):
        ref=copy.deepcopy(self.package['animationBeats'][0]['sourceRefs'][0]);ref['entryDigest']='sha256:'+'0'*64
        with self.assertRaisesRegex(ValueError,'EVIDENCE_DIGEST_MISMATCH'):resolve(ref)
    def test_reviewed_package_resolves_all_beats(self):
        p=validate_grounding(self.job)
        self.assertEqual(len(p['animationBeats']),6)
        for beat in p['animationBeats']:
            for ref in beat['sourceRefs']:self.assertIsNotNone(resolve(ref))
if __name__=='__main__':unittest.main()
