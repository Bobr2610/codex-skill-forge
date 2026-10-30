# Developer Tooling and Container Assessment

Status: recommendations only until project-owner approval. Do not add packages, containers, infrastructure, or CI workflows without approval.

| Concern | Current state/evidence | Recommendation | Fit/tradeoffs | Official documentation | Owner | Setup command | Verification |
|---|---|---|---|---|---|---|---|
| Runtime/version manager | | | | | | | |
| Package/dependency manager | | | | | | | |
| Formatter | | | | | | | |
| Linter/static analysis | | | | | | | |
| Type checker/compiler | | | | | | | |
| Test runner/coverage | | | | | | | |
| Docker Engine/Desktop | | Choose Docker only when it improves reproducibility, service parity, onboarding, or CI | | https://docs.docker.com/get-started/ | | | |
| Docker Compose | | Evaluate for multi-service local development and reproducible integration tests | | https://docs.docker.com/compose/ ; https://docs.docker.com/compose/gettingstarted/ | | | |
| Database/migrations | | | | | | | |
| CI/CD | | | | | | | |
| Security/dependency scanning | | | | | | | |
| Observability | | | | | | | |

For each recommended tool, explain why it fits this stack and team, operating-system/licensing requirements, alternatives, maintenance burden, and verification commands. Use official docs first. For Docker, specify image/base image and version policy, build context and `.dockerignore`, non-root runtime where applicable, configuration/secrets handling, persistent-vs-ephemeral data, health checks/service readiness, port exposure, and local cleanup. Never bake secrets into images or commit them. Document commands for start, status/logs, test, stop, and disposable data reset; warn before destructive volume removal.
