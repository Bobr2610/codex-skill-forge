from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any

from .inspection import OpsError, inspect, resolve_root, slugify


def _run_git(root: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(["git", "-C", str(root), *args], capture_output=True,
                            text=True, encoding="utf-8", errors="replace", check=False)
    if check and result.returncode:
        raise OpsError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout.strip()


def _safe_member_id(value: str) -> str:
    member = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip()).strip(".-_")[:48]
    if not member or member in {".", ".."}:
        raise OpsError("Member id must contain letters, digits, dots, underscores, or hyphens")
    return member


def generate_skill_draft(project_raw: str | Path, member_id: str, output_raw: str | Path | None = None) -> dict[str, Any]:
    project = resolve_root(project_raw)
    member = _safe_member_id(member_id)
    facts = inspect(project)
    package_root = Path(__file__).resolve().parents[2]
    default_output = package_root.parent / f"{slugify(project.name)}-codex-skill"
    output = Path(output_raw).expanduser().resolve() if output_raw else default_output.resolve()
    if output.exists():
        raise OpsError(f"Output already exists; refusing to overwrite: {output}")
    if output == project or project in output.parents or output in project.parents:
        raise OpsError("Generated skill output and source project must be separate, non-nested directories")
    template_root = package_root / "templates"
    project_slug = slugify(project.name)
    description = f"Project-specific Codex delivery instructions for {project.name}: test-first engineering, evidence-based decisions, Jira coordination, and release governance."
    skill_md = f'''---\nname: {project_slug}-project-skill\ndescription: {description}\n---\n\n# {project.name} Project Delivery\n\nThis generated skill is the project-specific operating contract. Read `project-context.md`, `references/project-profile.json`, and `references/coordination.md` before project work. This skill repository is separate from the product repository. Do not modify product code or product-repository configuration as part of skill administration.\n\n## Non-negotiable workflow\n1. Start with the Jira role roster and claim one issue. Record owner, bounded paths/deliverables, dependencies, acceptance checks, and handoff criteria. Separate Codex chats coordinate through Jira and reviewed changes; do not use subagents. Before asking to open another chat, explain its bounded role, why separation helps, and recommended model/reasoning level, then ask the user to choose or confirm.\n2. Research before material technical choices. Inspect project manifests and versions; consult current official documentation and primary sources. Summarize sources with URL, retrieval date, version, and applicability in the assigned member's ignored `.private/<member-id>/references/` folder. Do not copy full docs or store secrets. Promote only justified conclusions to tracked ADRs/project records.\n3. Define acceptance/verification checks before any work. For code, write tests first, run and record a valid red result caused by missing behavior, implement minimally to green, refactor, and rerun relevant gates. For non-code work, record measurable review checks and reviewer before starting.\n4. Follow the approved architecture, naming contract, stack/tool assessment, and requirements. Assess Docker/Compose, CI, DB/migrations, format/lint/type/security/observability tools against project fit. Do not add dependencies or infrastructure without owner approval.\n5. Keep canonical plans, decisions, risks, KPI definitions/evidence, gates, requirements, and release evidence concise and linked. New requirements require impact analysis and an approved versioned change to this skill.\n6. Run project verification, capture attributable evidence, update Jira, and hand off with changed paths, checks/results, decisions, blockers, and next action. Never claim a check that was not run.\n\n## Boundaries and Git workflow\n- This repository holds project-specific skill instructions, templates, decisions, and approved evidence only; application source remains in the separate product repository.\n- Never edit another member's `.private/<member-id>/` directory. `.private/` is Git-ignored; keep only task-relevant reference notes there. Shared conclusions must be proposed in a Jira-owned change and merged through reviewed PRs.\n- Use one task branch per Jira issue, explicit file ownership, and reviewed PRs. Protect the default/release branch; use the team's approved integration branch. Do not invent a remote: this repository starts local-only. The owner configures a shared path or Git remote for other devices.\n- Never silently change approved baselines. Record requirement, impact, alternatives, decision, approver/date, and links; create a new numbered skill version only after owner approval.\n- Keep generated documents in the user's requested language. Skill instructions remain English; conversation follows the user's language preference.\n\nRead `references/architecture.md`, `references/naming.md`, `references/test-first.md`, `references/tooling.md`, `references/research.md`, and `references/coordination.md` as relevant. Templates are in `templates/`.\n'''
    files: dict[str, str] = {
        "SKILL.md": skill_md,
        "README.md": f"# {project.name} Codex Project Skill\n\nProject-tailored Codex instructions generated by `codex-skill-forge`. This is a separate local Git repository; no remote is configured. Configure shared access explicitly for cross-device collaboration.\n\n- Source project (inspected read-only): `{project}`\n- Detected stack: {', '.join(facts['stack']) or 'not detected'}\n- Member reference cache: `.private/{member}/references/` (ignored by Git)\n- Shared project rules: `SKILL.md` and `references/`\n\nRead `SKILL.md` before project work. Keep only approved project-specific shared rules here.\n",
        "agents/openai.yaml": f"interface:\n  display_name: \"{project.name} Project Skill\"\n  short_description: \"Project-specific, test-first delivery guidance\"\n  default_prompt: \"Read this project skill, claim a bounded Jira task, and follow the approved evidence and test-first gates.\"\npolicy:\n  allow_implicit_invocation: true\n",
        "project-context.md": f"# Inspected Project Context\n\n- Project: {project.name}\n- Source path: `{project}`\n- Detected stacks: {', '.join(facts['stack']) or 'none detected'}\n- Manifests: {', '.join(facts['manifests']) or 'none detected'}\n- Existing agent instruction files: {', '.join(facts['agent_rules']) or 'none detected'}\n- Existing readmes: {', '.join(facts['readmes']) or 'none detected'}\n- Inspection mode: read-only\n- Generated: from the Codex Project Ops generator; review and approve project-specific baselines before use.\n",
        "references/project-profile.json": json.dumps({"schema_version": 1, "project_name": project.name,
            "source_project": str(project), "detected_stack": facts["stack"], "manifests": facts["manifests"],
            "existing_agent_rules": facts["agent_rules"], "existing_readmes": facts["readmes"],
            "jira_project_key": "", "project_owner": "", "team_members": [member],
            "git": {"default_branch": "", "integration_branch": "", "remote_configured": False}}, indent=2, ensure_ascii=False) + "\n",
        "references/coordination.md": (template_root / "project-skill.md").read_text(encoding="utf-8"),
        "references/architecture.md": (template_root / "architecture.md").read_text(encoding="utf-8"),
        "references/naming.md": (template_root / "naming.md").read_text(encoding="utf-8"),
        "references/test-first.md": (template_root / "test-first.md").read_text(encoding="utf-8"),
        "references/tooling.md": (template_root / "tooling-assessment.md").read_text(encoding="utf-8"),
        "references/research.md": (template_root / "research-policy.md").read_text(encoding="utf-8"),
        "references/sources.md": (package_root / "references.md").read_text(encoding="utf-8"),
        "references/plan.md": (template_root / "plan.md").read_text(encoding="utf-8"),
        "references/ui-rulebook.md": (template_root / "ui-rulebook.md").read_text(encoding="utf-8"),
        "references/verification-checklist.md": (template_root / "verification-checklist.md").read_text(encoding="utf-8"),
        "references/release-checklist.md": (template_root / "release-checklist.md").read_text(encoding="utf-8"),
        "references/roles.json": (template_root / "roles.json").read_text(encoding="utf-8"),
        "references/task-record-code.json": (template_root / "task-record-code.json").read_text(encoding="utf-8"),
        "references/task-record-non-code.json": (template_root / "task-record-non-code.json").read_text(encoding="utf-8"),
        "references/research-record.json": (template_root / "research-record.json").read_text(encoding="utf-8"),
        "references/release-notes-template.md": "# Release <version>\n\n- Jira issues:\n- User outcomes:\n- Verification evidence:\n- Known limitations:\n- Rollback/support owner:\n- Approval/date:\n",
        "records/requirements.md": "# Requirements and Acceptance\n\n| ID | Stakeholder/source | Requirement | Priority | Acceptance check | Owner | Jira | Status |\n|---|---|---|---|---|---|---|---|\n| | | | | | | | |\n",
        "records/architecture.md": (template_root / "architecture.md").read_text(encoding="utf-8"),
        "records/naming.md": (template_root / "naming.md").read_text(encoding="utf-8"),
        "records/tooling-assessment.md": (template_root / "tooling-assessment.md").read_text(encoding="utf-8"),
        "records/ui-rulebook.md": (template_root / "ui-rulebook.md").read_text(encoding="utf-8"),
        "records/verification-checklist.md": (template_root / "verification-checklist.md").read_text(encoding="utf-8"),
        "records/release-checklist.md": (template_root / "release-checklist.md").read_text(encoding="utf-8"),
        "records/decision-record.md": "# Decision <ID>\n\n- Status: proposed\n- Owner/approver/date:\n- Jira:\n\n## Context and evidence\n## Options and tradeoffs\n## Decision\n## Consequences\n## Sources\n",
        "records/changes/.keep": "Jira-keyed project skill change proposals.\n",
        "records/tasks/.keep": "Jira-linked test-first task records.\n",
        "records/research/.keep": "Shared canonical research decisions only.\n",
        "records/change-proposal-template.md": "# Skill Change Proposal <JIRA-KEY>\n\n- Status: pending approval\n- Owner:\n- Bounded files:\n\n## Requirement/source\n## Impact on scope, architecture, tests, schedule, risks, KPIs\n## Conflicts/options\n## Exact proposed instruction\n## Validation/evidence\n## Project-owner approval/date\n",
        "records/kpi-register.md": "# KPI Register\n\n| KPI | Definition/formula | Source | Baseline | Target/threshold | Owner | Cadence | Evidence | Jira |\n|---|---|---|---|---|---|---|---|---|\n| | | | | | | | | |\n",
        "records/handoff-template.md": "# Handoff <JIRA-KEY>\n\n- From/to/acknowledgement:\n- Scope and changed paths:\n- Checks and evidence:\n- Decisions:\n- Blockers/known gaps:\n- Next action:\n- Jira/PR links:\n",
        "records/README.md": "# Canonical Project Records\n\nStore concise project plans, architecture/ADRs, roles, risks, requirement changes, KPI evidence, gates, handoffs, acceptance, and releases here. Link Jira and CI evidence; avoid copying full Jira issues or logs. These records belong to the generated skill repository, not product source.\n",
        "versions/v0001.md": "# Project Skill Version v0001\n\nStatus: generated draft; project owner must approve before this becomes the project baseline.\n\n## Project instructions\n- Confirm requirements, roles, workflow, stack, security, data, architecture, and constraints before execution.\n- Preserve inspected product conventions unless an approved change says otherwise.\n- Keep project plans, architecture, decisions, KPIs, and delivery evidence in this generated skill repository; do not write into the product repository unless a stakeholder explicitly assigns a documentation change there.\n",
        "versions/CURRENT.md": "# Active Skill Version\n\nCurrent version: `v0001.md` (draft; owner approval required).\n",
        "versions/CHANGELOG.md": "# Project Skill Change History\n\n| Version | Jira change | Summary | Owner | Approval/date |\n|---|---|---|---|---|\n| v0001 | Initial generation | Draft project-specific overlay | | Pending |\n",
        ".gitignore": ".private/\n",
        "references/private-reference-policy.md": "# Private reference cache policy\n\n`.private/` is Git-ignored. Keep task-relevant reference notes only. Never store secrets or credentials. Do not edit another member's folder. Track source URL, retrieval date, version/applicability, and concise paraphrase. Put shared decisions in Jira-linked tracked records.\n",
        f".private/{member}/references/README.md": f"# Private references for {member}\n\nCache only sources needed by tasks owned by this member. Include source URL, retrieval date, version, and a brief paraphrase. Never store secrets or full copied manuals. Do not use this directory for shared decisions.\n",
    }
    return {"project": project, "output": output, "member_id": member, "facts": facts, "files": files}


def generate_skill(draft: dict[str, Any], approval: str | None = None) -> dict[str, Any]:
    target: Path = draft["output"]
    token = f"GENERATE {target.name}"
    if approval != token:
        raise OpsError(f"No files written. Review preview, then pass --approval '{token}'")
    if target.exists():
        raise OpsError(f"Output appeared after preview; refusing to overwrite: {target}")
    source = Path(draft["project"]).resolve()
    if target == source or source in target.parents or target in source.parents:
        raise OpsError("Generated skill output and source project must remain separate, non-nested directories")
    target.mkdir(parents=True, exist_ok=False)
    try:
        for relative, content in draft["files"].items():
            path = target / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("x", encoding="utf-8", newline="\n") as handle:
                handle.write(content)
        _run_git(target, "init", "--initial-branch=main")
        _run_git(target, "add", "--all")
        _run_git(target, "-c", "user.name=Codex Skill Forge", "-c", "user.email=codex-skill-forge@localhost",
                 "commit", "-m", "Generate project-specific Codex skill")
    except Exception:
        # Keep generated files available for inspection if local Git initialization fails.
        raise
    return {"generated": str(target), "files": len(draft["files"]), "git_initialized": True,
            "remotes": _run_git(target, "remote", "-v").splitlines(), "private_path": f".private/{draft['member_id']}/references"}


def validate_generated_skill(root_raw: str | Path, member_id: str) -> dict[str, Any]:
    root = resolve_root(root_raw)
    member = _safe_member_id(member_id)
    errors: list[str] = []
    required = ["SKILL.md", "agents/openai.yaml", "README.md", "project-context.md", "references/sources.md",
                "references/project-profile.json", "references/coordination.md",
                "versions/v0001.md", "versions/CURRENT.md", ".gitignore",
                f".private/{member}/references/README.md"]
    for relative in required:
        if not (root / relative).is_file():
            errors.append(f"Missing required generated-skill file: {relative}")
    git_dir = root / ".git"
    if not git_dir.exists():
        errors.append("Generated skill must have its own local Git repository")
    else:
        if _run_git(root, "remote", "-v"):
            errors.append("Generated skill unexpectedly has a Git remote")
        ignored = _run_git(root, "check-ignore", f".private/{member}/references/README.md", check=False)
        if not ignored:
            errors.append("Member reference cache is not ignored by Git")
    try:
        skill_text = (root / "SKILL.md").read_text(encoding="utf-8")
        match = re.match(r"(?s)^---\n(.*?)\n---\n", skill_text)
        if not match:
            errors.append("SKILL.md must begin with YAML frontmatter")
        else:
            name_match = re.search(r"(?m)^name:\s*([a-z0-9-]+)\s*$", match.group(1))
            description_match = re.search(r"(?m)^description:\s*(.+)$", match.group(1))
            if not name_match or len(name_match.group(1)) > 64:
                errors.append("SKILL.md frontmatter must contain a valid skill name of at most 64 characters")
            if not description_match:
                errors.append("SKILL.md frontmatter must contain a description")
        profile = json.loads((root / "references/project-profile.json").read_text(encoding="utf-8"))
        if not profile.get("project_name"):
            errors.append("Project profile must identify the inspected project")
    except (OSError, json.JSONDecodeError):
        errors.append("Project profile is missing or invalid JSON")
    return {"valid": not errors, "root": str(root), "member_id": member, "errors": errors,
            "git_initialized": git_dir.exists(), "remote_configured": bool(_run_git(root, "remote", "-v")) if git_dir.exists() else False}


def add_member_cache(root_raw: str | Path, member_id: str, approval: str | None = None) -> dict[str, str]:
    root = resolve_root(root_raw)
    member = _safe_member_id(member_id)
    if not (root / ".git").is_dir():
        raise OpsError("Target is not a generated skill Git repository")
    if ".private/" not in (root / ".gitignore").read_text(encoding="utf-8"):
        raise OpsError("Generated skill .gitignore must exclude .private/ before adding a member cache")
    path = root / ".private" / member / "references" / "README.md"
    token = f"ADD MEMBER {member}"
    if approval != token:
        raise OpsError(f"No files written. Review the private cache path, then pass --approval '{token}'")
    if path.exists():
        raise OpsError(f"Member cache already exists; refusing overwrite: {path}")
    path.parent.mkdir(parents=True, exist_ok=False)
    path.write_text(f"# Private references for {member}\n\nCache only source notes needed for Jira tasks owned by this member. Include source URL, retrieval date, version, and concise paraphrase. Never store secrets or full copied manuals. Do not edit another member's folder or use this cache for shared decisions.\n", encoding="utf-8", newline="\n")
    ignored = _run_git(root, "check-ignore", str(path.relative_to(root).as_posix()), check=False)
    if not ignored:
        path.unlink(missing_ok=True)
        raise OpsError("Git did not confirm that this private cache is ignored; removed the just-created file")
    return {"member_id": member, "private_path": str(path), "git_ignored": "true"}
