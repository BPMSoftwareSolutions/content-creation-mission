"""Build selected JSON-store revisions. No episode-specific content or routing.

The store adapter can be replaced without changing the rendering functions.
All outputs are local review artifacts; this command has no publishing operation.
"""
import argparse
from production_store import JsonProductionStore,ROOT,write,artifact_digest

def speech(store,revision):
    import run_narration_continuity_demo as tts
    profile=store.profile(revision)
    for scene in revision['scenes']:
        audio=store.resolve(scene['audioRef']);audio.parent.mkdir(parents=True,exist_ok=True)
        tts.OUT=audio.parent
        receipt=tts.speech(scene['narration'],audio.stem,profile['speech'])
        print(revision['revisionId'],scene['id'],round(receipt['durationSeconds'],2),flush=True)

def main():
    p=argparse.ArgumentParser();p.add_argument('operation',choices=['speech','render','review'])
    p.add_argument('--store',required=True);p.add_argument('--revision')
    a=p.parse_args();store=JsonProductionStore(a.store)
    revisions=[store.get_revision(a.revision)] if a.revision else store.revisions()
    for revision in revisions:
        if a.operation=='speech':speech(store,revision)
        elif a.operation=='render':
            from production_render import render
            render(store,revision)
        else:
            from production_review import review
            review(store,revision)
    if a.operation=='review':
        from production_review import review_hub
        review_hub(store)
if __name__=='__main__':main()
