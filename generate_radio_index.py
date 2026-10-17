from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from pathlib import Path

REPOSITORY = "LEDERG777-TEXNARIC/LEDERG-radio-crmp"
BRANCH = "main"
SUPPORTED_AUDIO_SUFFIXES = {".mp3", ".ogg", ".wav"}
MAX_TRACK_BYTES = 100_000_000
ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "radio-index.json"


def _git_blob_sha(path: Path) -> str:
    size = path.stat().st_size
    digest = hashlib.sha1(f"blob {size}\0".encode("ascii"))
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _valid_station_name(name: str) -> bool:
    if not name or name in {".", ".."} or len(name) > 48:
        return False
    if name.startswith(".") or any(char in name for char in '\\/:*?"<>|'):
        return False
    stem = name.split(".", 1)[0].casefold()
    if stem in {"con", "prn", "aux", "nul"} or re.fullmatch(r"(com|lpt)[1-9]", stem):
        return False
    return True


def build_index(root: Path = ROOT) -> dict:
    root = Path(root).resolve()
    if not root.is_dir():
        raise FileNotFoundError(f"Radio repository root does not exist: {root}")

    station_dirs = sorted(
        (
            entry for entry in root.iterdir()
            if (
                entry.is_dir()
                and not entry.is_symlink()
                and not entry.name.startswith(".")
                and entry.name.casefold() not in {"__pycache__"}
            )
        ),
        key=lambda entry: entry.name.casefold(),
    )
    stations = []
    seen_stations = {}
    files = []
    seen_paths = set()

    for station_dir in station_dirs:
        station = station_dir.name
        if not _valid_station_name(station):
            raise ValueError(f"Invalid station folder name: {station!r}")
        key = station.casefold()
        if key in seen_stations and seen_stations[key] != station:
            raise ValueError(
                f"Station folder names collide on Windows: {seen_stations[key]!r} and {station!r}"
            )
        seen_stations[key] = station
        stations.append(station)

        for track in sorted(station_dir.iterdir(), key=lambda entry: entry.name.casefold()):
            if not track.is_file() or track.is_symlink():
                continue
            if track.suffix.casefold() not in SUPPORTED_AUDIO_SUFFIXES:
                continue
            if not track.name or track.name.startswith(".") or any(char in track.name for char in '\\/:*?"<>|'):
                raise ValueError(f"Invalid audio filename: {track.name!r}")
            relative = f"{station}/{track.name}"
            path_key = relative.casefold()
            if path_key in seen_paths:
                raise ValueError(f"Duplicate case-insensitive track path: {relative}")
            seen_paths.add(path_key)
            size = track.stat().st_size
            if size <= 0 or size > MAX_TRACK_BYTES:
                raise ValueError(
                    f"Track must be between 1 byte and 100 MiB for GitHub distribution: {relative}"
                )
            files.append({
                "path": relative,
                "station": station,
                "size": size,
                "sha": _git_blob_sha(track),
            })

    files.sort(key=lambda item: item["path"].casefold())
    canonical = {"stations": stations, "files": files}
    fingerprint = hashlib.sha256(
        json.dumps(canonical, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")
    ).hexdigest()
    return {
        "schema": 1,
        "repository": REPOSITORY,
        "branch": BRANCH,
        "fingerprint": fingerprint,
        "stations": stations,
        "files": files,
    }


def main() -> int:
    try:
        payload = build_index()
        rendered = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        if OUTPUT.is_file() and OUTPUT.read_text(encoding="utf-8") == rendered:
            print(f"Radio index unchanged: {len(payload['stations'])} folders, {len(payload['files'])} tracks")
            return 0
        temporary = OUTPUT.with_name(OUTPUT.name + ".tmp")
        temporary.write_text(rendered, encoding="utf-8")
        os.replace(temporary, OUTPUT)
        print(
            f"Radio index updated: {len(payload['stations'])} folders, "
            f"{len(payload['files'])} tracks, fingerprint={payload['fingerprint']}"
        )
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
