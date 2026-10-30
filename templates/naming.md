# Naming Contract

Status: draft until approved. Align names across code, API, data, events, Jira, and documentation. Follow selected language/framework official style; do not impose one casing across languages.

## Domain glossary
| Canonical term | Definition | Avoided synonyms | Code/API/data names | Owner |
|---|---|---|---|---|
| | | | | |

Use one canonical term per business concept. Explain abbreviations; prefer full words. Avoid generic buckets such as `utils`, `common`, `misc`, `manager`, `data`, or `helpers` unless a narrow, documented responsibility makes the name precise.

## Naming matrix
| Element | Rule to agree per language/framework | Example intent |
|---|---|---|
| Directories/packages | Framework-native; group by feature and responsibility | `billing/infrastructure` |
| Source files/modules | One primary responsibility; idiomatic casing | `invoice_repository.py`, `InvoiceRepository.ts` (adapt to ecosystem) |
| Functions/methods | Verb + domain outcome; idiomatic casing | `calculate_invoice_total` / `calculateInvoiceTotal` |
| Variables | Specific domain noun; booleans as predicates | `overdueInvoices`, `isEligible` |
| Classes/types/interfaces | Domain noun or role; idiomatic type casing | `Invoice`, `PaymentGateway` |
| Enums | Domain concept; values consistent with serialization | `PaymentStatus.PENDING` |
| Constants | Stable values only; native constant convention | `DEFAULT_PAGE_SIZE` / `defaultPageSize` per style guide |
| Tests | Mirror unit/feature and describe behavior | `test_rejects_expired_invitation` |
| API routes | Resource nouns, plural collections, HTTP semantics | `GET /invoices/{invoiceId}` |
| Request/response fields | Stable, documented public contract; consistent casing | `invoiceId`, `dueDate` |
| Database tables/columns | ORM/database convention; policy declared | `invoices.due_at` |
| Events | Past-tense fact, version when contract requires | `InvoiceIssued` |
| Config/env vars | Documented, scoped, no secret values in source | `PAYMENTS_API_BASE_URL` |
| Migrations | Ordered, immutable after shared application | `20261030_add_invoice_due_date` |

## Language and repository rules
| Language/framework | File/module | Function/variable | Type | Constant | Formatter/linter | Official docs/style URL |
|---|---|---|---|---|---|---|
| Python | snake_case | snake_case | CapWords | project convention | Ruff/Black or existing tool | https://docs.python.org/3/tutorial/ ; https://peps.python.org/pep-0008/ |
| JavaScript/TypeScript | ecosystem convention | camelCase | PascalCase | project convention | Prettier + ESLint or existing tool | https://developer.mozilla.org/en-US/docs/Web/JavaScript ; https://www.typescriptlang.org/docs/ |
| Rust | snake_case | snake_case | UpperCamelCase | SCREAMING_SNAKE_CASE | rustfmt + Clippy | https://doc.rust-lang.org/book/ ; https://doc.rust-lang.org/std/ |
| Go | lowercase concise package files | MixedCaps; exported starts uppercase | MixedCaps | idiomatic const context | gofmt + go vet | https://go.dev/doc/ ; https://go.dev/doc/effective_go |
| Java | lowercase packages; type-aligned files | lowerCamelCase | UpperCamelCase | UPPER_SNAKE_CASE | formatter + Checkstyle/Spotless | https://docs.oracle.com/en/java/ |
| Kotlin | lowercase packages; framework file convention | lowerCamelCase | UpperCamelCase | idiomatic `const val` | ktfmt/Ktlint | https://kotlinlang.org/docs/home.html ; https://kotlinlang.org/docs/coding-conventions.html |

Language detection alone does not determine framework style. Inspect manifests, existing code, and repository rules, then add verified official framework links. Preserve existing patterns until an approved migration. Configure formatters/linters additively; do not reformat a repository wholesale during setup.

## Enforcement and exceptions
Review names manually against the glossary and idiomatic style guide, then run the selected language-native formatter/linter in check-only mode where supported. Record approved legacy, generated-code, protocol, and interoperability exceptions here. Never rename files or identifiers automatically. Treat API and database naming changes as compatibility-impacting changes.
