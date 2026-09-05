"""Enforce exact-image review binding; never infer visual conformance from structure."""
import hashlib,json
from pathlib import Path
from jsonschema import validate

ROOT=Path(__file__).resolve().parents[1]
DIMENSIONS=('phaseDistinction','humanLegibility','causalClarity','outcomeClosure','continuity','semanticFidelity','labelIndependence','operationalReality')

def validate_review(review,job,image_bytes):
    validate(review,json.loads((ROOT/'evaluations/visual-experience-review.schema.json').read_text()))
    if review['imageDigest']!=hashlib.sha256(image_bytes).hexdigest():
        raise ValueError('VISUAL_REVIEW_STALE_IMAGE')
    if review['scenarioKey']!=job['scenarioKey'] or review['directorVersion']!=job['directorVersion']:
        raise ValueError('VISUAL_REVIEW_IDENTITY_MISMATCH')
    conforms=all(review['dimensions'][d]['passes'] for d in DIMENSIONS) and not review['findings']
    if (review['disposition']=='VISUAL_EXPERIENCE_CONFORMS')!=conforms:
        raise ValueError('VISUAL_REVIEW_DISPOSITION_CONTRADICTS_FINDINGS')
    return conforms
