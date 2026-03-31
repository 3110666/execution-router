# Execution Policy

## Default Order

Always prefer:

`rule/config -> script -> skill -> agent`

## Definitions

### Rule or Config

Use when the task is already solved by:

- a repository rule
- a template
- a fixed configuration
- a documented command with no meaningful branching

### Script

Use when:

- the inputs and outputs are clear
- the steps are predictable
- the task is repeatable
- success can be checked mechanically

### Skill

Use when:

- the workflow is mostly stable
- bounded judgment is still needed
- repo or domain guidance matters
- the task benefits from bundled scripts, references, or templates

### Agent

Use only when:

- the goal is known but the path is unclear
- exploration may change the plan
- intermediate results determine the next step

## Mandatory Questions Before Agent Escalation

1. Can an existing rule, template, or config solve this?
2. Can a deterministic script solve this?
3. Can an existing skill cover most of the workflow?
4. What uncertainty remains?
5. What exact output must the agent return?

## Promotion Rule

- Repeated successful agent work should be promoted downward.
- Prefer `script` for fixed execution.
- Prefer `skill` for stable workflows with bounded judgment.
- Keep `agent` for exploration and exceptions.
