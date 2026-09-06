
from __future__ import annotations

import argparse
import asyncio
import hashlib
import inspect
import json
import os
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlsplit

import httpx
import orjson
from bs4 import BeautifulSoup, Comment
from mcp import Client
from mcp.server import MCPServer
from pydantic import BaseModel, ConfigDict, Field, TypeAdapter


COMPILER_VERSION = "rapidapi-assimilator-reference.v1"
RAPID_HOST_PATTERN = re.compile(r"^[a-z0-9-]+\.p\.rapidapi\.com$", re.I)
METHODS = ("GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS")
SECRET_LABELS = {"x-rapidapi-key", "authorization", "cookie", "set-cookie"}


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class EvidenceRef(StrictModel):
    kind: str
    locator: str


class ParameterObservation(StrictModel):
    name: str
    location: str = "query"
    requiredMarker: bool
    documentedType: str
    documentedDefault: str | int | float | bool | None = None
    exampleValuePresent: bool
    description: str
    authority: str = "RENDERED_DOM_OBSERVATION"
    evidence: EvidenceRef


class CatalogOperation(StrictModel):
    endpointId: str
    method: str
    pathLabel: str
    deprecatedLabelObserved: bool
    evidence: EvidenceRef


class SelectedOperation(StrictModel):
    endpointId: str
    method: str
    path: str
    queryParameterNames: list[str]
    parameters: list[ParameterObservation]
    deprecatedDisposition: str
    requestBodyDisposition: str
    responseContractDisposition: str
    toolName: str
    evidence: list[EvidenceRef]


class ProductIdentity(StrictModel):
    publisherSlug: str
    productSlug: str
    displayName: str
    marketplaceUrl: str


class GatewayBindingCandidate(StrictModel):
    gateway: str = "RAPIDAPI_RUNTIME"
    scheme: str = "https"
    host: str
    requiredHeaders: list[str] = Field(default_factory=lambda: ["X-RapidAPI-Host", "X-RapidAPI-Key"])
    credentialReference: str = "env:RAPID_API_KEY"
    credentialValueRetained: bool = False
    additionalAuthorizationDisposition: str


class Coverage(StrictModel):
    catalogCompleteness: str
    renderedCatalogOperationCount: int
    selectedOperationRequestObserved: bool
    selectedOperationParameterCount: int
    selectedOperationResponseSchemaObserved: bool
    openApiDocumentObserved: bool
    companionAssetCount: int
    findings: list[str]


class CaptureCandidate(StrictModel):
    captureId: str
    sourceFileName: str
    sourceClassification: str
    sourceDigestDisclosure: str
    product: ProductIdentity
    gatewayBinding: GatewayBindingCandidate
    selectedOperation: SelectedOperation
    catalog: list[CatalogOperation]
    coverage: Coverage
    providerAdmissionDisposition: str
    duplicateOfCaptureId: str | None = None


class Compilation(StrictModel):
    schemaVersion: str = "remote-api-compilation-observation.v1"
    compiler: str = COMPILER_VERSION
    deterministic: bool = True
    credentialPolicy: dict[str, Any]
    captures: list[CaptureCandidate]
    uniqueProviderOperationCount: int
    compilationDisposition: str
    findings: list[str]
    compilationDigest: str | None = None


def canonical_bytes(value: Any) -> bytes:
    return orjson.dumps(value, option=orjson.OPT_SORT_KEYS)


def sha256(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def resolve_rapidapi_key() -> tuple[str | None, str]:
    """Resolve the runtime secret without reading it from the saved HTML captures."""
    value = os.environ.get("RAPID_API_KEY")
    if value:
        return value, "PROCESS_ENVIRONMENT"
    if os.name != "nt":
        return None, "UNAVAILABLE"
    try:
        import winreg

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
            value, _ = winreg.QueryValueEx(key, "RAPID_API_KEY")
        if value:
            return str(value), "WINDOWS_USER_ENVIRONMENT"
    except (FileNotFoundError, OSError):
        pass
    return None, "UNAVAILABLE"


def normalized_text(node: Any) -> str:
    return " ".join(node.get_text(" ", strip=True).split())


def parse_saved_url(soup: BeautifulSoup) -> str:
    for comment in soup.find_all(string=lambda x: isinstance(x, Comment)):
        match = re.search(r"saved from url=\(\d+\)(https://rapidapi\.com/[^\s]+)", str(comment), re.I)
        if match:
            return match.group(1)
    raise ValueError("RAPIDAPI_SAVED_URL_NOT_FOUND")


def parse_identity(saved_url: str, soup: BeautifulSoup) -> tuple[ProductIdentity, str]:
    parts = [part for part in urlsplit(saved_url).path.split("/") if part]
    if len(parts) < 5 or parts[1] != "api" or parts[3] != "playground":
        raise ValueError("RAPIDAPI_MARKETPLACE_IDENTITY_UNRECOGNIZED")
    publisher, product_slug = parts[0], parts[2]
    endpoint_id = parts[4]
    if not endpoint_id.startswith("apiendpoint_"):
        raise ValueError("RAPIDAPI_ENDPOINT_ID_UNRECOGNIZED")
    title = normalized_text(soup.title) if soup.title else product_slug
    if " | RapidAPI" in title:
        title = title.split(" | RapidAPI", 1)[0]
    identity = ProductIdentity(
        publisherSlug=publisher,
        productSlug=product_slug,
        displayName=title,
        marketplaceUrl=f"https://rapidapi.com/{publisher}/api/{product_slug}",
    )
    return identity, endpoint_id


def parse_shell_request(soup: BeautifulSoup) -> tuple[str, str, list[tuple[str, str]], set[str]]:
    code = soup.select_one("pre code.language-shell")
    if code is None:
        raise ValueError("RAPIDAPI_SHELL_SNIPPET_NOT_FOUND")
    text = code.get_text("\n", strip=True)
    method_match = re.search(r"\bcurl\s+--request\s+(" + "|".join(METHODS) + r")\b", text, re.I)
    url_match = re.search(r"--url\s+['\"](https://[^'\"]+)['\"]", text, re.I)
    if not method_match or not url_match:
        raise ValueError("RAPIDAPI_SHELL_SNIPPET_UNSUPPORTED")
    method = method_match.group(1).upper()
    parsed = urlsplit(url_match.group(1))
    if parsed.scheme != "https" or not parsed.hostname or not RAPID_HOST_PATTERN.fullmatch(parsed.hostname):
        raise ValueError("RAPIDAPI_GATEWAY_HOST_INVALID")
    header_names = {m.lower() for m in re.findall(r"--header\s+['\"]([^:'\"]+):", text, re.I)}
    return method, parsed.path or "/", list(parse_qsl(parsed.query, keep_blank_values=True)), header_names


def parse_default(text: str, documented_type: str) -> str | int | float | bool | None:
    match = re.search(r"\bDefault:\s*([^\s]+)", text, re.I)
    if not match:
        return None
    value = match.group(1).strip()
    lowered = documented_type.lower()
    try:
        if lowered in {"number", "integer", "int"}:
            return int(value) if re.fullmatch(r"-?\d+", value) else float(value)
        if lowered in {"boolean", "bool"}:
            return value.lower() == "true"
    except ValueError:
        return value
    return value


def parse_parameters(soup: BeautifulSoup, query_pairs: list[tuple[str, str]]) -> list[ParameterObservation]:
    example_names = {name for name, _ in query_pairs}
    observations: list[ParameterObservation] = []
    seen: set[str] = set()
    for label in soup.select("label[aria-label]"):
        name = (label.get("aria-label") or "").strip()
        if not name or name.lower() in SECRET_LABELS or name in {"App", "Request URL", "X-RapidAPI-Host"}:
            continue
        container = label.parent.parent if label.parent and label.parent.parent else label.parent
        if container is None:
            continue
        text = normalized_text(container)
        required = "*" in normalized_text(label.parent) if label.parent else False
        type_match = re.search(r"\b(String|Number|Integer|Boolean|Array|Object|File)\.", text, re.I)
        documented_type = type_match.group(1).lower() if type_match else "string"
        observations.append(ParameterObservation(
            name=name,
            requiredMarker=required,
            documentedType=documented_type,
            documentedDefault=parse_default(text, documented_type),
            exampleValuePresent=name in example_names,
            description=text,
            evidence=EvidenceRef(kind="DOM", locator=f'label[aria-label="{name}"]'),
        ))
        seen.add(name)
    for name, _ in query_pairs:
        if name not in seen:
            observations.append(ParameterObservation(
                name=name,
                requiredMarker=False,
                documentedType="string",
                exampleValuePresent=True,
                description="Observed only in the selected request URL.",
                authority="DISPLAYED_REQUEST_EXAMPLE",
                evidence=EvidenceRef(kind="DOM", locator="pre code.language-shell"),
            ))
    return observations


def parse_catalog(soup: BeautifulSoup) -> list[CatalogOperation]:
    rows: list[CatalogOperation] = []
    seen: set[str] = set()
    for anchor in soup.select('a[href*="/playground/apiendpoint_"]'):
        href = anchor.get("href") or ""
        endpoint_match = re.search(r"(apiendpoint_[A-Za-z0-9-]+)", href)
        label = normalized_text(anchor)
        method_match = re.match(r"(" + "|".join(METHODS) + r")\s+(.+)", label, re.I)
        if not endpoint_match or not method_match:
            continue
        endpoint_id = endpoint_match.group(1)
        if endpoint_id in seen:
            continue
        seen.add(endpoint_id)
        path_label = re.sub(r"\s*\(Deprecated\)\s*$", "", method_match.group(2), flags=re.I).strip()
        rows.append(CatalogOperation(
            endpointId=endpoint_id,
            method=method_match.group(1).upper(),
            pathLabel="/" + path_label.lstrip("/"),
            deprecatedLabelObserved="deprecated" in label.lower(),
            evidence=EvidenceRef(kind="DOM", locator=f'a[href*="{endpoint_id}"]'),
        ))
    return rows


def build_tool_name(product_slug: str, method: str, path: str) -> str:
    raw = f"{product_slug}_{method.lower()}_{path.strip('/')}"
    value = re.sub(r"[^a-zA-Z0-9_]+", "_", raw).strip("_").lower()
    return value[:96]


def detect_additional_auth(soup: BeautifulSoup) -> str:
    text = normalized_text(soup)
    return "NONE_OBSERVED" if "No additional authorizations needed" in text else "UNKNOWN"


def companion_directory(path: Path) -> Path | None:
    candidate = path.with_name(path.stem + "_files")
    return candidate if candidate.is_dir() else None


def compile_capture(path: Path) -> CaptureCandidate:
    raw = path.read_bytes()
    soup = BeautifulSoup(raw.decode("utf-8", errors="replace"), "lxml")
    saved_url = parse_saved_url(soup)
    product, endpoint_id = parse_identity(saved_url, soup)
    method, request_path, query_pairs, headers = parse_shell_request(soup)
    host_values = {
        (node.get("value") or "").strip()
        for node in soup.select('input[aria-label="X-RapidAPI-Host value"]')
        if node.get("value")
    }
    curl_hosts = set(re.findall(r"\b[a-z0-9-]+\.p\.rapidapi\.com\b", str(soup.select_one("pre code.language-shell")), re.I))
    hosts = {h.lower() for h in host_values | curl_hosts if RAPID_HOST_PATTERN.fullmatch(h)}
    if len(hosts) != 1:
        raise ValueError("RAPIDAPI_GATEWAY_HOST_AMBIGUOUS")
    host = next(iter(hosts))
    required = {"x-rapidapi-key", "x-rapidapi-host"}
    if not required.issubset(headers):
        raise ValueError("RAPIDAPI_REQUIRED_HEADERS_NOT_OBSERVED")
    parameters = parse_parameters(soup, query_pairs)
    catalog = parse_catalog(soup)
    selected_catalog = next((row for row in catalog if row.endpointId == endpoint_id), None)
    deprecated = (
        "OBSERVED_DEPRECATED" if selected_catalog and selected_catalog.deprecatedLabelObserved
        else "OBSERVED_CURRENT" if selected_catalog
        else "UNKNOWN_NOT_RENDERED_IN_CATALOG"
    )
    assets = companion_directory(path)
    asset_count = sum(1 for p in assets.rglob("*") if p.is_file()) if assets else 0
    findings = [
        "COMPLETE_OPERATION_CATALOG_NOT_ESTABLISHED",
        "SELECTED_OPERATION_RESPONSE_CONTRACT_NOT_CAPTURED",
    ]
    if deprecated == "OBSERVED_DEPRECATED":
        findings.append("SELECTED_OPERATION_DEPRECATED")
    if deprecated == "UNKNOWN_NOT_RENDERED_IN_CATALOG":
        findings.append("SELECTED_OPERATION_DEPRECATION_UNKNOWN")
    capture_id = sha256(canonical_bytes({
        "marketplaceUrl": product.marketplaceUrl,
        "endpointId": endpoint_id,
        "method": method,
        "path": request_path,
        "parameters": [p.model_dump(mode="json") for p in parameters],
    }))
    selected = SelectedOperation(
        endpointId=endpoint_id,
        method=method,
        path=request_path,
        queryParameterNames=sorted({name for name, _ in query_pairs}),
        parameters=parameters,
        deprecatedDisposition=deprecated,
        requestBodyDisposition="NO_BODY_OBSERVED_NOT_PROOF_OF_ABSENCE",
        responseContractDisposition="NOT_CAPTURED",
        toolName=build_tool_name(product.productSlug, method, request_path),
        evidence=[
            EvidenceRef(kind="HTML_SAVE_COMMENT", locator="saved from url"),
            EvidenceRef(kind="DOM", locator="pre code.language-shell"),
            EvidenceRef(kind="DOM", locator='label[aria-label]'),
        ],
    )
    return CaptureCandidate(
        captureId=capture_id,
        sourceFileName=path.name,
        sourceClassification="BROWSER_SAVED_RAPIDAPI_PLAYGROUND_HTML",
        sourceDigestDisclosure="OMITTED_RESTRICTED_CAPTURE_CONTAINS_CREDENTIAL_MATERIAL",
        product=product,
        gatewayBinding=GatewayBindingCandidate(
            host=host,
            additionalAuthorizationDisposition=detect_additional_auth(soup),
        ),
        selectedOperation=selected,
        catalog=catalog,
        coverage=Coverage(
            catalogCompleteness="UNKNOWN",
            renderedCatalogOperationCount=len(catalog),
            selectedOperationRequestObserved=True,
            selectedOperationParameterCount=len(parameters),
            selectedOperationResponseSchemaObserved=False,
            openApiDocumentObserved=False,
            companionAssetCount=asset_count,
            findings=findings,
        ),
        providerAdmissionDisposition="HELD_INCOMPLETE_DOCUMENTATION",
    )


def compile_directory(root: Path) -> Compilation:
    captures = [compile_capture(path) for path in sorted(root.glob("*.html"), key=lambda p: p.name.casefold())]
    first_by_id: dict[str, str] = {}
    for capture in captures:
        if capture.captureId in first_by_id:
            capture.duplicateOfCaptureId = first_by_id[capture.captureId]
        else:
            first_by_id[capture.captureId] = capture.captureId
    result = Compilation(
        credentialPolicy={
            "runtimeReference": "env:RAPID_API_KEY",
            "capturedCredentialAccepted": False,
            "credentialValueRetained": False,
            "rawSourceClassification": "RESTRICTED",
        },
        captures=captures,
        uniqueProviderOperationCount=len(first_by_id),
        compilationDisposition="PARTIAL_PROVIDER_OPERATION_CANDIDATES",
        findings=[
            "ALL_CAPTURES_SHARE_RAPIDAPI_RUNTIME_HEADER_ENVELOPE",
            "NO_CAPTURE_ESTABLISHES_COMPLETE_OPERATION_CATALOG",
            "NO_CAPTURE_CONTAINS_SELECTED_OPERATION_RESPONSE_SCHEMA",
            "PROVIDER_ENTITLEMENT_MUST_BE_QUALIFIED_SEPARATELY",
        ],
    )
    payload=result.model_dump(mode="json", exclude={"compilationDigest"})
    result.compilationDigest=sha256(canonical_bytes(payload))
    return result


def annotation_for(parameter: ParameterObservation) -> Any:
    kind=parameter.documentedType.lower()
    if kind in {"number"}:
        return float
    if kind in {"integer","int"}:
        return int
    if kind in {"boolean","bool"}:
        return bool
    if kind == "array":
        return list[Any]
    if kind == "object":
        return dict[str, Any]
    return str


def build_server(compilation: Compilation) -> MCPServer:
    server=MCPServer(
        name="Agentic Harness RapidAPI Reference",
        version="0.1.0-observation",
        instructions="Tools are projected from content-addressed RapidAPI operation descriptors.",
    )
    for capture in compilation.captures:
        if capture.duplicateOfCaptureId is not None:
            continue
        operation=capture.selectedOperation
        binding=capture.gatewayBinding
        query_examples={}
        # The values are intentionally not retained by the compiler output. Defaults come only from docs.
        signature_parameters=[]
        for parameter in operation.parameters:
            annotation=annotation_for(parameter)
            if parameter.requiredMarker:
                default=inspect.Parameter.empty
            else:
                default=parameter.documentedDefault
            signature_parameters.append(inspect.Parameter(
                parameter.name,
                inspect.Parameter.KEYWORD_ONLY,
                annotation=annotation,
                default=default,
            ))
        signature_parameters.append(inspect.Parameter(
            "evidence_only",
            inspect.Parameter.KEYWORD_ONLY,
            annotation=bool,
            default=True,
        ))

        def make_handler(cap: CaptureCandidate):
            async def handler(**kwargs: Any) -> dict[str, Any]:
                evidence_only=bool(kwargs.pop("evidence_only",True))
                key,_=resolve_rapidapi_key()
                if not key:
                    return {"disposition":"CREDENTIAL_REQUIRED","credentialReference":"env:RAPID_API_KEY"}
                params={k:v for k,v in kwargs.items() if v is not None}
                started=asyncio.get_running_loop().time()
                async with httpx.AsyncClient(timeout=httpx.Timeout(25.0),follow_redirects=False,headers={"Accept-Encoding":"identity"}) as client:
                    response=await client.request(
                        cap.selectedOperation.method,
                        f"https://{cap.gatewayBinding.host}{cap.selectedOperation.path}",
                        params=params,
                        headers={"X-RapidAPI-Key":key,"X-RapidAPI-Host":cap.gatewayBinding.host},
                    )
                elapsed=round((asyncio.get_running_loop().time()-started)*1000)
                body=response.content
                output={
                    "disposition":"SUCCEEDED" if 200<=response.status_code<300 else "PROVIDER_REJECTED",
                    "providerOperationId":cap.captureId,
                    "toolName":cap.selectedOperation.toolName,
                    "status":response.status_code,
                    "elapsedMs":elapsed,
                    "contentType":response.headers.get("content-type","").split(";")[0].lower(),
                    "bodyBytes":len(body),
                    "bodySha256":sha256(body),
                    "rapidApiVersionHeaderPresent":bool(response.headers.get("x-rapidapi-version")),
                    "requestIdHeaderPresent":any(k.lower() in {"x-rapidapi-request-id","x-request-id"} for k in response.headers),
                    "credentialValueRetained":False,
                }
                if not evidence_only and len(body)<=2_000_000:
                    try:
                        output["body"]=response.json()
                    except Exception:
                        output["bodyText"]=body.decode("utf-8","replace")
                return output
            handler.__name__=f"invoke_{cap.selectedOperation.toolName}"
            handler.__doc__=(
                f"{cap.selectedOperation.method} {cap.selectedOperation.path} via "
                f"{cap.product.displayName} on RapidAPI. Provider admission: "
                f"{cap.providerAdmissionDisposition}."
            )
            return handler

        handler=make_handler(capture)
        handler.__signature__=inspect.Signature(signature_parameters,return_annotation=dict[str,Any])
        server.add_tool(
            handler,
            name=operation.toolName,
            title=f"{capture.product.displayName}: {operation.method} {operation.path}",
            description=handler.__doc__,
            structured_output=True,
        )
    return server


async def prove_mcp(compilation: Compilation) -> dict[str, Any]:
    server=build_server(compilation)
    async with Client(server) as client:
        listed=await client.list_tools()
        tools=[]
        for tool in listed.tools:
            tools.append({
                "name":tool.name,
                "title":tool.title,
                "inputSchema":tool.input_schema,
            })
        by_product={c.product.productSlug:c for c in compilation.captures if c.duplicateOfCaptureId is None}
        calls=[]
        call_specs=[
            ("yahoo-finance166",{"snippetCount":500,"region":"US","evidence_only":True}),
            ("yh-finance",{"messageBoardId":"finmb_24937","offset":0,"sort_by":"newest","count":16,"evidence_only":True}),
        ]
        for slug,args in call_specs:
            cap=by_product[slug]
            result=await client.call_tool(cap.selectedOperation.toolName,args)
            payload=result.structured_content
            if payload is None and result.content:
                payload=json.loads(result.content[0].text)
            calls.append({
                "toolName":cap.selectedOperation.toolName,
                "protocolResultIsError":result.is_error,
                "structuredResult":payload,
            })
        proof={
            "proofType":"rapidapi-descriptor-to-mcp-reference-observation.v1",
            "compiler":COMPILER_VERSION,
            "compilationDigest":compilation.compilationDigest,
            "officialSdkPackage":"mcp==2.1.1",
            "toolCount":len(tools),
            "tools":tools,
            "calls":calls,
        }
        proof["proofDigest"]=sha256(canonical_bytes(proof))
        return proof


def write_canonical(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(orjson.dumps(value,option=orjson.OPT_SORT_KEYS|orjson.OPT_INDENT_2)+b"\n")


def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("command",choices=["compile","schema","prove-mcp"])
    parser.add_argument("--input",type=Path,default=Path(r"C:\lab\rapid-api"))
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    if args.command=="schema":
        write_canonical(args.output,Compilation.model_json_schema())
        return 0
    compilation=compile_directory(args.input)
    TypeAdapter(Compilation).validate_python(compilation.model_dump())
    if args.command=="compile":
        write_canonical(args.output,compilation.model_dump(mode="json"))
        return 0
    proof=asyncio.run(prove_mcp(compilation))
    write_canonical(args.output,proof)
    return 0


if __name__=="__main__":
    raise SystemExit(main())
