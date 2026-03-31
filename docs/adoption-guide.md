# Adoption Guide

## Who This Is For

- Teams using AI coding assistants
- Repositories where repeated agent use is too expensive or too unstable
- Maintainers who want a reusable escalation policy

## Recommended Rollout

1. Publish this repository as `execution-router`.
2. Install the skill into the target environment.
3. Start using the router script for task intake.
4. Track repeated agent work and promote it into scripts or skill instructions.
5. Add project-local examples only in the consuming repository, not here.

## How To Adapt It Per Project

- Keep the shared routing policy here.
- Add repository-specific rules in the consuming project.
- Add project-only scripts or memory workflows outside this shared repo.

## Good First Integrations

- Add a short team rule: "Check script/skill before agent."
- Add the intake template to planning workflows.
- Use the router script in issue triage or task kickoff.

## When To Use An Agent Anyway

- The outcome is known, but the path is unclear.
- Exploration may change the plan.
- New information will affect the next step.
