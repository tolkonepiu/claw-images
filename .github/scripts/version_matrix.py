#!/usr/bin/env python3

import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
IMAGES_DIR = REPO_ROOT / "images"


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _matrix_rows(path: Path, data: dict[str, Any]) -> list[dict[str, str]]:
    source = data["source"]
    rows: list[dict[str, str]] = []
    for image in sorted(data["images"], key=lambda item: item["name"]):
        rows.append(
            {
                "config_name": path.stem,
                "images_file": str(path.relative_to(REPO_ROOT)),
                "version": data["version"],
                "source_repo": source["repo"],
                "source_tag": source["tag"],
                "image_name": image["name"],
                "dockerfile": image["dockerfile"],
            }
        )
    return rows


def build_matrix() -> list[dict[str, str]]:
    files = sorted(IMAGES_DIR.glob("*.json"), key=lambda item: item.name)
    if not files:
        raise ValueError("No images JSON files found in images/*.json")

    rows: list[dict[str, str]] = []

    for path in files:
        data = _load_json(path)
        rows.extend(_matrix_rows(path, data))

    return rows


def main() -> int:
    try:
        matrix = build_matrix()
    except ValueError as exc:
        print(str(exc))
        return 1

    print(json.dumps(matrix, separators=(",", ":"), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
