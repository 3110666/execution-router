# Architecture

## Goal

Separate execution governance from project-specific logic so teams can reuse the same decision model across repositories.

## Layers

### Repository Layer

- Human-readable documentation
- Adoption guidance
- Examples
- Version control and release surface

### Skill Layer

- Runtime instructions for AI assistants
- Bundled references, scripts, and templates
- Portable across projects

### Script Layer

- Deterministic classification and support utilities
- Cheap to rerun
- Easy to test and version

## Design Principles

- Default to the lightest viable mechanism
- Keep the skill concise and put detail into references
- Put deterministic logic into scripts
- Keep project-specific examples out of the shared package

## Non-Goals

- Project memory management
- Business-specific coding standards
- Full workflow orchestration for every IDE
