#!/usr/bin/env python3
"""Report 02 locked cross-seed runner (Python standard library only).

Modes:
  --self-test   Offline checks only; zero Ollama model calls.
  --preflight   Read-only verification of frozen candidate inputs and local Ollama.
  --run --confirm-frozen-run
               Exactly 45 cases x 2 fixed seeds; requires a frozen manifest,
               valid local model digest, and date 2-15 November 2026 UTC.

The runner never reads reference_label/reference_rationale when rendering a prompt.
Preserves full wire request/response bytes in base64-encoded append-only JSONL
receipts, including retries, plus one strict scorer-compatible final row per
successful case/pass. DO NOT replace or resume a partially executed run.
"""

import argparse
import base64
import hashlib
import json
import os
import socket
import sys
import tempfile
import urllib.error
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

NAME = "qwen3:0.6b"
DIGEST = "7df6b6e09427a769808717c0a93cadc4ae99ed4eb8bf5ca557c90846becea435"
MODEL_VERSION = "0.40.11"
API_ROOT = "http://localhost:11434"
VALID_DATES = (date(2026, 11, 2), date(2026, 11, 15))
EXPECTED = {
    "main_dataset_45_v0_2_REVIEW.json": "74086847af27fbaffa38f0d794da7cff579d18f41fdb14afd2f8c10abebf6190",
    "model_contract_v0_1_REVIEW.json": "1b9c3d2c05a8785283b2bb30dab1d09dc3c47403f5bf4b8c99a2029d2a5f7beb",
    "report02_score_v0_1.py": "8797504a9c4080ea35ae28c192a04122502258935a8d46e5d4fc566d2cb747a2",
    "model_environment_v0_1_REVIEW.json": "bce603a748b03ee232ef35c65d2010665b91e42be0db4b9fdb7f2fc5c000d893",
    "protocol_v0_2_REVIEW.md": "91831de4bf4c389a79245373fed9e19bff8e73d1f8150354465ae979bb96ed73",
    "calibration_review_v0_1.md": "79a7ce46016690a92c222507fbb5cadd84b859d3538aa5b58ce751c395627544",
}


class IntegrityError(Exception):
    pass


class TransportFailure(Exception):
    pass


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def load_json_file(path):
    return json.loads(path.read_text(encoding="utf-8"))


def append_event(path, event):
    encoded = (json.dumps(event, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
    with path.open("ab") as fh:
        fh.write(encoded)
        fh.flush()
        os.fsync(fh.fileno())


def atomic_json(path, data):
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("x", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)


def check_files(folder, include_runner=False):
    checks = dict(EXPECTED)
    if include_runner:
        checks[Path(__file__).name] = digest(Path(__file__).read_bytes())
    for name, expected in checks.items():
        path = folder / name
        if not path.is_file():
            raise IntegrityError(f"Missing required input: {name}")
        actual = digest(path.read_bytes())
        if actual != expected:
            raise IntegrityError(f"Hash mismatch: {name} ({actual})")
    return checks


def load_inputs(folder):
    check_files(folder)
    ds = load_json_file(folder / "main_dataset_45_v0_2_REVIEW.json")
    c = load_json_file(folder / "model_contract_v0_1_REVIEW.json")
    env = load_json_file(folder / "model_environment_v0_1_REVIEW.json")
    if not isinstance(ds, list) or len(ds) != 45:
        raise IntegrityError("Expected 45 dataset records")
    ids = [rec.get("id") for rec in ds]
    if set(ids) != {f"MAIN-{i:03d}" for i in range(1, 46)}:
        raise IntegrityError("Unexpected dataset identifiers")
    for rec in ds:
        if not isinstance(rec.get("evidence"), str) or not isinstance(rec.get("claim"), str):
            raise IntegrityError(f"Missing prompt data for {rec['id']}")
    if (c.get("model") != NAME or c.get("endpoint") != API_ROOT + "/api/generate"
            or c.get("dataset_sha256") != EXPECTED["main_dataset_45_v0_2_REVIEW.json"]
            or c.get("passes") != [{"id": "A", "seed": 101}, {"id": "B", "seed": 202}]):
        raise IntegrityError("Model, endpoint, seeds or dataset mismatch")
    if (c.get("request", {}).get("stream") is not False
            or c["request"].get("think") is not False
            or c["request"].get("options_common") != {"temperature": 0.2, "num_ctx": 2048, "num_predict": 64}
            or c.get("run_policy", {}).get("maximum_transport_retries") != 1):
        raise IntegrityError("Unexpected request or retry settings")
    schema = c["request"].get("format")
    if schema != {"type": "object", "properties": {"label": {"type": "string", "enum": ["SUPPORTED", "CONTRADICTED", "NOT_ESTABLISHED"]}}, "required": ["label"], "additionalProperties": False}:
        raise IntegrityError("Unexpected JSON output schema")
    prompt = c.get("prompt_template", "")
    if not isinstance(prompt, str) or prompt.count("{evidence}") != 1 or prompt.count("{claim}") != 1:
        raise IntegrityError("Invalid prompt placeholders")
    if "reference_label" in prompt or "reference_rationale" in prompt:
        raise IntegrityError("Reference-label leakage")
    if c.get("model_input_fields") != ["evidence", "claim"]:
        raise IntegrityError("Unexpected model input fields")
    if (env.get("ollama_version") != MODEL_VERSION or env.get("model_digest") != DIGEST
            or env.get("model_name") != NAME):
        raise IntegrityError("Recorded Ollama environment mismatch")
    return ds, c, env


def opener():
    return urllib.request.build_opener(urllib.request.ProxyHandler({}))


def get_json(uri):
    with opener().open(API_ROOT + uri, timeout=10) as resp:
        return json.load(resp)


def verify_ollama_live():
    version = get_json("/api/version").get("version")
    tags = get_json("/api/tags").get("models", [])
    matches = [m for m in tags if m.get("name") == NAME]
    if version != MODEL_VERSION or len(matches) != 1 or matches[0].get("digest") != DIGEST:
        raise IntegrityError(f"Local environment changed: version={version}, digest={[m.get('digest') for m in matches]}")
    return {"ollama_version": version, "model_name": NAME, "model_digest": DIGEST}


def verify_freeze(folder):
    manifest_path = folder / "freeze_manifest_v0_1.json"
    if not manifest_path.exists():
        raise IntegrityError("Not frozen: freeze_manifest_v0_1.json missing")
    manifest = load_json_file(manifest_path)
    if manifest.get("status") != "FROZEN" or manifest.get("model_digest") != DIGEST:
        raise IntegrityError("Freeze manifest status or model digest mismatch")
    expected = check_files(folder, include_runner=True)
    if manifest.get("input_file_sha256") != expected:
        raise IntegrityError("Freeze manifest file hashes do not match")
    return digest(manifest_path.read_bytes())


def build_request(contract, case, one_pass):
    # This is the sole place where case text is sent to the model.
    prompt = contract["prompt_template"].format(evidence=case["evidence"], claim=case["claim"])
    payload = {
        "model": contract["model"],
        "prompt": prompt,
        "stream": contract["request"]["stream"],
        "think": contract["request"]["think"],
        "format": contract["request"]["format"],
        "options": {**contract["request"]["options_common"], "seed": one_pass["seed"]},
    }
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def do_http(request_bytes):
    req = urllib.request.Request(
        API_ROOT + "/api/generate",
        data=request_bytes,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with opener().open(req, timeout=120) as response:
        return response.status, response.read()


def retryable(exc):
    if isinstance(exc, urllib.error.HTTPError):
        return exc.code in (502, 503, 504)
    return isinstance(exc, (urllib.error.URLError, TimeoutError, socket.timeout, ConnectionError))


def send_with_receipts(body, case_id, one_pass, events_path, send_once=do_http):
    for attempt in (1, 2):
        rid = f"{case_id}:{one_pass['id']}:{attempt}"
        append_event(events_path, {
            "event": "ATTEMPT_START", "at_utc": utc_now(), "attempt_id": rid,
            "case_id": case_id, "pass_id": one_pass["id"], "seed": one_pass["seed"],
            "request_sha256": digest(body), "request_bytes_base64": base64.b64encode(body).decode("ascii"),
        })
        try:
            status, raw = send_once(body)
        except Exception as exc:
            retriable = retryable(exc)
            append_event(events_path, {
                "event": "REQUEST_ERROR", "at_utc": utc_now(), "attempt_id": rid,
                "error_type": type(exc).__name__, "error": str(exc),
                "transport_retry_eligible": retriable,
            })
            if retriable and attempt == 1:
                continue
            raise TransportFailure(f"{rid}: {type(exc).__name__}: {exc}") from exc
        append_event(events_path, {
            "event": "HTTP_RESPONSE", "at_utc": utc_now(), "attempt_id": rid,
            "http_status": status, "response_sha256": digest(raw),
            "response_bytes_base64": base64.b64encode(raw).decode("ascii"),
        })
        if status != 200:
            raise IntegrityError(f"Unexpected HTTP status {status} at {rid}")
        try:
            packet = json.loads(raw.decode("utf-8"))
        except (UnicodeError, ValueError) as exc:
            raise IntegrityError(f"Invalid API JSON envelope at {rid}: {exc}") from exc
        if not isinstance(packet, dict) or not isinstance(packet.get("response"), str) or packet.get("done") is not True:
            raise IntegrityError(f"Incomplete or invalid API envelope at {rid}")
        return packet["response"]
    raise RuntimeError("Unreachable retry state")


def run(folder):
    now = datetime.now(timezone.utc)
    if not VALID_DATES[0] <= now.date() <= VALID_DATES[1]:
        raise IntegrityError("Main run allowed only 2-15 November 2026 (UTC)")
    ds, c, env = load_inputs(folder)
    manifest_sha = verify_freeze(folder)
    live = verify_ollama_live()
    folder_runs = folder / "runs"
    folder_runs.mkdir(exist_ok=True)
    run_folder = folder_runs / ("run_" + now.strftime("%Y%m%dT%H%M%S%fZ"))
    run_folder.mkdir(exist_ok=False)
    events = run_folder / "attempt_events.jsonl"
    final = run_folder / "final_responses.jsonl"
    status_path = run_folder / "run_status.json"
    metadata = {
        "status": "RUNNING", "created_at_utc": utc_now(),
        "freeze_manifest_sha256": manifest_sha,
        "dataset_sha256": EXPECTED["main_dataset_45_v0_2_REVIEW.json"],
        "contract_sha256": EXPECTED["model_contract_v0_1_REVIEW.json"],
        "runner_sha256": digest(Path(__file__).read_bytes()),
        "model_environment": live, "expected_final_records": 90, "final_records": 0,
        "notes": "No restart/resume; preserve partial runs for audit",
    }
    atomic_json(status_path, metadata)
    try:
        for one_pass in c["passes"]:
            for case in ds:
                body = build_request(c, case, one_pass)
                text = send_with_receipts(body, case["id"], one_pass, events)
                append_event(final, {
                    "case_id": case["id"], "pass_id": one_pass["id"],
                    "seed": one_pass["seed"], "transport_ok": True,
                    "response_text": text,
                })
                metadata["final_records"] += 1
                print(f"RECORDED {metadata['final_records']:02d}/90: {case['id']} pass {one_pass['id']}", flush=True)
        metadata["status"] = "COMPLETE_UNSCORED"
    except Exception as exc:
        metadata["status"] = "INCONCLUSIVE_INTERRUPTED"
        metadata["error_type"] = type(exc).__name__
        metadata["error"] = str(exc)
        append_event(events, {"event": "RUN_STOP", "at_utc": utc_now(),
                              "error_type": type(exc).__name__, "error": str(exc)})
        raise
    finally:
        metadata["completed_or_stopped_at_utc"] = utc_now()
        metadata["attempt_events_sha256"] = digest(events.read_bytes()) if events.exists() else None
        metadata["final_responses_sha256"] = digest(final.read_bytes()) if final.exists() else None
        atomic_json(status_path, metadata)
        print("RUN DIRECTORY:", run_folder, flush=True)
        print("STATUS:", metadata["status"], flush=True)


def self_test():
    # No Ollama requests; only in-memory mocked responses, with temporary receipts.
    contract = {
        "model": NAME,
        "request": {"stream": False, "think": False,
                    "options_common": {"temperature": 0.2, "num_ctx": 2048, "num_predict": 64},
                    "format": {"type": "object", "properties": {"label": {"type": "string", "enum": ["SUPPORTED"]}},
                               "required": ["label"], "additionalProperties": False}},
        "prompt_template": "EVIDENCE:\n{evidence}\nCLAIM:\n{claim}",
    }
    record = {"evidence": "Sample E", "claim": "Sample C", "reference_label": "MUST_NOT_LEAK",
              "reference_rationale": "ALSO_MUST_NOT_LEAK"}
    a = {"id": "A", "seed": 101}
    b = build_request(contract, record, a)
    payload = json.loads(b)
    assert "MUST_NOT_LEAK" not in b.decode() and "ALSO_MUST_NOT_LEAK" not in b.decode()
    assert payload["options"]["seed"] == 101 and payload["prompt"] == "EVIDENCE:\nSample E\nCLAIM:\nSample C"
    print("TEST 1: payload and reference-label exclusion PASS")

    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "events.jsonl"
        seen = []
        def fake_retry(body):
            seen.append(body)
            if len(seen) == 1:
                raise urllib.error.URLError("mock connection reset")
            return 200, b'{"response":"{\\"label\\":\\"SUPPORTED\\"}","done":true}'
        text = send_with_receipts(b, "CAL-TEST", a, path, fake_retry)
        events = [json.loads(line) for line in path.read_text().splitlines()]
        assert len(seen) == 2 and seen[0] == seen[1] and text == '{"label":"SUPPORTED"}'
        assert [x["event"] for x in events] == ["ATTEMPT_START", "REQUEST_ERROR", "ATTEMPT_START", "HTTP_RESPONSE"]
        assert base64.b64decode(events[-1]["response_bytes_base64"]).startswith(b'{"response"')
        print("TEST 2: exact-byte retry and raw receipts PASS")

        attempts = []
        def always_fails(body):
            attempts.append(body)
            raise urllib.error.URLError("mock down")
        try:
            send_with_receipts(b, "CAL-TEST2", a, path, always_fails)
            raise AssertionError("Expected failure")
        except TransportFailure:
            assert len(attempts) == 2
        print("TEST 3: stop after one transport retry PASS")

        bad_calls = []
        def bad_envelope(body):
            bad_calls.append(body)
            return 200, b'{"response": 4, "done": true}'
        try:
            send_with_receipts(b, "CAL-TEST3", a, path, bad_envelope)
            raise AssertionError("Expected integrity failure")
        except IntegrityError:
            assert len(bad_calls) == 1
        print("TEST 4: malformed API envelope stops without retry PASS")

        calls = []
        def bad_request(body):
            calls.append(body)
            raise urllib.error.HTTPError(API_ROOT, 400, "bad request", {}, None)
        try:
            send_with_receipts(b, "CAL-TEST4", a, path, bad_request)
            raise AssertionError("Expected stop")
        except TransportFailure:
            assert len(calls) == 1
        print("TEST 5: HTTP 400 never retried PASS")

    print("RESULT: RUNNER SELF-TEST 5/5 PASS (NO MODEL CALLS)")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--self-test", action="store_true")
    action.add_argument("--preflight", action="store_true")
    action.add_argument("--run", action="store_true")
    parser.add_argument("--confirm-frozen-run", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    folder = Path(__file__).resolve().parent
    if args.preflight:
        load_inputs(folder)
        live = verify_ollama_live()
        print("RESULT: INPUTS + LOCAL MODEL PREFLIGHT PASS")
        print("MODEL:", live["model_name"])
        print("DIGEST:", live["model_digest"])
        print("MAIN MODEL GENERATION CALLS: 0")
        print("FREEZE MANIFEST:", "PRESENT" if (folder / "freeze_manifest_v0_1.json").exists() else "NOT YET CREATED")
        return
    if not args.confirm_frozen_run:
        raise SystemExit("STOP: --run requires --confirm-frozen-run")
    run(folder)


if __name__ == "__main__":
    try:
        main()
    except (IntegrityError, TransportFailure, urllib.error.URLError, OSError, ValueError) as exc:
        raise SystemExit(f"STOP: {exc}")
