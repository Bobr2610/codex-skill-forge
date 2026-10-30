# MVP Verification Checklist

Link each row to Jira acceptance criteria and retain concise, attributable evidence.

| Area | Check/evidence | Owner | Gate | Status/link |
|---|---|---|---|---|
| Requirements | Each MVP requirement maps to acceptance criteria and verification | | | |
| Test-first gate | Each Jira task has acceptance checks before work; code tests have valid red evidence before implementation | | | |
| Architecture | Dependencies respect approved module boundaries | | | |
| Naming | Glossary and naming contract followed; exceptions recorded | | | |
| Static quality | Formatter/linter/type checks from project config | | | |
| Unit | Domain rules and edge cases | | | |
| Integration | Persistence and external adapters, error paths | | | |
| API/UI | Contract, responsive states, accessibility target | | | |
| Security | Authz, input validation, secret/data handling | | | |
| Operations | Logging, health, configuration, backup/restore where applicable | | | |
| Acceptance | User-visible MVP flow passes agreed criteria | | | |
| Release | Rollback/known limitations and release approval | | | |

## Task evidence record
Use `records/tasks/<JIRA-KEY>.json` in the generated skill repository copied from `task-record-code.json` or `task-record-non-code.json`. Do not duplicate full CI logs; link authoritative output. Do not write verification records into the product repository unless an explicitly owned Jira task calls for that documentation there.
