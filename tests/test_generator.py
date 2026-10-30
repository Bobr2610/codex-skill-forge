import json
import subprocess
from pathlib import Path

import pytest

from codex_skill_forge.generator import add_member_cache, generate_skill, generate_skill_draft, validate_generated_skill
from codex_skill_forge.inspection import OpsError, inspect


def run_git(path: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(path), *args], capture_output=True, text=True, check=True)
    return result.stdout.strip()


def test_inspection_reports_stack_without_mutating_source(tmp_path):
    (tmp_path / "pyproject.toml").write_text("[project]\nname='sample'\n", encoding="utf-8")
    before = sorted(path.relative_to(tmp_path).as_posix() for path in tmp_path.rglob("*"))
    facts = inspect(tmp_path)
    after = sorted(path.relative_to(tmp_path).as_posix() for path in tmp_path.rglob("*"))
    assert facts["stack"] == ["Python"]
    assert before == after


def test_generation_preview_and_rejection_write_nothing(tmp_path):
    source = tmp_path / "product"
    source.mkdir()
    (source / "package.json").write_text('{"name":"sample"}', encoding="utf-8")
    before = sorted(path.relative_to(source).as_posix() for path in source.rglob("*"))
    draft = generate_skill_draft(source, "alex", tmp_path / "sample-codex-skill")
    with pytest.raises(OpsError):
        generate_skill(draft, None)
    after = sorted(path.relative_to(source).as_posix() for path in source.rglob("*"))
    assert before == after
    assert not draft["output"].exists()


def test_generate_skill_is_separate_git_repo_with_private_ignore(tmp_path):
    source = tmp_path / "product"
    source.mkdir()
    (source / "pyproject.toml").write_text("[project]\nname='sample'\n", encoding="utf-8")
    source_snapshot = {path.relative_to(source).as_posix(): path.read_bytes() for path in source.rglob("*") if path.is_file()}
    draft = generate_skill_draft(source, "alex", tmp_path / "sample-codex-skill")
    result = generate_skill(draft, "GENERATE sample-codex-skill")
    output = Path(result["generated"])
    assert output != source
    assert (output / ".git").is_dir()
    assert run_git(output, "remote", "-v") == ""
    run_git(output, "config", "user.name", "Test User")
    run_git(output, "config", "user.email", "test@example.com")
    run_git(output, "commit", "--allow-empty", "-m", "initial skill snapshot")
    assert run_git(output, "check-ignore", ".private/alex/references/README.md")
    assert (output / "SKILL.md").is_file()
    assert validate_generated_skill(output, "alex")["valid"]
    assert sorted(path.relative_to(source).as_posix() for path in source.rglob("*")) == ["pyproject.toml"]
    assert {path.relative_to(source).as_posix(): path.read_bytes() for path in source.rglob("*") if path.is_file()} == source_snapshot


def test_generation_refuses_existing_and_nested_outputs(tmp_path):
    source = tmp_path / "product"
    source.mkdir()
    nested = source / "generated"
    with pytest.raises(OpsError):
        generate_skill_draft(source, "alex", nested)
    existing = tmp_path / "already-there"
    existing.mkdir()
    with pytest.raises(OpsError):
        generate_skill_draft(source, "alex", existing)


def test_skill_has_required_delivery_rules_and_member_specific_private_dir(tmp_path):
    source = tmp_path / "product"
    source.mkdir()
    draft = generate_skill_draft(source, "member-2", tmp_path / "product-codex-skill")
    skill = draft["files"]["SKILL.md"]
    assert "write tests first" in skill
    assert "official documentation" in skill
    assert "owner approval" in skill
    assert ".private/<member-id>/references/" in skill
    assert ".private/member-2/references/README.md" in draft["files"]
    assert ".private/\n" in draft["files"][".gitignore"]


def test_add_member_requires_approval_and_ignores_new_member_folder(tmp_path):
    source = tmp_path / "product"
    source.mkdir()
    draft = generate_skill_draft(source, "alex", tmp_path / "product-codex-skill")
    generate_skill(draft, "GENERATE product-codex-skill")
    with pytest.raises(OpsError):
        add_member_cache(draft["output"], "sam")
    result = add_member_cache(draft["output"], "sam", "ADD MEMBER sam")
    assert result["git_ignored"] == "true"
    assert run_git(draft["output"], "check-ignore", ".private/sam/references/README.md")


def test_validation_detects_unignored_private_path(tmp_path):
    source = tmp_path / "product"
    source.mkdir()
    draft = generate_skill_draft(source, "alex", tmp_path / "product-codex-skill")
    generate_skill(draft, "GENERATE product-codex-skill")
    skill = Path(draft["output"])
    (skill / ".gitignore").write_text("", encoding="utf-8")
    report = validate_generated_skill(skill, "alex")
    assert not report["valid"]
    assert any("not ignored" in error for error in report["errors"])


def test_generated_skill_profile_is_valid_json(tmp_path):
    source = tmp_path / "product"
    source.mkdir()
    draft = generate_skill_draft(source, "alex", tmp_path / "product-codex-skill")
    profile = json.loads(draft["files"]["references/project-profile.json"])
    assert profile["source_project"] == str(source.resolve())
    assert profile["git"]["remote_configured"] is False
