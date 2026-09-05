import copy,hashlib,unittest
from visual_review import DIMENSIONS,validate_review

class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.job={'scenarioKey':'example::one','directorVersion':'visual-experience-director.v2'}
        self.review={**self.job,'imageDigest':hashlib.sha256(b'image').hexdigest(),
                     'dimensions':{d:{'passes':True,'observation':'A concrete reviewer observation.'} for d in DIMENSIONS},
                     'findings':[],'disposition':'VISUAL_EXPERIENCE_CONFORMS'}
    def test_exact_image_binding(self):
        self.assertTrue(validate_review(self.review,self.job,b'image'))
        with self.assertRaisesRegex(ValueError,'STALE_IMAGE'): validate_review(self.review,self.job,b'changed')
    def test_failed_phase_cannot_conform(self):
        self.review['dimensions']['phaseDistinction']['passes']=False
        with self.assertRaisesRegex(ValueError,'CONTRADICTS'): validate_review(self.review,self.job,b'image')
    def test_open_finding_cannot_conform(self):
        self.review['findings']=['VISUAL_PHASE_COLLAPSE']
        with self.assertRaisesRegex(ValueError,'CONTRADICTS'): validate_review(self.review,self.job,b'image')
    def test_failed_visual_is_not_accepted(self):
        self.review['dimensions']['labelIndependence']['passes']=False
        self.review['findings']=['VISUAL_PHASE_COLLAPSE']
        self.review['disposition']='VISUAL_EXPERIENCE_DOES_NOT_CONFORM'
        self.assertFalse(validate_review(self.review,self.job,b'image'))

if __name__=='__main__': unittest.main()
