"""Build the screening room, captions, entity sheet, and audience measurement template."""
import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'samples/narration-continuity'
demo=json.loads((OUT/'demo.receipt.json').read_bytes())
voice=json.loads((OUT/'film-voiceover.receipt.json').read_bytes())
profile=json.loads((OUT/'audience-profile.json').read_bytes())
entities=[
 {'entity':'Producer','input':'Holding the marked script; interrupted, tense','event':'Leans forward, watches options checked and work resume','outcome':'Puts on headphones, listens, returns to editing','continuity':'Same person, charcoal jacket, bun, studio'},
 {'entity':'Narration script','input':'Human creative intent, still waiting','event':'The exact local script digest survives provider selection','outcome':'Its words are audible in a real WAV','continuity':'Original text unchanged'},
 {'entity':'Provider A','input':'Unavailable in this injected failure','event':'Kept outside the active path','outcome':'Remains disconnected','continuity':'Simulated failure throughout'},
 {'entity':'Provider B','input':'Possible alternative','event':'Rejected: declared text-only capability','outcome':'Never invoked','continuity':'Local demonstration candidate'},
 {'entity':'Provider C','input':'Compatible audio alternative','event':'Gemini synthesizes the original narration','outcome':'Live-generated speech file exists','continuity':'Actual named model recorded in receipt'},
 {'entity':'Provider D','input':'Standby alternative','event':'Not selected','outcome':'Not invoked','continuity':'No fabricated test or service call'},
 {'entity':'Audio and evidence','input':'No new narration asset','event':'Bytes materialize; file is hashed; provider and request retained','outcome':'Playable narration plus a local receipt','continuity':'Waveform comes from the actual generated audio'},
 {'entity':'Queue','input':'Seven illustrative local jobs','event':'One narration job handled','outcome':'Six remain','continuity':'Never claims the entire queue drained'}]
(OUT/'entity-sheet.json').write_text(json.dumps(entities,indent=2))
metrics=['filmId','platform','videoId','variantId','publishedAt','windowStart','windowEnd','impressions','views','ctr','viewedVsSwipedAway','firstSecondRetention','retention30Seconds','averagePercentViewed','shares','subscriberConversion','websiteClicks','notes']
if not (OUT/'audience-observations.csv').exists():
    with (OUT/'audience-observations.csv').open('w',newline='',encoding='utf-8') as f:csv.writer(f).writerow(metrics)
def stamp(v):
    ms=round(v*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}.{ms%1000:03}'
sentences=[s.strip()+'.' for s in voice['script'].split('.') if s.strip()]
total=sum(len(s.split()) for s in sentences);elapsed=0;lines=['WEBVTT','']
for s in sentences:
    duration=len(s.split())/total*voice['durationSeconds'];lines += [f'{stamp(elapsed)} --> {stamp(elapsed+duration)}',s,''];elapsed+=duration
lines += [f'00:00:54.000 --> {stamp(54+demo["asset"]["durationSeconds"])}',demo['asset']['script'],'']
(OUT/'captions.vtt').write_text('\n'.join(lines),encoding='utf-8')
payload=json.dumps({'demo':demo,'profile':profile,'entities':entities}).replace('</','<\\/')
html=(ROOT/'scripts/continuity_screening.template.html').read_text(encoding='utf-8').replace('__DATA__',payload)
(OUT/'index.html').write_text(html,encoding='utf-8')
print('Screening room, entity sheet, approximate captions and empty audience-observation template ready.')
