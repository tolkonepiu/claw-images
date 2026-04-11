#!/usr/bin/env python3

import argparse
import json
from pathlib import Path
from typing import Any

from matrix_common import format_args


REPO_ROOT = Path(__file__).resolve().parents[2]
OVERLAYS_DIR = REPO_ROOT / "overlays"


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--changed-files-json",
        help="JSON array of changed overlays/*.json paths relative to the repository root",
    )
    return parser.parse_args()


def _selected_files(changed_files_json: str | None) -> list[Path] | None:
    if changed_files_json is None:
        return None

    if changed_files_json.strip() == "":
        return []

    parsed = json.loads(changed_files_json)
    if not isinstance(parsed, list):
        raise ValueError("--changed-files-json must be a JSON array")

    changed_paths: list[Path] = []

    for raw_path in parsed:
        if not isinstance(raw_path, str):
            raise ValueError("--changed-files-json entries must be strings")

        candidate = (REPO_ROOT / raw_path).resolve()

        try:
            relative = candidate.relative_to(REPO_ROOT)
        except ValueError:
            continue

        if candidate in changed_paths:
            continue

        changed_paths.append(candidate)

    overlay_files = sorted(OVERLAYS_DIR.glob("*.json"), key=lambda item: item.name)
    files: list[Path] = []
    seen: set[Path] = set()

    for overlay_file in overlay_files:
        if not overlay_file.is_file():
            continue

        overlay_data = _load_json(overlay_file)
        context_path = (REPO_ROOT / overlay_data["overlay"]["context"]).resolve()
        dockerfile_path = (REPO_ROOT / overlay_data["overlay"]["dockerfile"]).resolve()

        for changed_path in changed_paths:
            if changed_path == overlay_file or changed_path == dockerfile_path:
                if overlay_file not in seen:
                    files.append(overlay_file)
                    seen.add(overlay_file)
                break

            if context_path.is_dir():
                try:
                    changed_path.relative_to(context_path)
                except ValueError:
                    continue

                if overlay_file not in seen:
                    files.append(overlay_file)
                    seen.add(overlay_file)
                break

    return sorted(files, key=lambda item: item.name)


def _matrix_row(path: Path, data: dict[str, Any]) -> dict[str, str]:
    overlay = data["overlay"]
    return {
        "overlay_file": str(path.relative_to(REPO_ROOT)),
        "image_name": data["name"],
        "version": data["version"],
        "source_image": data["source_image"],
        "dockerfile": overlay["dockerfile"],
        "context": overlay["context"],
        "args": format_args(overlay.get("args"), kind="overlay"),
    }


def build_matrix(changed_files_json: str | None = None) -> list[dict[str, str]]:
    files = _selected_files(changed_files_json)
    if files is None:
        files = sorted(OVERLAYS_DIR.glob("*.json"), key=lambda item: item.name)

    if changed_files_json is None and not files:
        raise ValueError("No overlay JSON files found in overlays/*.json")

    rows: list[dict[str, str]] = []

    for path in files:
        data = _load_json(path)
        rows.append(_matrix_row(path, data))

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
