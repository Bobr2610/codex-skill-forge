# Security Policy

## Secrets
- Supply Jira/provider tokens through environment variables or an approved secret manager.
- Never put tokens in arguments, profiles, logs, prompts, issue descriptions, or commits.
- Redact authorization headers and sensitive response bodies.

## Destructive operations
- Jira bulk writes, protection changes, tags, and cleanup display a preview and require approval.
- Cleanup is manifest-scoped and limited to regular files below .projectops/review-temp/. Reject symlinks and path escapes.
- Protected branches cannot be deleted.

## Reporting
The MVP is pre-release. Report vulnerabilities privately to the package owner using the contact channel in the distribution listing. Do not publish exploit details.
