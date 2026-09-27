#!/usr/bin/env python3
"""Validate the PVZRH Mods catalog using only the Python standard library."""

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


CATALOG = Path(__file__).resolve().parents[1] / "catalog.json"
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
RELEASE_ASSET_RE = re.compile(r"^/[^/]+/[^/]+/releases/download/[^/]+/.+$")
REQUIRED = (
    "id", "name", "author", "description", "version", "game", "loader",
    "category", "downloadUrl", "sha256", "fileSize", "sourceUrl",
)


def https_url(value):
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def main():
    try:
        data = json.loads(CATALOG.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Cannot read catalog.json: {exc}", file=sys.stderr)
        return 1

    errors = []
    if not isinstance(data, dict):
        errors.append("top level must be an object")
    else:
        if data.get("schemaVersion") != 1:
            errors.append("schemaVersion must be 1")
        mods = data.get("mods")
        if not isinstance(mods, list):
            errors.append("mods must be an array")
            mods = []

        seen_ids = set()
        for index, mod in enumerate(mods):
            where = f"mods[{index}]"
            if not isinstance(mod, dict):
                errors.append(f"{where} must be an object")
                continue
            missing = [key for key in REQUIRED if key not in mod]
            if missing:
                errors.append(f"{where} is missing: {', '.join(missing)}")
                continue

            mod_id = mod["id"]
            if not isinstance(mod_id, str) or not ID_RE.fullmatch(mod_id):
                errors.append(f"{where}.id must be lowercase letters, digits, and hyphens")
            elif mod_id in seen_ids:
                errors.append(f"duplicate mod id: {mod_id}")
            seen_ids.add(mod_id)

            for key in ("name", "author", "description", "version", "game", "loader", "category"):
                if not isinstance(mod[key], str) or not mod[key].strip():
                    errors.append(f"{where}.{key} must be a non-empty string")

            digest = mod["sha256"]
            if not isinstance(digest, str) or not SHA_RE.fullmatch(digest):
                errors.append(f"{where}.sha256 must be 64 lowercase hexadecimal characters")

            size = mod["fileSize"]
            if isinstance(size, bool) or not isinstance(size, int) or size <= 0:
                errors.append(f"{where}.fileSize must be a positive integer")

            download = mod["downloadUrl"]
            if not isinstance(download, str) or not https_url(download):
                errors.append(f"{where}.downloadUrl must be an HTTPS URL")
            else:
                parsed = urlparse(download)
                if parsed.hostname not in ("github.com", "www.github.com") or not RELEASE_ASSET_RE.fullmatch(parsed.path):
                    errors.append(f"{where}.downloadUrl must be a direct GitHub Release asset URL")

            source = mod["sourceUrl"]
            if not isinstance(source, str) or not https_url(source):
                errors.append(f"{where}.sourceUrl must be an HTTPS URL")

    if errors:
        print("Catalog validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Catalog valid ({len(data['mods'])} mod entries).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
