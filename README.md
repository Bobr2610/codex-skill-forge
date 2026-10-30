# Codex Skill Forge — Project-Specific Codex Skill Generator

**A read-only project inspector and Codex skill generator. It creates a separate, project-tailored skill and local Git repository; it does not manage or modify the product project.**

## What it does
Codex Skill Forge is the immutable generic baseline. It inspects product project metadata read-only, then generates a sibling Codex skill with project-specific delivery instructions, reusable templates, and a personal ignored reference cache. The generated skill guides a separate team through project planning and delivery.

The package contains one discoverable generator skill in `SKILL.md` and a standard-library Python CLI. The CLI only inspects the source repository and creates/validates a distinct skill repository. It does not write into product repositories or create Jira issues, product branches, or releases.

## Capabilities
- Read-only inspection of stack manifests and existing project instructions.
- Generated Codex skill with project context, Waterfall/Jira, non-overlapping chat, architecture/naming, TDD, research, Docker/tooling, UI, release, and cleanup guidance.
- Separate local Git repositories for the immutable generator baseline and each generated project skill; no remotes configured by default.
- Git-ignored `.private/<member-id>/references/` cache for task-specific notes, with shared decisions kept tracked.
- Generated skill validation for Codex structure, local Git, and private-cache ignore rules.

## Quick start
Requires Python 3.11 or newer.

```powershell
python -m pip install -e .
codex-skill-forge inspect --project C:\path\to\product
codex-skill-forge generate-skill --project C:\path\to\product --member-id alex --approval "GENERATE product-codex-skill"
codex-skill-forge validate-skill --skill C:\path\to\skills\product-codex-skill --member-id alex
codex-skill-forge add-member --skill C:\path\to\skills\product-codex-skill --member-id sam
```

`generate-skill` inspects the product repository read-only, previews the generated file list, and writes only after the exact `GENERATE <folder-name>` approval token. It refuses nested or existing output paths. Existing product `.projectops/` records are not migrated or touched. The first member cache is created in the ignored folder before the generated skill's initial commit; additional member caches require explicit approval with `ADD MEMBER <id>`.

By default, the generated skill is a sibling of this package under `skills/`, outside the product repository. It gets a separate local Git repository without a remote. A local repository does not synchronize across devices; the owner configures a shared path or remote. Its `.private/` folder is ignored by Git and contains only member-specific task references; never place secrets there. Use `add-member` (approval token `ADD MEMBER <id>`) to create more isolated caches. Teammates use owned issue branches and reviewed PRs for shared skill changes.

## Test-first, research, and tool selection
The generated skill mandates acceptance checks before work, test-first red-green-refactor for code, cited current technical research, fit-based Docker/Compose recommendations, and explicit approval before project changes. These are project-team instructions, not operations performed by the generator.

## Quality and security
The runtime CLI uses Python's standard library; development tests use pytest. It reads source project metadata and does not request or store product credentials. Generated skills start local-only and must be explicitly shared by the owner.

Run the development checks:

```powershell
python -m pip install -e ".[dev]"
python -m pytest
python -m codex_skill_forge.cli --help
```

## Package structure
- `SKILL.md`: immutable generator instructions and safety boundaries.
- `src/codex_skill_forge/`: read-only inspector and skill generator CLI.
- `templates/`: templates copied into generated project skills.
- `tests/`: deterministic CLI-core tests.
- `SECURITY.md`, `CHANGELOG.md`, `LICENSE`: security policy, history, and owner-finalized proprietary license placeholder.

## License and support
This distribution contains a proprietary-license placeholder. The rights holder must finalize commercial terms, support commitments, and redistribution terms before sale. No warranty or support level is implied by this package.
