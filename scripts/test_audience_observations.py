import tempfile,unittest
from pathlib import Path
from analyze_audience_observations import analyze
class AudienceEvidenceTests(unittest.TestCase):
    def test_empty_has_no_winner(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'data.csv';p.write_text('filmId,platform,videoId,variantId,windowStart,windowEnd,ctr\n')
            result=analyze(p);self.assertEqual(result['status'],'NO_AUDIENCE_EVIDENCE');self.assertIsNone(result['winner'])
    def test_missing_fraction_stays_unknown(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'data.csv';p.write_text('filmId,platform,videoId,variantId,windowStart,windowEnd,ctr\nf,y,v,A,start,end,\n')
            self.assertIsNone(analyze(p)['observations'][0]['measurements']['ctr'])
    def test_nan_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'data.csv';p.write_text('filmId,platform,videoId,variantId,windowStart,windowEnd,ctr\nf,y,v,A,start,end,NaN\n')
            with self.assertRaises(ValueError):analyze(p)
if __name__=='__main__':unittest.main()
