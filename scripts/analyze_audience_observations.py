"""Summarize supplied audience observations without inventing missing performance."""
import argparse,csv,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FRACTIONS=('ctr','viewedVsSwipedAway','firstSecondRetention','retention30Seconds','averagePercentViewed','subscriberConversion')
COUNTS=('impressions','views','shares','websiteClicks')
def analyze(path):
    rows=[]
    with path.open(encoding='utf-8-sig',newline='') as f:
        for r in csv.DictReader(f):
            if not any(r.values()):continue
            for key in ('filmId','platform','videoId','variantId','windowStart','windowEnd'):
                if not r.get(key):raise ValueError('Missing observation identity: '+key)
            values={}
            for key in FRACTIONS+COUNTS:
                raw=r.get(key,'').strip();value=None if raw=='' else float(raw)
                if value is not None and (not math.isfinite(value) or value<0 or (key in FRACTIONS and value>1)):
                    raise ValueError('Invalid metric: '+key)
                if value is not None and key in COUNTS and not value.is_integer():raise ValueError('Count must be integral: '+key)
                values[key]=value
            rows.append({**r,'measurements':values})
    return {'status':'NO_AUDIENCE_EVIDENCE' if not rows else 'DESCRIPTIVE_OBSERVATIONS_ONLY','observations':rows,
            'winner':None,'causalConclusion':None,'note':'No performance is inferred from missing data. No automatic creative winner is declared.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,default=ROOT/'samples/narration-continuity/audience-observations.csv');args=p.parse_args()
    result=analyze(args.input);out=ROOT/'evaluations/audience-observation-report.json';out.write_text(json.dumps(result,indent=2));print(result['status'])
