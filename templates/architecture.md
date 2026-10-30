# Architecture Contract

Status: draft; project-owner approval required before baseline changes.

## Product and system context
- Product outcome and MVP boundary:
- Users and external systems:
- Constraints and quality attributes:

## Greenfield MVP default
Use a feature-first modular monolith, tailored to the chosen framework. Each feature owns its presentation adapter, application use cases, domain rules, infrastructure adapters, and tests where appropriate. Enforce inward dependency flow: presentation/infrastructure may depend on application/domain abstractions; domain logic must not depend on framework, database, or transport details. Keep deployment simple until evidence justifies distributed services.

## Proposed file map (replace with a concrete, stack-specific tree)
```text
project/
  src-or-app/
    features/
      <feature-name>/
        presentation/     # screens, controllers, route handlers, DTO mapping
        application/      # use cases, ports, orchestration
        domain/           # entities, value objects, invariants, domain services
        infrastructure/   # persistence and external-service adapters
        tests/            # focused tests, unless framework conventions dictate colocated tests
    shared/               # stable cross-feature primitives only; no dumping ground
  tests/                  # integration and end-to-end tests if idiomatic
  docs/                   # canonical architecture, decisions, requirements
```

## Actual project tree and ownership
| Path/pattern | Responsibility | Owner/role | Public boundary | Notes |
|---|---|---|---|---|
| | | | | |

## Dependencies and data flow
Describe allowed imports, API boundaries, validation, error propagation, transactions, authorization, logging, and external-system boundaries. State forbidden dependency directions.

## Data and security
Identify data classifications, sources of truth, retention, migrations, authentication/authorization, secret handling, and threat assumptions. Link relevant Jira decisions.

## Test architecture
Unit/domain, application, integration, contract, UI/accessibility, and end-to-end layers; state which checks gate merge and release.

## Decisions and alternatives
| ADR | Decision | Alternatives | Rationale/evidence | Owner | Approval/date |
|---|---|---|---|---|---|
| | | | | | |

## Official references
Record exact language, framework, persistence, hosting, security, and observability documentation URLs and verification date. See `naming.md` for language/style references.
