---
name: codex-skill-forge
description: Inspect a product repository read-only and generate a separate, versioned Codex project skill with evidence-based, test-first engineering, Jira coordination, architecture, tooling, and release rules.
---

# Codex Project Ops Skill Generator

This skill is an immutable generator baseline. Its only product-facing function is read-only inspection and generation of a separate, project-specific Codex skill repository. It must not operate the product repository, implement product code, create Jira issues, change product branches/releases, or write project overlays into the product repository. Skill instructions and CLI messages are English; generated skill content follows the user's requested language.

## Start
1. Read README.md and inspect the candidate product repository read-only using `codex-skill-forge inspect --project <repo>`.
2. Ask for a stable member identifier. Generate a sibling skill folder by default, preview all included files and detected project facts, then ask explicit approval to write. The default confirmation token is `GENERATE <folder-name>`.
3. Keep generator source and each generated project skill in separate local Git repositories with no remote configured. Never initialize or modify Git in the product repository. Explain that a local repository does not sync across devices; the owner configures shared storage or a remote.
4. Reject output paths equal to, nested inside, or containing the product source; refuse any pre-existing output path. Do not create `.projectops/` in the product repository or migrate/delete existing records.
5. Validate the generated skill structure and member-specific ignored cache using `codex-skill-forge validate-skill --skill <generated-skill> --member-id <id>`.
6. The generated skill, not this generator, is responsible for project plans, Jira, architecture, implementation, tests, Docker/tooling recommendations, and releases.

## Baseline immutability
This skill is the generic generator baseline, not the project's working skill. Do not adapt it in place per project. Only the owner may approve generator changes; each accepted change requires a version increment, changelog entry, tests, and a reviewed release. Project-specific adaptations belong in the generated sibling skill repository.
