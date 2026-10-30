# Project-Specific Codex Skill

This repository is a generated Codex skill, separate from the product source repository. It adapts the shared Codex Project Ops guidance to approved project requirements.

## Usage
- Read `versions/CURRENT.md` and the active version it names at the start of each project skill task.
- Keep only project-specific terminology, constraints, approved patterns, tool choices, and operational requirements here; link canonical plans/architecture/Jira instead of duplicating them.
- When requirements change, first record the requirement and impact in canonical requirements/change records. Draft an overlay proposal with Jira change key, conflict analysis, exact proposed instruction, and approver.
- Apply a proposal only after explicit project-owner approval through a reviewed PR in this generated skill repository.
- Version updates are additive, preserve previous approved versions, and update `versions/CURRENT.md`; never edit the shared generator or overwrite a prior version.
- Reconcile the project overlay against changed requirements at each phase gate. Flag stale or conflicting instructions for owner resolution; do not silently reinterpret approved baselines.
- Keep documentation concise and canonical. Link Jira, CI, design, and decision evidence instead of copying it. Before removing generated review scratch files, list exact paths and reasons, check they are agent-created and unused, and obtain approval; preserve private references, source, approved records, and final evidence.

## Files
- `versions/CURRENT.md`: pointer to the active overlay version.
- `versions/vNNNN.md`: immutable, approved project-specific instructions.
- `records/changes/<JIRA-KEY>-proposal.md`: pending or applied change proposal and approval record.
- `records/`: canonical project plans, Jira links, decisions, KPIs, phase evidence, and release records; keep product-source files untouched.
- `.private/<member-id>/references/`: Git-ignored personal task references; never store secrets or full copied manuals.
