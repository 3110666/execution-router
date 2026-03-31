# execution-router

`execution-router` is a small open-source toolkit for routing work to the lightest useful execution mode:

`rule/config -> script -> skill -> agent`

It is designed for teams that want lower token cost, better repeatability, and a clear escalation path before using agents.

## What This Repo Contains

- A reusable skill at `skill/execution-router/`
- A deterministic task classifier script
- A task intake template for justifying agent escalation
- Lightweight docs and examples for adoption

## Repository Layout

```text
execution-router/
  README.md
  .gitignore
  docs/
    architecture.md
    adoption-guide.md
  examples/
    example-requests.md
  skill/
    execution-router/
      SKILL.md
      agents/
        openai.yaml
      scripts/
        task_router.py
      references/
        policy.md
      templates/
        execution-intake-template.md
```

## Core Idea

Use the cheapest stable execution mode first:

1. `rule/config`
2. `script`
3. `skill`
4. `agent`

Agents are the last escalation layer, not the default engine.

## Local Usage

Run the router directly:

```powershell
python skill/execution-router/scripts/task_router.py "Batch normalize API specs" --steps-fixed yes --repeatable yes --needs-judgment no --path-unclear no
```

Install the skill by copying `skill/execution-router/` into your Codex skills directory or another compatible skills location.

## Publishing To GitHub

This folder is already a standalone Git repository. After you create a remote GitHub repo named `execution-router`, run:

```powershell
cd D:\code\LMOP\execution-router
git remote add origin <your-github-repo-url>
git add .
git commit -m "Initial scaffold"
git push -u origin main
```

## Notes

- This scaffold is intentionally generic and does not contain LMOP-specific paths or business context.
- Choose and add a license before publishing if you want clear reuse terms.
