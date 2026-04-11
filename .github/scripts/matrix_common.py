from typing import Any


def format_args(raw_args: Any, *, kind: str) -> str:
    if raw_args is None:
        return ""

    if not isinstance(raw_args, dict):
        raise ValueError(f"{kind} args must be a JSON object")

    lines: list[str] = []
    for key, value in raw_args.items():
        if not isinstance(key, str):
            raise ValueError(f"{kind} args keys must be strings")
        if "=" in key or "\n" in key or "\r" in key:
            raise ValueError(f"{kind} args keys must not contain '=', '\\n', or '\\r'")
        if not isinstance(value, str):
            raise ValueError(f"{kind} args values must be strings")
        if "\n" in value or "\r" in value:
            raise ValueError(f"{kind} args values must be single-line strings")
        lines.append(f"{key}={value}")

    return "\n".join(lines)
