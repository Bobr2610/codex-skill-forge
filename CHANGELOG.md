# Changelog

All notable changes to this package are documented here.

## 1.3.0 - 2026-11-17
- Make GitHub Issues the only task tracker in generated project skills and surface that rule at the top of their instructions.
- Add reusable issue discovery and ownership guidance, plus user-visible coordinator and implementation chat workflow.
- Align generated record templates and metadata with GitHub Issues; preserve older release notes as historical records.

## 1.2.0 - 2026-10-30
- Renamed the Codex skill and Python distribution to Codex Skill Forge.
- Renamed the Python package and console command to `codex_skill_forge` / `codex-skill-forge`.
- Retained previous package history and behavior.

## 1.1.0 - 2026-10-30
- Corrected generated skill records and immutable version files to live in the generated skill repository, not in product source or template-only folders.
- Added approval-gated per-member private reference cache provisioning.
- Added standalone inspection module and retired legacy product-operation CLI/core modules.

## 1.0.0 - 2026-10-30
- Replaced product project operations with a read-only inspector and project-specific Codex skill generator.
- Added separate local Git repo generation, member-specific ignored reference cache, and generated skill validation.
- Retired CLI paths for Jira mutations, product branches/releases, product overlays, reports, and cleanup.
- Preserved project governance, test-first, research, Docker/tooling and architecture guidance inside generated skills.

## 0.3.0 - 2026-10-30
- Added test-first code and non-code acceptance gates, research record validation, Docker/tooling assessment, and versioned project-specific skill overlays.
- Expanded cleanup scope to registered, agent-created research scratchpads while keeping dry-run and approval safeguards.
- Expanded overlay validation and updated the end-to-end workflow guidance.

## 0.2.0 - 2026-10-30
- Expanded the skill into an end-to-end product brief-to-MVP workflow.
- Added architecture, naming, scaffold, verification, and release contracts/templates.
- Added read-only, heuristic `naming-check` CLI command.
- Added Codex skill discovery metadata and clarified preservation of existing project conventions.
- Removed the project-specific coordination archive so the workspace contains one general-purpose skill.
