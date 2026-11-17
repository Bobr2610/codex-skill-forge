---
name: {{PROJECT_SLUG}}-project-skill
description: {{DESCRIPTION}}
---

# Task tracking: GitHub Issues

**GitHub Issues is the sole task tracker for this project.** Use repository Issues for assignments,
scope, status, and handoffs. Do not use another issue tracker.

# {{PROJECT_NAME}} Project Delivery

This generated skill is the project-specific operating contract. Read `project-context.md`,
`references/project-profile.json`, and `references/coordination.md` before project work. This skill
repository is separate from the product repository. Do not modify product code or product-repository
configuration as part of skill administration.

## Non-negotiable workflow

1. Identify the product repository from its `origin` remote or the confirmed
   `references/project-profile.json`; verify GitHub access and the authenticated account. List issues
   assigned to that account and inspect the selected issue, comments, dependencies, related issues,
   pull requests, and checks before starting. Never invent an issue, assignee, repository, or
   assignment. See `references/github-issues.md`.
2. Confirm the task owner, bounded paths/deliverables, dependencies, acceptance checks, and handoff
   criteria. Do not self-assign, reassign others, change issue metadata, or close issues without
   explicit authorization or an approved project rule. If the assignment or GitHub access is
   ambiguous, ask the user; do not fall back to another tracker.
3. Research before material technical choices. Inspect project manifests and versions; consult
   current official documentation and primary sources. Summarize sources with URL, retrieval date,
   version, and applicability in the assigned member's ignored
   `.private/<member-id>/references/` folder. Do not copy full docs or store secrets. Promote only
   justified conclusions to tracked ADRs/project records.
4. Define acceptance/verification checks before work. For code, write tests first, run and record a
   valid red result caused by missing behavior, implement minimally to green, refactor, and rerun
   relevant gates. For non-code work, record measurable review checks and reviewer before starting.
5. Follow the approved architecture, naming contract, stack/tool assessment, and requirements.
   Assess Docker/Compose, CI, DB/migrations, format/lint/type/security/observability tools against
   project fit. Do not add dependencies or infrastructure without owner approval.
6. Keep canonical plans, decisions, risks, KPI definitions/evidence, gates, requirements, and
   release evidence concise and linked. New requirements require impact analysis and an approved
   versioned change to this skill.
7. Run project verification, capture attributable evidence, update the issue or PR when authorized,
   and hand off with changed paths, checks/results, decisions, blockers, and next action. Never
   claim a check that was not run.

## Coordinating work across Codex chats

- Keep a small, bounded change in one chat. For a large task with independent work streams, use one
  user-visible coordinator chat for direction, integrated planning, ownership boundaries,
  dependencies, and status. The coordinator does not implement product code.
- The coordinator decides the integrated plan first, then creates separate user-visible Codex
  implementation chats for substantial, non-overlapping slices. Do not use subagents or
  multi-agent delegation for this workflow.
- Each implementation chat starts by stating its concise plan and receives the exact issue URL,
  repository, branch/SHA baseline, bounded paths, dependencies, acceptance checks, and handoff
  owner. Assign a single writer for shared contracts and cross-service configuration.
- Implementation chats report issue/PR links, branch and SHA, checks, blockers, and next action to
  the coordinator. The coordinator reconciles status without duplicating implementation or losing
  the main objective.

## Boundaries and Git workflow

- This repository holds project-specific skill instructions, templates, decisions, and approved
  evidence only; application source remains in the separate product repository.
- Never edit another member's `.private/<member-id>/` directory. `.private/` is Git-ignored; keep
  only task-relevant reference notes there. Shared conclusions belong in issue-linked change
  proposals and reviewed PRs.
- Use one task branch per GitHub Issue, explicit file ownership, and reviewed PRs. Protect the
  default/release branch and use the team's approved integration branch. Do not invent a remote:
  this repository starts local-only. The owner configures a shared path or Git remote for other
  devices.
- Link PRs to issues with a non-closing reference unless the PR should close the issue after merge.
  Do not close issues before acceptance and review gates are met.
- Never silently change approved baselines. Record requirement, impact, alternatives, decision,
  approver/date, and links; create a new numbered skill version only after owner approval.
- Keep generated documents in the user's requested language. Skill instructions remain English;
  conversation follows the user's language preference.

Read `references/github-issues.md`, `references/architecture.md`, `references/naming.md`,
`references/test-first.md`, `references/tooling.md`, `references/research.md`, and
`references/coordination.md` as relevant. Templates are in `templates/`.
