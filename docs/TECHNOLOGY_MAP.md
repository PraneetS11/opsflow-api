# CareReady technology evidence map

CareReady serves staff and device readiness across care sites. The following features are planned unless marked foundation. Each technology must support a visible behavior and a test; dependency installation alone is not evidence of proficiency.

| Technology / concept | Product use | Demonstration or acceptance evidence |
|---|---|---|
| FastAPI, routers, path/query/body/header handling | Sites, assets, readiness requests; date/site/status filters | Validated requests, pagination, safe status codes, OpenAPI |
| Pydantic settings and schemas | Environment config (foundation), kit and date validation | Reject end dates before start dates; secrets excluded from responses |
| SQLModel + PostgreSQL | Placements, stock, custody, approvals, shipment history | Reviewed constraints and real database integration tests |
| Async I/O and lifespan | Database/cache lifecycle (foundation), concurrent I/O | Per-request sessions; bounded health probes; no blocking calls in async routes |
| Service classes + dependency injection | Reservation, approval, readiness and return rules | Thin routes, explicit transaction boundaries, replaceable adapters |
| Alembic | Evolving tenant/domain schema | Upgrade clean DB and safely migrate populated fixtures |
| Password hashing | Staff and operator accounts using Argon2 | Verify hashes; no plaintext stored or logged |
| JWT + Bearer + refresh tokens | Authenticated sessions for site coordinators and IT | Expiry/type/audience checks; rotation and replay detection |
| Redis | Revocation TTLs; tenant-keyed readiness cache | Revoked access fails; mutations invalidate cached summaries |
| RBAC | Coordinator, operator, approver, admin, auditor | Role matrix; self-approval denied; read-only audit access |
| Multi-tenancy | Separate care organizations | Two-tenant tests across routes, relationships, cache, jobs, exports |
| ORM relationships | Placement -> request -> reservation -> assignment; request -> approvals/shipments | Same-tenant foreign keys and race-safe constraints |
| Exceptions and handlers | Stock conflict, invalid state, stale approval | Stable 404/409/422 contracts; safe unexpected errors |
| Middleware / ASGI / CORS / trusted hosts | Request IDs, timings, explicit deployed origins/hosts | Request correlation without token or personal-data leakage |
| Email verification and password reset | Account lifecycle | Expiring single-use links, generic reset responses |
| FastAPI background tasks | Non-critical post-response telemetry only | Document loss-on-crash behavior; no critical workflows here |
| Celery + Redis | Due-date reminders, delayed-shipment checks, return reminders | Retry/backoff, tenant context, idempotency, transactional outbox |
| Flower | Worker troubleshooting | Private monitoring, queue/retry visibility, protected access |
| Audit logging | Approval, custody, return and wipe evidence | Audit event commits with mutation; immutable tenant-scoped history |
| Swagger UI / ReDoc | Client-ready contracts (health docs are foundation) | Examples and errors for real workflows |
| pytest + unittest.mock | Service decisions and adapter failures (health tests are foundation) | Failure paths and contract checks; mocks complemented by integration tests |
| Schemathesis | OpenAPI-driven negative cases | Run against disposable seeded test deployment |
| Docker, CI and deployment | Separate API/worker; PostgreSQL/Redis | Foundation Compose and CI; later migrations, secrets, TLS, backup/restore |

## Credible engineering depth

Do not add an AI feature just to broaden the stack. First prove transaction safety, tenant isolation, reliable jobs, and lifecycle rules. A focused system with failure-case evidence is stronger than many unchecked integrations.
