"""Prepare the reviewed Episode 1 upload kit and explicit public page assets."""
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / 'releases/episode-01'
PUBLIC = ROOT / 'release-site/public'
MEDIA = ROOT / 'samples/content-catalog/interlock-agent-operation'
TITLE = 'AI Agents Can Act. Who Gives Them Authority? | SideFX Episode 1'
SITE = 'https://sidefx-agentic-engineering.sjonesbpm.chatgpt.site'
CHANNEL = 'https://www.youtube.com/@SideFX-b4'


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    KIT.mkdir(parents=True, exist_ok=True)
    (PUBLIC / 'media').mkdir(parents=True, exist_ok=True)
    review = read('evaluations/episode-01-infographic-review.json')
    assert digest(MEDIA / 'episode-01.mp4') == review['film']['sha256'], 'Film differs from reviewed edition'
    contract = read('declarations/capability-content/interlock-agent-operation.json')
    for evidence in contract['evidence']:
        assert digest(ROOT / evidence['path']) == evidence['sha256'], f'Stale evidence: {evidence["id"]}'
    timeline = read('samples/content-catalog/interlock-agent-operation/timeline.json')
    gaps = read('evaluations/episode-01-platform-gap.json')
    chapters = []
    for chapter in timeline['chapters']:
        second = round(chapter['start'])
        chapters.append({'id': chapter['id'], 'title': chapter['title'], 'seconds': second,
                         'timestamp': f'{second // 60:02d}:{second % 60:02d}',
                         'narration': chapter['narration']})
    assert chapters[0]['seconds'] == 0
    assert all(b['seconds'] - a['seconds'] >= 10 for a, b in zip(chapters, chapters[1:]))
    media_files = {}
    for filename in ['episode-01.mp4', 'thumbnail.jpg', 'captions.vtt']:
        src = MEDIA / filename
        shutil.copy2(src, KIT / filename)
        shutil.copy2(src, PUBLIC / 'media' / filename)
        media_files[filename] = {'sha256': digest(src), 'bytes': src.stat().st_size,
                                'source': src.relative_to(ROOT).as_posix()}
    vtt = (MEDIA / 'captions.vtt').read_text(encoding='utf-8')
    cues = [part.strip() for part in vtt.split('\n\n') if '-->' in part]
    srt = '\n\n'.join(f'{i}\n' + cue.replace('.', ',', 2) for i, cue in enumerate(cues, 1)) + '\n'
    (KIT / 'captions.srt').write_text(srt, encoding='utf-8')
    description = f'''An AI agent has the tools to publish. Its assignment authorizes inspection. What should happen before the command runs?

Episode 1 of The Future of Agentic Engineering explores the difference between capability, authority, and evidence of enforcement.

Watch the film, read the transcript, and inspect the evidence guide:
{SITE}

In this fictional engineering scenario, we separate what the reviewed SideFX snapshot declares, the intended interlock design, and the proof still required. This is an illustrated design explanation, not a demonstration of live tool interception.

CHAPTERS
''' + '\n'.join(f'{c["timestamp"]} {c["title"]}' for c in chapters) + f'''

THE QUESTION
What evidence would convince you that an unauthorized action was prevented before it happened—and that authorized work could still proceed?

PRODUCTION
Fictional human scenes use AI-generated imagery. Narration is synthetic. Circuit animation is illustrative; it does not establish live execution. Current, target, and gap labels preserve the scope of the explanation.

Follow SideFX for agentic engineering:
{CHANNEL}

#AgenticEngineering #AIAgents #SideFX
'''
    (KIT / 'description.txt').write_text(description, encoding='utf-8')
    (KIT / 'title.txt').write_text(TITLE + '\n', encoding='utf-8')
    (KIT / 'pinned-comment.txt').write_text(
        'A decision result is not yet proof of enforcement. What would you test on both sides of the boundary: preventing an unauthorized action and permitting the authorized work?\n\n'
        f'Film, transcript, and evidence guide: {SITE}\n', encoding='utf-8')
    (KIT / 'transcript.txt').write_text('\n\n'.join(f'{c["timestamp"]} {c["title"]}\n{c["narration"]}' for c in chapters) + '\n', encoding='utf-8')
    metadata = {'title': TITLE, 'channelUrl': CHANNEL, 'landingPageUrl': SITE,
                'videoUrl': None, 'status': 'PREPARED_NOT_UPLOADED',
                'language': 'en', 'category': 'Education', 'madeForKids': False,
                'alteredOrSyntheticContent': True,
                'tags': ['agentic engineering', 'AI agents', 'AI governance', 'agent authority', 'SideFX', 'human oversight'],
                'durationSeconds': review['film']['durationSeconds'], 'media': media_files,
                'chapters': chapters}
    existing = KIT / 'release.json'
    if existing.exists():
        old = json.loads(existing.read_text(encoding='utf-8'))
        for key in ['videoUrl', 'status', 'uploadedVideoId', 'publishedAt', 'youtubeChecks', 'thumbnailStatus', 'captionsStatus', 'landingPageStatus']:
            if old.get(key): metadata[key] = old[key]
    existing.write_text(json.dumps(metadata, indent=2) + '\n', encoding='utf-8')
    public_evidence = {'scope': 'Editorial explanation of a reviewed snapshot; no live tool interception demonstrated.',
                       'capabilityId': contract['capabilityId'], 'claims': contract['claims'],
                       'sourceReferences': contract['evidence'], 'gaps': gaps['gaps'],
                       'currentEvidenceLimit': gaps['currentEvidenceLimit']}
    (PUBLIC / 'evidence-guide.json').write_text(json.dumps(public_evidence, indent=2) + '\n', encoding='utf-8')
    shutil.copy2(KIT / 'transcript.txt', PUBLIC / 'transcript.txt')
    public_video = metadata['videoUrl'] if metadata['status'] == 'PUBLISHED' else None
    (ROOT / 'release-site/app/episode.json').write_text(json.dumps({'title': TITLE, 'chapters': chapters, 'gaps': gaps['gaps'], 'videoUrl': public_video}, indent=2) + '\n', encoding='utf-8')
    print(f'Prepared upload kit: {KIT}; {len(chapters)} chapters; film and five evidence bindings verified.')


if __name__ == '__main__':
    main()
