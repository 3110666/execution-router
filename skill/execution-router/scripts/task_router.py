from __future__ import annotations

import argparse
from dataclasses import dataclass


CHOICES = ("yes", "no")


@dataclass(frozen=True)
class Answers:
    description: str
    config_only: bool
    repeatable: bool
    steps_fixed: bool
    needs_judgment: bool
    path_unclear: bool


@dataclass(frozen=True)
class Recommendation:
    mode: str
    reason: str
    next_action: str


def yes_no(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized not in CHOICES:
        raise argparse.ArgumentTypeError(f"Expected one of {CHOICES}, got: {value}")
    return normalized == "yes"


def recommend(answers: Answers) -> Recommendation:
    if answers.config_only:
        return Recommendation(
            mode="rule/config",
            reason="The task can already be handled by an existing rule, template, or static configuration.",
            next_action="Apply or document the existing rule directly.",
        )

    if answers.path_unclear:
        return Recommendation(
            mode="agent",
            reason="The target is known, but the execution path still needs dynamic planning.",
            next_action="Write down the unresolved uncertainty and the exact output required before escalating.",
        )

    if answers.steps_fixed and answers.repeatable and not answers.needs_judgment:
        return Recommendation(
            mode="script",
            reason="The task is deterministic, repeatable, and can be verified mechanically.",
            next_action="Automate it with a script and make that script the default entry point.",
        )

    if answers.needs_judgment:
        return Recommendation(
            mode="skill",
            reason="The workflow is mostly stable, but still needs bounded judgment or reusable guidance.",
            next_action="Package the workflow as a skill and move deterministic steps into scripts.",
        )

    if answers.steps_fixed:
        return Recommendation(
            mode="script",
            reason="The execution path is already fixed even if the task is not yet frequent.",
            next_action="Start with a script so the work stays cheap and repeatable.",
        )

    return Recommendation(
        mode="skill",
        reason="The task does not need open-ended exploration, but it still benefits from reusable workflow guidance.",
        next_action="Capture the method as a skill and keep the remaining judgment explicit.",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Recommend whether a task should use rule/config, script, skill, or agent."
    )
    parser.add_argument("description", help="Short task description.")
    parser.add_argument(
        "--config-only",
        type=yes_no,
        choices=(True, False),
        default=False,
        metavar="yes|no",
        help="Use yes when an existing rule, template, or config is already enough.",
    )
    parser.add_argument(
        "--repeatable",
        type=yes_no,
        choices=(True, False),
        default=False,
        metavar="yes|no",
        help="Use yes when the task will likely be repeated.",
    )
    parser.add_argument(
        "--steps-fixed",
        type=yes_no,
        choices=(True, False),
        default=False,
        metavar="yes|no",
        help="Use yes when the execution steps are already predictable.",
    )
    parser.add_argument(
        "--needs-judgment",
        type=yes_no,
        choices=(True, False),
        default=False,
        metavar="yes|no",
        help="Use yes when bounded judgment is still part of the workflow.",
    )
    parser.add_argument(
        "--path-unclear",
        type=yes_no,
        choices=(True, False),
        default=False,
        metavar="yes|no",
        help="Use yes when the task path must be discovered during execution.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    parsed = parser.parse_args()

    answers = Answers(
        description=parsed.description,
        config_only=parsed.config_only,
        repeatable=parsed.repeatable,
        steps_fixed=parsed.steps_fixed,
        needs_judgment=parsed.needs_judgment,
        path_unclear=parsed.path_unclear,
    )
    recommendation = recommend(answers)

    print(f"Task: {answers.description}")
    print(f"Recommended mode: {recommendation.mode}")
    print(f"Reason: {recommendation.reason}")
    print(f"Next action: {recommendation.next_action}")


if __name__ == "__main__":
    main()
