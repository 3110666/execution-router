from __future__ import annotations

import argparse
import re
from pathlib import Path


def normalize_name(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.strip().lower())
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    if not slug:
        raise ValueError("Skill name must contain at least one letter or digit.")
    return slug


def to_title(value: str) -> str:
    return " ".join(part.capitalize() for part in value.split("-"))


def build_skill_md(name: str, description: str) -> str:
    return f'''---
name: {name}
description: {description}
---

# {to_title(name)}

## Purpose

Use this skill when:

- the workflow is mostly stable
- bounded judgment is still needed
- scripts, references, or templates should be bundled together

## Workflow

1. Read the user request and identify the expected output.
2. Check whether an existing rule or script is already enough.
3. Read `references/workflow.md` before starting substantial work.
4. Use bundled scripts and templates where they reduce repeated work.
5. Keep project-specific details out of the skill unless they are essential.

## Bundled Resources

- `references/workflow.md`
- `scripts/run_task.py`
- `templates/task-intake.md`
'''


def build_openai_yaml(display_name: str, short_description: str, default_prompt: str) -> str:
    return f'''interface:
  display_name: "{display_name}"
  short_description: "{short_description}"
  default_prompt: "{default_prompt}"

policy:
  allow_implicit_invocation: false
'''


def build_workflow_reference(name: str, description: str) -> str:
    return f"""# Workflow

## Goal

- Skill: `{name}`
- Description: {description}

## What To Customize

- Replace the default workflow steps with task-specific guidance.
- Add domain-specific references only when they are truly needed.
- Keep `SKILL.md` concise and move detailed material into `references/`.

## Suggested Next Steps

1. Clarify the exact use cases for this skill.
2. Replace the placeholder script if deterministic tooling is needed.
3. Replace the intake template with task-specific fields if useful.
"""


def build_task_script(name: str) -> str:
    return f'''from __future__ import annotations


def main() -> None:
    print("TODO: Replace this placeholder with deterministic tooling for {name}.")


if __name__ == "__main__":
    main()
'''


def build_template() -> str:
    return """# Task Intake

## Request

- User request:
- Expected output:

## Constraints

- Known inputs:
- Known risks:
- Validation plan:
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create a starter skill scaffold that can be edited into a reusable skill."
    )
    parser.add_argument("name", help="Human-readable skill name.")
    parser.add_argument(
        "--description",
        required=True,
        help="One-sentence description for SKILL.md frontmatter.",
    )
    parser.add_argument(
        "--display-name",
        help="Optional UI display name. Defaults to the title-cased skill name.",
    )
    parser.add_argument(
        "--short-description",
        help="Optional short description for openai.yaml.",
    )
    parser.add_argument(
        "--default-prompt",
        help="Optional default prompt for openai.yaml.",
    )
    parser.add_argument(
        "--output-dir",
        default="generated/skills",
        help="Directory where the new skill folder should be created.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite an existing scaffold if it already exists.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the files that would be created without writing them.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    name = normalize_name(args.name)
    display_name = args.display_name or to_title(name)
    short_description = args.short_description or args.description
    default_prompt = args.default_prompt or f"Use ${name} to handle this task."

    root = Path(args.output_dir) / name
    files = {
        root / "SKILL.md": build_skill_md(name, args.description),
        root / "agents" / "openai.yaml": build_openai_yaml(
            display_name=display_name,
            short_description=short_description,
            default_prompt=default_prompt,
        ),
        root / "references" / "workflow.md": build_workflow_reference(
            name=name,
            description=args.description,
        ),
        root / "scripts" / "run_task.py": build_task_script(name),
        root / "templates" / "task-intake.md": build_template(),
    }

    if args.dry_run:
        print(f"Target root: {root}")
        for path in files:
            print(path)
        return

    if root.exists() and not args.overwrite:
        raise FileExistsError(f"{root} already exists. Use --overwrite to replace it.")

    for path, content in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")

    print(f"Created skill scaffold: {root}")
    for path in files:
        print(f"- {path}")


if __name__ == "__main__":
    main()
