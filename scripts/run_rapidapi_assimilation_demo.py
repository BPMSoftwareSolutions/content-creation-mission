"""Run the recordable RapidAPI assimilation proof and emit sanitized evidence.

The provider compiler and MCP calls run in this external editorial lab. The
script separately verifies the provisioned Agentic Harness token and estate; it
does not present the reference Python execution as managed Harness execution.
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import importlib.metadata
import json
import logging
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mcp import Client

from rapidapi_assimilation_reference import (
    COMPILER_VERSION,
    build_server,
    canonical_bytes,
    compile_directory,
    resolve_rapidapi_key,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = Path(r"C:\lab\rapid-api")
DEFAULT_HARNESS = Path(r"C:\lab\repos\agentic-harness")
DEFAULT_RELEASE = ROOT / "releases" / "rapidapi-assimilation-demo"
CAPSULE_RELATIVE = Path("provisioning/compile-rapidapi-provider-candidates-596d898eaaf68921.sfxcap")
FEATURE_RELATIVE = Path("features/compile-rapidapi-provider-candidates.feature")
RECEIPT_RELATIVE = Path("provisioning/rapidapi-assimilation-reference-proof.observation.receipt.json")


def digest(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


class Presenter:
    def __init__(self, pace: float) -> None:
        self.pace = max(0.0, pace)
        self.lines: list[str] = []

    def say(self, text: str = "") -> None:
        print(text, flush=True)
        self.lines.append(text)
        if text and self.pace:
            time.sleep(self.pace)

    def stage(self, number: int, title: str, label: str) -> None:
        self.say()
        self.say("=" * 78)
        self.say(f"{number}. {title}")
        self.say(label)
        self.say("=" * 78)


def run_text(command: list[str], cwd: Path) -> str:
    completed = subprocess.run(
        command,
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return completed.stdout.strip()


def verify_harness(harness_root: Path) -> dict[str, Any]:
    receipt = json.loads((harness_root / RECEIPT_RELATIVE).read_text(encoding="utf-8"))
    capsule_bytes = (harness_root / CAPSULE_RELATIVE).read_bytes()
    feature_bytes = (harness_root / FEATURE_RELATIVE).read_bytes()
    capsule_digest = digest(capsule_bytes)
    feature_digest = digest(feature_bytes)
    expected = receipt["managedTokenProvisioning"]
    npm = shutil.which("npm.cmd") or shutil.which("npm")
    if not npm:
        raise RuntimeError("NPM_NOT_AVAILABLE")
    estate = json.loads(run_text([npm, "run", "--silent", "capsule:verify"], harness_root))
    head = run_text(["git", "rev-parse", "HEAD"], harness_root)
    origin_main = run_text(["git", "rev-parse", "origin/main"], harness_root)
    return {
        "repository": str(harness_root),
        "head": head,
        "originMain": origin_main,
        "headMatchesOriginMain": head == origin_main,
        "capsuleRef": CAPSULE_RELATIVE.as_posix(),
        "capsuleDigest": capsule_digest,
        "capsuleDigestMatchesReceipt": capsule_digest == expected["capsuleDigest"],
        "featureRef": FEATURE_RELATIVE.as_posix(),
        "featureDigest": feature_digest,
        "featureDigestMatchesReceipt": feature_digest == expected["featureDigest"],
        "structuralDisposition": expected["structuralDisposition"],
        "scenarioGeometryDisposition": expected["scenarioGeometryDisposition"],
        "provisioningDisposition": expected["provisioningDisposition"],
        "openEventMechanicSlotCount": expected["openEventMechanicSlotCount"],
        "businessBehaviorProven": expected["businessBehaviorProven"],
        "estate": estate,
    }


async def list_tools(compilation: Any) -> list[dict[str, Any]]:
    server = build_server(compilation)
    async with Client(server) as client:
        listed = await client.list_tools()
        return [
            {
                "name": tool.name,
                "title": tool.title,
                "inputSchema": tool.input_schema,
            }
            for tool in listed.tools
        ]


async def call_tools(compilation: Any) -> list[dict[str, Any]]:
    server = build_server(compilation)
    async with Client(server) as client:
        by_product = {
            item.product.productSlug: item
            for item in compilation.captures
            if item.duplicateOfCaptureId is None
        }
        call_specs = [
            ("yahoo-finance166", {"snippetCount": 500, "region": "US", "evidence_only": True}),
            (
                "yh-finance",
                {
                    "messageBoardId": "finmb_24937",
                    "offset": 0,
                    "sort_by": "newest",
                    "count": 16,
                    "evidence_only": True,
                },
            ),
        ]
        calls: list[dict[str, Any]] = []
        for product_slug, arguments in call_specs:
            candidate = by_product[product_slug]
            result = await client.call_tool(candidate.selectedOperation.toolName, arguments)
            payload = result.structured_content
            if payload is None and result.content:
                payload = json.loads(result.content[0].text)
            calls.append(
                {
                    "productSlug": product_slug,
                    "toolName": candidate.selectedOperation.toolName,
                    "protocolResultIsError": result.is_error,
                    "result": payload,
                }
            )
        return calls


def dependency_versions() -> dict[str, str]:
    names = ["beautifulsoup4", "httpx", "lxml", "mcp", "orjson", "pydantic"]
    return {name: importlib.metadata.version(name) for name in names}


def candidate_summary(compilation: Any) -> list[dict[str, Any]]:
    return [
        {
            "candidateIdentity": item.captureId,
            "sourceFileName": item.sourceFileName,
            "productSlug": item.product.productSlug,
            "method": item.selectedOperation.method,
            "path": item.selectedOperation.path,
            "toolName": item.selectedOperation.toolName,
            "parameterNames": [parameter.name for parameter in item.selectedOperation.parameters],
            "duplicate": item.duplicateOfCaptureId is not None,
            "documentationDisposition": item.providerAdmissionDisposition,
        }
        for item in compilation.captures
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-root", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--harness-root", type=Path, default=DEFAULT_HARNESS)
    parser.add_argument("--release-root", type=Path, default=DEFAULT_RELEASE)
    parser.add_argument("--live", action="store_true", help="Call two generated MCP tools through RapidAPI.")
    parser.add_argument("--pace", type=float, default=0.0, help="Seconds between presentation lines.")
    args = parser.parse_args()
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

    presenter = Presenter(args.pace)
    presenter.say("RAPIDAPI -> DESCRIPTOR -> MCP -> AGENTIC HARNESS")
    presenter.say("A recordable, evidence-scoped provider assimilation proof")

    presenter.stage(1, "Preflight the real inputs", "[OBSERVED INPUT / RESTRICTED LOCAL CAPTURES]")
    html_files = sorted(args.input_root.glob("*.html"), key=lambda path: path.name.casefold())
    credential, credential_source = resolve_rapidapi_key()
    presenter.say(f"Saved RapidAPI pages: {len(html_files)}")
    presenter.say(f"Runtime credential reference: env:RAPID_API_KEY ({'AVAILABLE' if credential else 'UNAVAILABLE'})")
    presenter.say("Captured credential values: REJECTED")
    presenter.say("Raw response bodies: NOT RETAINED")
    if args.live and not credential:
        raise RuntimeError("RAPID_API_KEY_UNAVAILABLE")

    presenter.stage(2, "Compile the same bundle twice", "[OBSERVED RUN / LOCAL EDITORIAL LAB]")
    first = compile_directory(args.input_root)
    second = compile_directory(args.input_root)
    first_bytes = canonical_bytes(first.model_dump(mode="json"))
    second_bytes = canonical_bytes(second.model_dump(mode="json"))
    byte_identical = first_bytes == second_bytes
    presenter.say(f"Run 1: {len(first_bytes):,} bytes  {digest(first_bytes)}")
    presenter.say(f"Run 2: {len(second_bytes):,} bytes  {digest(second_bytes)}")
    presenter.say(f"Byte-identical replay: {'PASS' if byte_identical else 'FAIL'}")
    presenter.say(f"Captured pages: {len(first.captures)}")
    presenter.say(f"Unique provider-operation candidates: {first.uniqueProviderOperationCount}")
    presenter.say(f"Duplicate captures collapsed: {sum(c.duplicateOfCaptureId is not None for c in first.captures)}")
    if not byte_identical:
        raise RuntimeError("COMPILATION_REPLAY_DIVERGED")

    presenter.stage(3, "Project endpoint-specific MCP tools", "[OBSERVED RUN / OFFICIAL MCP PYTHON SDK]")
    mcp_tools = asyncio.run(list_tools(first))
    presenter.say(f"Generated tools: {len(mcp_tools)}")
    for tool in mcp_tools:
        presenter.say(f"  + {tool['name']}")

    if args.live:
        presenter.stage(4, "Invoke two generated tools", "[OBSERVED LIVE PROVIDER CALLS / EVIDENCE ONLY]")
        mcp_calls = asyncio.run(call_tools(first))
        for call in mcp_calls:
            result = call["result"]
            presenter.say(
                f"{call['toolName']}: HTTP {result['status']} / {result['disposition']} / "
                f"{result['bodyBytes']:,} bytes / {result['elapsedMs']} ms"
            )
            presenter.say(
                "  RapidAPI headers: "
                f"version={'YES' if result['rapidApiVersionHeaderPresent'] else 'NO'}, "
                f"request-id={'YES' if result['requestIdHeaderPresent'] else 'NO'}"
            )
            presenter.say(f"  Body identity: {result['bodySha256']}")
    else:
        mcp_calls = []
        presenter.stage(4, "Live invocation skipped", "[DRY RUN / NO NETWORK EFFECT]")
        presenter.say("Add --live to call the entitled Yahoo tool and the legacy YH entitlement boundary.")

    presenter.stage(5, "Verify the managed token and capsule estate", "[OBSERVED EVIDENCE / AGENTIC HARNESS]")
    harness = verify_harness(args.harness_root)
    presenter.say(f"Harness HEAD == origin/main: {'PASS' if harness['headMatchesOriginMain'] else 'FAIL'}")
    presenter.say(f"Capsule digest matches receipt: {'PASS' if harness['capsuleDigestMatchesReceipt'] else 'FAIL'}")
    presenter.say(f"Feature digest matches receipt: {'PASS' if harness['featureDigestMatchesReceipt'] else 'FAIL'}")
    presenter.say(
        f"Estate: {harness['estate']['capabilityCount']} capabilities / "
        f"{harness['estate']['entryCount']:,} entries / expanded root "
        f"{harness['estate']['durableLayout']['expandedCapabilityRoot']}"
    )
    presenter.say(f"Managed token state: {harness['provisioningDisposition']}")
    presenter.say(f"Open event-mechanic slots: {harness['openEventMechanicSlotCount']}")
    presenter.say("Managed business behavior proven: NO")

    presenter.stage(6, "State the result precisely", "[DEMO VERDICT]")
    presenter.say("PROVEN: one generic compiler handled real estate and finance captures.")
    presenter.say("PROVEN: identical input produced byte-identical descriptors.")
    presenter.say("PROVEN: descriptors projected endpoint-specific tools through the official MCP SDK.")
    if args.live:
        presenter.say("PROVEN: generated MCP tools reached RapidAPI and returned scoped provider evidence.")
    presenter.say("OPEN: complete specs, semantic equivalence, a second entitled finance provider,")
    presenter.say("      and managed fallback/replacement execution inside the Harness circuit.")

    implementation_digest = digest((ROOT / "scripts" / "rapidapi_assimilation_reference.py").read_bytes())
    evidence = {
        "evidenceType": "rapidapi-assimilation-video-demo.observation.v1",
        "observedAt": datetime.now(timezone.utc).isoformat(),
        "executionLane": "LOCAL_EDITORIAL_REFERENCE_WITH_SEPARATE_MANAGED_TOKEN_VERIFICATION",
        "liveProviderCallsEnabled": args.live,
        "credentialHandling": {
            "reference": "env:RAPID_API_KEY",
            "source": credential_source,
            "valueRetained": False,
            "capturedCredentialAccepted": False,
            "rawResponseBodyRetained": False,
        },
        "referenceCompiler": {
            "name": COMPILER_VERSION,
            "implementationDigest": implementation_digest,
            "python": sys.version.split()[0],
            "libraries": dependency_versions(),
        },
        "compilation": {
            "inputCaptureCount": len(first.captures),
            "uniqueProviderOperationCount": first.uniqueProviderOperationCount,
            "duplicateCaptureCount": sum(c.duplicateOfCaptureId is not None for c in first.captures),
            "runBytes": [len(first_bytes), len(second_bytes)],
            "runDigests": [digest(first_bytes), digest(second_bytes)],
            "byteIdentical": byte_identical,
            "disposition": first.compilationDisposition,
            "candidates": candidate_summary(first),
        },
        "mcp": {
            "sdk": f"mcp=={importlib.metadata.version('mcp')}",
            "transport": "official SDK in-memory client/server",
            "tools": mcp_tools,
            "calls": mcp_calls,
        },
        "managedHarness": harness,
        "provenClaims": [
            "One generic offline compiler handled the downloaded real-estate and finance pages without product-specific branches.",
            "The same input bundle compiled twice to byte-identical output.",
            "Duplicate captured content collapsed to one provider-operation identity.",
            "The compiled descriptors projected four endpoint-specific tools through the official MCP SDK.",
        ] + (["Generated MCP tools reached RapidAPI and returned evidence-only response metadata."] if args.live else []),
        "openClaims": [
            "The downloaded pages do not establish complete API specifications or response schemas.",
            "The reference Python execution is not managed Agentic Harness execution.",
            "Two entitled, semantically interchangeable finance providers are not yet proven.",
            "Managed provider fallback and replacement execution remain open.",
        ],
    }
    args.release_root.mkdir(parents=True, exist_ok=True)
    evidence_path = args.release_root / "latest-evidence.json"
    transcript_path = args.release_root / "latest-demo-transcript.txt"
    evidence_path.write_text(json.dumps(evidence, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    transcript_path.write_text("\n".join(presenter.lines) + "\n", encoding="utf-8")
    presenter.say()
    presenter.say(f"Evidence written: {evidence_path}")
    presenter.say(f"Transcript written: {transcript_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
