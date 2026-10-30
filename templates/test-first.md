# Test-First Task Workflow

Apply to every Jira task before implementation. For coding, use red-green-refactor. For project-management/design-only work, define measurable review checks before starting.

## Per-task gate
Create `records/tasks/<JIRA-KEY>.json` in the generated skill repository from the appropriate task template. Link it from the Jira issue; keep full test artifacts in the product repository's CI/test system and reference them rather than duplicating logs. Do not write a task ledger or tests into product source unless the Jira task explicitly assigns those product files.

### Code task
1. Confirm Jira owner, scope, non-overlapping file boundaries, dependencies, acceptance criteria, stack conventions, and approved architecture.
2. Write/extend a focused test for the required behavior. Record exact test path and command.
3. Run the test before implementation. Record output/evidence showing it fails because the requested behavior is missing (not because of an environment or test defect). Fix an invalid test or environment issue before proceeding; do not treat an unrelated failure as a valid red result.
4. Implement the smallest change that makes the test pass. Run the focused test and record green evidence.
5. Refactor only with green tests as safety; rerun the focused test and relevant suite, formatter, linter, type/security checks required by the project gates.
6. Record changed paths, commands, outcomes, CI/evidence links, and known gaps. Do not mark complete without passing acceptance criteria or an explicit approved exception.

### Non-code task
Before starting, specify observable acceptance checks, reviewer/approver, source of truth, review method, and evidence format. Record completion evidence against every check.

## Gate evidence
The generated skill repository holds the task gate record at `records/tasks/<JIRA-KEY>.json`; Jira links to it. Before implementation, the record must include measurable acceptance checks, test path and exact command, test-written evidence, and valid red evidence demonstrating the missing behavior. Completion requires green evidence and post-refactor checks when refactoring occurred. A record is evidence metadata only; it does not execute tests or prove claims. Review CI/test output directly before accepting the evidence.
