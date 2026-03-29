#!/usr/bin/env python3

import argparse
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
IMAGES_DIR = REPO_ROOT / "images"


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--changed-files-json",
        help="JSON array of changed images/*.json paths relative to the repository root",
    )
    return parser.parse_args()


def _selected_files(changed_files_json: str | None) -> list[Path] | None:
    if changed_files_json is None:
        return None

    parsed = json.loads(changed_files_json)
    if not isinstance(parsed, list):
        raise ValueError("--changed-files-json must be a JSON array")

    files: list[Path] = []
    seen: set[Path] = set()

    for raw_path in parsed:
        if not isinstance(raw_path, str):
            raise ValueError("--changed-files-json entries must be strings")

        candidate = (REPO_ROOT / raw_path).resolve()

        try:
            relative = candidate.relative_to(REPO_ROOT)
        except ValueError:
            continue

        if relative.parent != Path("images") or relative.suffix != ".json":
            continue

        if not candidate.is_file() or candidate in seen:
            continue

        files.append(candidate)
        seen.add(candidate)

    return sorted(files, key=lambda item: item.name)


def _matrix_rows(path: Path, data: dict[str, Any]) -> list[dict[str, str]]:
    source = data["source"]
    rows: list[dict[str, str]] = []
    for image in sorted(data["images"], key=lambda item: item["name"]):
        rows.append(
            {
                "images_file": str(path.relative_to(REPO_ROOT)),
                "version": data["version"],
                "source_repo": source["repo"],
                "source_tag": source["tag"],
                "image_name": image["name"],
                "dockerfile": image["dockerfile"],
            }
        )
    return rows


def build_matrix(changed_files_json: str | None = None) -> list[dict[str, str]]:
    files = _selected_files(changed_files_json)
    if files is None:
        files = sorted(IMAGES_DIR.glob("*.json"), key=lambda item: item.name)

    if changed_files_json is None and not files:
        raise ValueError("No images JSON files found in images/*.json")

    rows: list[dict[str, str]] = []

    for path in files:
        data = _load_json(path)
        rows.extend(_matrix_rows(path, data))

    return rows


def main() -> int:
    args = _parse_args()

    try:
        matrix = build_matrix(changed_files_json=args.changed_files_json)
    except ValueError as exc:
        print(str(exc))
        return 1

    print(json.dumps(matrix, separators=(",", ":"), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
