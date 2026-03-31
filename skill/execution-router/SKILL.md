---
name: execution-router
description: Route work to rule/config, script, skill, or agent. Use when the user wants lower token usage, wants to avoid unnecessary agent work, or needs a repeatable way to decide whether a task should be automated, packaged as a skill, or escalated to an agent.
---

# Execution Router

Read [policy.md](./references/policy.md) first.

## Purpose

Use this skill to choose the lightest useful execution mode:

`rule/config -> script -> skill -> agent`

## Workflow

1. Start with the task goal and expected output.
2. Check whether an existing rule, template, or config is already enough.
3. If not, run `python scripts/task_router.py "<task description>" ...` when classification is unclear.
4. If the result is `script`, automate the task.
5. If the result is `skill`, package the reusable workflow and keep deterministic parts in scripts.
6. If the result is `agent`, write down the unresolved uncertainty before escalating.

## Use The Template

When the work might need an agent, fill out:

`templates/execution-intake-template.md`

This makes the escalation explicit and keeps repeated agent work visible for later promotion.

## Promotion Rule

- If the same kind of agent work succeeds 2 to 3 times, move it down a layer.
- Promote to `script` when the path is now fixed.
- Promote to `skill` when bounded judgment is still needed.

## Keep It Generic

- Put project-specific rules in the consuming repository.
- Keep this skill focused on routing and escalation logic.
- Do not mix in private paths, business terms, or internal repo structures.
