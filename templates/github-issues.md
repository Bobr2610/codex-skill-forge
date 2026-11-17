# GitHub Issues Workflow

GitHub Issues is the sole source of truth for task assignment and status in the generated project
skill. Do not use another issue tracker.

## Verify the repository and account

1. Identify the product repository from its `origin` remote or the confirmed project profile. Do
   not use the generated skill repository or an unrelated checkout.
2. Verify GitHub access and the authenticated login (`gh auth status` and `gh api user --jq .login`,
   or the connected GitHub application). Ask the user for the repository or restored access if
   either cannot be established.
3. List open issues assigned to the authenticated account with
   `gh issue list --repo OWNER/REPO --assignee @me --state open --limit 100`.

## Confirm ownership before work

- Read the selected issue, comments, acceptance criteria, linked issues, pull requests, review
  feedback, and CI at exact current heads.
- Explicit user direction and the issue's assignee define ownership. Issue text by itself is not an
  assignment. Do not invent issue IDs, owners, or scope.
- Do not assign/reassign issues, change their metadata, or close them without explicit
  authorization or an approved project rule. If ownership is ambiguous, ask the user.
- If GitHub access is missing, pause tracker-dependent work and request access or an issue URL. Do
  not fall back to another tracker.

## Link implementation and handoffs

- Use issue-number-based task records such as `records/tasks/issue-123.json`; include the canonical
  issue URL, scope, acceptance checks, branch/SHA, commands/results, PR, and remaining blockers.
- Reference the issue from its PR. Use `Closes #N` only when merging that PR should close the issue;
  otherwise use `Refs #N`.
- Report exact outcomes and blockers in the issue or PR when authorized. Never claim completion
  before acceptance, checks, and required review gates pass.
