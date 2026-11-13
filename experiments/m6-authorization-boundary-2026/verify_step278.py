#!/usr/bin/env python3
"""Read-only checks for M6 Step 277/278 public record and (optional) private ZIP.

Does NOT load/run DLLs, install services, execute PowerShell, or change Windows policy.
Python 3.9+ standard library only.
"""
import argparse
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
INDEX = HERE / "PUBLIC_EVIDENCE_STEP278.json"


def sha256(data):
    return hashlib.sha256(data).hexdigest().upper()


def require(ok, message):
    if not ok:
        raise ValueError(message)


def load_index():
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    require(data["schema"] == "m6-step277-278-public-evidence-v1", "wrong public schema")
    digest = re.compile(r"^[0-9A-F]{64}$")
    require(bool(digest.fullmatch(data["private_zip"]["sha256"])), "invalid ZIP hash")
    items = data["entries"]
    names = [item["name"] for item in items]
    require(len(names) == 5 and len(set(names)) == 5, "five unique entries required")
    for item in items:
        require(bool(digest.fullmatch(item["sha256"])), "invalid member hash")
        require(isinstance(item["size_bytes"], int) and item["size_bytes"] >= 0,
                "invalid member length")
    hashes = {item["name"]: item["sha256"] for item in items}
    require(data["recorded"]["rebuilt_dll_sha256"] ==
            hashes["M6_STEP277_REBUILT_HOLD.dll"], "DLL hash disagreement")
    for source in data["original_source_hashes_reported"]:
        require(bool(digest.fullmatch(source["sha256"])), "invalid source hash")

    state = data["recorded"]
    require(state["cfc"] == "FROZEN" and state["m6"] == "HOLD", "unsafe state claim")
    require(state["e2e_gates_closed"] == 0 and state["e2e_gates_total"] == 6,
            "cannot claim E2E success")
    require(state["independent_authority"] == "NOT_ESTABLISHED",
            "cannot claim independent authority")
    require(state["positive_control_executed"] is False and
            state["approval_path_executed"] is False, "unexecuted paths misreported")
    require(state["byte_identical_to_historical_reference"] is False,
            "build mismatch omitted")
    require(data["disclosure"]["full_reproduction_from_public_repo_possible"] is False,
            "missing full reproduction limitation")
    print("PUBLIC_RECORD: PASS_WITH_LIMITATIONS")
    print("E2E: 0/6 OPEN")
    return data


def verify_archive(path, data):
    raw = path.read_bytes()
    require(sha256(raw) == data["private_zip"]["sha256"], "private ZIP SHA256 mismatch")
    expected = {item["name"]: item for item in data["entries"]}
    with zipfile.ZipFile(path, "r") as archive:
        members = archive.namelist()
        require(len(members) == len(expected) and set(members) == set(expected),
                "ZIP entry names/count differ from index")
        require(archive.testzip() is None, "ZIP CRC failure")
        for name, item in expected.items():
            payload = archive.read(name)
            require(len(payload) == item["size_bytes"], "size mismatch: " + name)
            require(sha256(payload) == item["sha256"], "SHA256 mismatch: " + name)

        # SHA256SUMS lists 4 payloads, not the manifest itself.
        manifest = archive.read("SHA256SUMS.txt").decode("utf-8")
        listed = {}
        for line in manifest.splitlines():
            if not line.strip():
                continue
            digest, name = line.strip().split(None, 1)
            require(name not in listed, "duplicate SHA256SUMS entry")
            listed[name] = digest
        require(set(listed) == set(expected) - {"SHA256SUMS.txt"},
                "SHA256SUMS names mismatch")
        for name, digest in listed.items():
            require(digest.upper() == expected[name]["sha256"],
                    "SHA256SUMS mismatch: " + name)

        evidence = json.loads(archive.read("evidence.json").decode("utf-8-sig"))
        r = data["recorded"]
        fields = {
            "step": "run_step",
            "test_id": "test_id",
            "build_exit_code": "compiler_exit_code",
            "built_dll_sha256": "rebuilt_dll_sha256",
            "historical_dll_reference_sha256": "historical_reference_sha256",
            "byte_identical_to_historical_reference": "byte_identical_to_historical_reference",
            "negative_control_result": "negative_control_result",
            "positive_control_executed": "positive_control_executed",
            "approval_path_executed": "approval_path_executed",
            "service_installed_or_started": "service_installed_or_started",
            "independent_authority": "independent_authority",
            "cfc": "cfc",
            "m6": "m6",
            "e2e_pass_count": "e2e_gates_closed",
            "e2e_total": "e2e_gates_total",
        }
        for raw_key, public_key in fields.items():
            require(evidence[raw_key] == r[public_key],
                    "operator record differs: " + raw_key)
        source_hashes = {s["name"]: s["sha256"]
                         for s in data["original_source_hashes_reported"]}
        require({s["name"]: s["sha256"] for s in evidence["original_sources"]}
                == source_hashes, "source-hash reports differ")
        compiler_output = archive.read("compiler_stdout.txt").decode("utf-8")
        require("warning CS0162" in compiler_output and "(145,13)" in compiler_output,
                "expected CS0162 warning missing")
        require(archive.read("compiler_stderr.txt") == b"", "compiler stderr not empty")

    print("PRIVATE_ARCHIVE: SHA256_AND_MEMBERS_PASS")
    print("OPERATOR_RECORD: PUBLIC_FIELDS_MATCH")
    print("SOURCE_EXECUTION: NOT_INDEPENDENTLY_REPRODUCED")
    print("E2E: 0/6 OPEN")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path,
                        help="Optional original private Step 278A ZIP; never executed")
    args = parser.parse_args()
    data = load_index()
    if args.archive is None:
        print("PRIVATE_ARCHIVE: NOT_SUPPLIED")
        print("SOURCE_EXECUTION: NOT_INDEPENDENTLY_REPRODUCED")
    else:
        verify_archive(args.archive, data)


if __name__ == "__main__":
    try:
        main()
    except (OSError, KeyError, ValueError, zipfile.BadZipFile) as exc:
        print("VERIFICATION_STOP: " + str(exc), file=sys.stderr)
        sys.exit(1)
