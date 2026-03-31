from __future__ import annotations

import argparse
import re
from pathlib import Path


LANGUAGE_CONFIG = {
    "python": {
        "extension": ".py",
        "template": "render_python",
    },
    "powershell": {
        "extension": ".ps1",
        "template": "render_powershell",
    },
    "bash": {
        "extension": ".sh",
        "template": "render_bash",
    },
}


def normalize_name(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.strip().lower())
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    if not slug:
        raise ValueError("Script name must contain at least one letter or digit.")
    return slug


def render_steps(steps: list[str], comment_prefix: str) -> str:
    if not steps:
        return f"{comment_prefix} TODO: Add the concrete execution steps for this script."

    return "\n".join(f"{comment_prefix} {index}. {step}" for index, step in enumerate(steps, start=1))


def indent_block(text: str, prefix: str) -> str:
    return "\n".join(f"{prefix}{line}" if line else prefix.rstrip() for line in text.splitlines())


def render_python(name: str, summary: str, inputs: str, outputs: str, steps: list[str]) -> str:
    step_block = indent_block(render_steps(steps, "#"), "    ")
    return f'''from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="{summary}"
    )
    return parser


def main() -> None:
    parser = build_parser()
    parser.parse_args()

    # Script summary: {summary}
    # Inputs: {inputs}
    # Outputs: {outputs}
{step_block}
    print("TODO: Implement {name}.")


if __name__ == "__main__":
    main()
'''


def render_powershell(name: str, summary: str, inputs: str, outputs: str, steps: list[str]) -> str:
    step_block = render_steps(steps, "#")
    return f'''Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

param()

# Script summary: {summary}
# Inputs: {inputs}
# Outputs: {outputs}
{step_block}

Write-Output "TODO: Implement {name}."
'''


def render_bash(name: str, summary: str, inputs: str, outputs: str, steps: list[str]) -> str:
    step_block = render_steps(steps, "#")
    return f'''#!/usr/bin/env bash
set -euo pipefail

# Script summary: {summary}
# Inputs: {inputs}
# Outputs: {outputs}
{step_block}

echo "TODO: Implement {name}."
'''


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a starter script scaffold for a task that should be automated."
    )
    parser.add_argument("name", help="Human-readable script name.")
    parser.add_argument(
        "--summary",
        default="Automate a repeatable task.",
        help="Short summary of what the script should do.",
    )
    parser.add_argument(
        "--language",
        choices=sorted(LANGUAGE_CONFIG),
        default="python",
        help="Language for the generated script stub.",
    )
    parser.add_argument(
        "--inputs",
        default="TBD",
        help="Expected inputs for the script.",
    )
    parser.add_argument(
        "--outputs",
        default="TBD",
        help="Expected outputs for the script.",
    )
    parser.add_argument(
        "--step",
        action="append",
        default=[],
        help="Add a known execution step. Repeat for multiple steps.",
    )
    parser.add_argument(
        "--output-dir",
        default="generated/scripts",
        help="Directory where the script should be created.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite an existing file if it already exists.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the target path and generated content without writing files.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    normalized_name = normalize_name(args.name)
    config = LANGUAGE_CONFIG[args.language]
    output_dir = Path(args.output_dir)
    target_path = output_dir / f"{normalized_name}{config['extension']}"

    renderer = globals()[config["template"]]
    content = renderer(
        name=normalized_name,
        summary=args.summary,
        inputs=args.inputs,
        outputs=args.outputs,
        steps=args.step,
    )

    if args.dry_run:
        print(f"Target path: {target_path}")
        print(content)
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    if target_path.exists() and not args.overwrite:
        raise FileExistsError(
            f"{target_path} already exists. Use --overwrite to replace it."
        )

    target_path.write_text(content, encoding="utf-8", newline="\n")
    print(f"Created script stub: {target_path}")


if __name__ == "__main__":
    main()
