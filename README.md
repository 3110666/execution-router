# execution-router

`execution-router` is a small open-source toolkit for routing work to the lightest useful execution mode:

`rule/config -> script -> skill -> agent`

It is built for teams that want lower token cost, better repeatability, and a clear escalation path before using agents.

## 中文简介

`execution-router` 是一套轻量的开源治理工具，用来把任务优先分流到最轻的可用执行方式：

`rule/config -> script -> skill -> agent`

它适合这类团队：

- 希望减少不必要的 agent 调用和 token 消耗
- 希望把高频任务沉淀为脚本或 skill
- 希望在真正需要动态规划时才升级到 agent

### 这套仓库包含什么

- 一个可复用的 skill：`skill/execution-router/`
- 一个确定性的任务分类脚本
- 一个用于说明是否需要 agent 的 intake 模板
- 一组轻量文档和示例，方便团队接入

### 核心原则

优先使用最便宜、最稳定、最可复用的执行层：

1. `rule/config`
2. `script`
3. `skill`
4. `agent`

其中 `agent` 是最后的升级层，不是默认入口。

### 什么时候该用什么

- `rule/config`：已有规则、模板或固定配置已经足够
- `script`：输入输出明确、步骤固定、可重复执行
- `skill`：流程大体稳定，但还需要边界内判断或领域指导
- `agent`：目标明确，但路径不清楚，需要探索和动态规划

### 快速使用

直接运行任务分类脚本：

```powershell
python skill/execution-router/scripts/task_router.py "批量整理 API 规范文件" --steps-fixed yes --repeatable yes --needs-judgment no --path-unclear no
```

把 `skill/execution-router/` 目录复制到你的技能目录后，就可以作为独立 skill 使用。

### 仓库结构

```text
execution-router/
  README.md
  LICENSE
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

### 适用边界

- 这是一个通用执行治理项目，不包含任何私有业务路径或内部仓库信息
- 项目专属 memory、业务规范、架构细节，应该放在消费方仓库里

## English Overview

`execution-router` helps teams route work to the lightest useful execution mode before reaching for an agent.

It is a good fit when you want to:

- reduce unnecessary agent calls and token cost
- turn repeated work into scripts or skills
- keep agent use focused on exploration and dynamic planning

### What this repo contains

- A reusable skill at `skill/execution-router/`
- A deterministic task classifier script
- A task intake template for justifying agent escalation
- Lightweight docs and examples for adoption

### Core model

Use the cheapest stable execution mode first:

1. `rule/config`
2. `script`
3. `skill`
4. `agent`

Agents are the last escalation layer, not the default engine.

### When to use each layer

- `rule/config`: an existing rule, template, or fixed configuration is already enough
- `script`: the task is deterministic, repeatable, and mechanically verifiable
- `skill`: the workflow is mostly stable, but still needs bounded judgment
- `agent`: the outcome is known, but the path must be discovered during execution

### Quick start

Run the router directly:

```powershell
python skill/execution-router/scripts/task_router.py "Batch normalize API specs" --steps-fixed yes --repeatable yes --needs-judgment no --path-unclear no
```

Install the skill by copying `skill/execution-router/` into your Codex skills directory or another compatible skills location.

### Public release status

This repository is ready for a first public release as `v0.1.0`.

The intended scope of `v0.1.0` is:

- a portable routing policy
- a reusable skill
- a deterministic router script
- a minimal adoption guide for teams

## Why execution-router?

There are already good skill ecosystems and agent-skill formats on GitHub, including:

- [openai/skills](https://github.com/openai/skills)
- [anthropics/skills](https://github.com/anthropics/skills)
- [vercel-labs/skills](https://github.com/vercel-labs/skills)
- [GitHub Copilot agent skills documentation](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/create-skills)

`execution-router` is different in scope.

It is not mainly a skill catalog, a packaging format, or a collection of domain capabilities.
It is a lightweight execution-governance layer for deciding what should happen before an agent is used.

In practice, that means:

- Not "which skill should we use?"
- But "should this task use a rule, a script, a skill, or an agent at all?"

### What makes it different

- It treats `agent` as the last escalation layer, not the default engine.
- It is designed to reduce token cost, not just expand assistant capability.
- It gives teams a deterministic precheck with a router script.
- It includes an intake template so agent escalation can be justified explicitly.
- It encourages promotion of repeated agent work into scripts or skills.
- It stays generic, so project-specific logic can live in consuming repositories.

### Use execution-router when

- your team is overusing agents for repeatable work
- you want a shared policy for script-vs-skill-vs-agent decisions
- you want successful agent workflows to become reusable assets
- you need a small governance layer that works across projects

### Do not use execution-router as

- a replacement for domain-specific skills
- a full agent framework
- a project memory system
- a business-specific workflow package

It works best as a thin decision layer placed before your existing scripts, skills, and agents.

## Links

- Architecture: `docs/architecture.md`
- Adoption guide: `docs/adoption-guide.md`
- Examples: `examples/example-requests.md`
- Skill entry: `skill/execution-router/SKILL.md`

## License

This project is released under the MIT License. See `LICENSE`.
