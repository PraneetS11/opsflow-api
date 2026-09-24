# CareReady delivery roadmap

CareReady coordinates staff and device readiness for fictional multi-site care organizations. The API foundation exists; the stages below are planned. See BUILD_PROGRESSION.md for exact video pauses, acceptance gates, and commit messages.

## Implemented foundation

FastAPI app factory; settings; async database/cache lifecycle; liveness/readiness routes; local PostgreSQL/Redis; six starter tests; CI; container recipe. No domain routes, migrations, JWT sessions, tenant enforcement, or workers are claimed as implemented.

## Stage 01: HTTP foundations

Watch range: 0:00-0:49:43. Watch 50 min; build 30-45 min.

- Create SiteCreate with name, city, timezone, and active; use fictional Hamilton and Toronto care sites.
- Implement GET /api/v1/sites, GET /api/v1/sites/{id}, and POST /api/v1/sites using temporary memory. Add an active filter.
- Sketch ReadinessRequestCreate with site_id, staff_reference, role_template, start_date, and end_date. Validate end_date >= start_date. The request workflow is implemented later; do not imply persistence or tenant protection yet.

Acceptance: POST valid data returns 201; malformed data returns 422. Unknown ID returns 404; query filtering changes the result.

## Stage 02: CRUD and route boundaries

Watch range: 0:49:43-1:38:22. Watch 49 min; build 35-60 min.

- Move site handlers to app/api/sites.py and add PATCH and DELETE. Distinguish omitted fields from explicit nulls.
- Add status/city filters and consistent 404/422 responses. Use a fictional staff kit request to explain why site identity matters.
- Document future archive behavior: a site referenced by a placement must not disappear from its audit history. Physical delete is limited to unused prototype records.

Acceptance: Missing site returns 404 consistently across read/update/delete. Invalid patch preserves prior state. A 204 delete response has no JSON body.

## Stage 03: Async persistence

Watch range: 1:38:22-2:29:48. Watch 51 min; build 75-120 min.

- Define a Site SQLModel with UUID, organization_id, name, timezone, active, and UTC timestamps. Use a fixed fictional organization until real membership enforcement exists.
- Extend the existing request-scoped async session dependency to persist site creation and listing in PostgreSQL.
- Verify data survives an API restart and failed writes roll back. Understand disposable table creation, then replace it with reviewed Alembic migrations in session 05.

Acceptance: Create data, restart API, and read it back. Reject duplicate business identifiers using database constraints; roll back failed transactions.

## Stage 04: Services and dependency injection

Watch range: 2:29:48-3:33:35. Watch 64 min; build 60-90 min.

- Introduce SiteService with an explicit session; keep HTTP parsing and response codes in routers.
- Move create/update/archive rules into service methods and define transaction ownership. Add deterministic pagination with a maximum page size.
- Describe the future ReadinessService contract: create a request, validate its site and placement, apply policy, and compute readiness from required checks. Do not implement the full workflow before relationships.

Acceptance: Service tests exercise conflicts without relying on route internals. API tests verify that domain failures become the intended status codes.

## Stage 05: Users and schema evolution

Watch range: 3:33:35-4:42:57. Watch 69 min; build 90-150 min.

- Create User and OrganizationMembership models; membership will carry tenant role.
- Initialize Alembic, generate and review the first migration, and test upgrade on a clean database.
- Add registration with normalized email uniqueness, a password policy, and a response that never includes password_hash.

Acceptance: Duplicate email is handled consistently; raw passwords never persist. Correct password verifies and incorrect password fails. Clean database upgrade succeeds; inspect generated constraints and indexes.

## Stage 06: Sessions, JWTs, and revocation

Watch range: 4:42:57-6:07:39. Watch 85 min; build 120-180 min.

- Implement login with short-lived access tokens and explicit issuer, audience, expiry, and token-type checks.
- Store hashed refresh tokens durably; rotate them on use and revoke the token family on reuse.
- Implement logout/revocation with Redis TTLs. Decide how revocation behaves if Redis is unavailable; document and test the chosen policy.

Acceptance: Expired/wrong-audience/wrong-type tokens fail. A reused refresh token cannot create a new session; logout makes the session unusable. Authentication errors never echo secrets or disclose whether a password was close.

## Stage 07: Authorization and tenant context

Watch range: 6:07:39-6:39:24. Watch 32 min; build 90-150 min.

- Resolve active membership from the authenticated user and selected organization. Never accept a tenant header without membership validation.
- Add admin, IT operator, approver, employee, and auditor permission rules.
- Apply tenant predicates to every site operation; include tenant identity in cache and job boundaries later.

Acceptance: A user from organization A cannot list, read, edit, or delete B records even with a known UUID. An employee cannot grant roles; an auditor cannot mutate data.

## Stage 08: Relationships and operational workflows

Watch range: 6:39:24-7:59:58. Watch 81 min; build in several 60-90 minute blocks. Expect 5-8 hours for this domain-heavy stage.

- Add StaffPlacement, KitTemplate, ReadinessRequest, checklist items, Vendor, Asset, Reservation, Assignment, PurchaseRequest, Approval, Shipment, and ReturnCase in small migrations.
- Reserve available equipment atomically; route stock shortages into an independent purchase approval. Enforce same-tenant references and invalidate approval if the requested amount changes.
- Track draft -> submitted -> approved -> preparing -> dispatched -> ready; rejected/cancelled are explicit alternatives. Derive readiness from delivery and required setup checks.
- Track return -> received -> inspected -> wipe_verified -> closed. Only then release equipment for reuse; record authorized exceptions and prevent duplicate assignment.

Acceptance: Cross-tenant relationships fail even if IDs are valid. Two concurrent requests cannot assign the same asset. An invalid workflow transition returns 409; rejected requests cannot silently ship.

## Stage 09: Error contracts, logs, and audit evidence

Watch range: 7:59:58-9:05:04. Watch 65 min; build 90-150 min.

- Define stable error codes for not-found, conflict, invalid transition, and insufficient permission.
- Add correlation IDs and structured request logs; omit tokens, passwords, and unnecessary employee details.
- Write append-only audit events in the same transaction as state changes. Configure explicit allowed origins/hosts for deployment.

Acceptance: Unexpected failures return safe 500 responses while logs retain a correlation ID. Failed transactions do not leave a misleading success audit record. Tenant-scoped audit export never includes another organization.

## Stage 10: Email and account recovery

Watch range: 9:05:04-10:40:38. Watch 96 min; build 90-150 min.

- Define a mail adapter so business logic is independent of a provider.
- Add single-use, expiring verification and reset tokens; store only safe token representations.
- Use generic reset responses to reduce account enumeration; invalidate relevant sessions after reset. Do not send real employee mail from test fixtures.

Acceptance: Expired and reused reset links fail. Reset responses do not reveal account existence. A failed mail send is observable and safely retryable.

## Stage 11: Durable background work

Watch range: 10:40:38-11:23:48. Watch 43 min; build 120-180 min.

- Create Celery jobs for approaching start dates, late shipments, expiring reservations, and overdue returns.
- Pass organization and record identifiers; reload state and check tenant scope inside the worker.
- Add retry/backoff, idempotency keys, and an outbox so committing a request cannot lose its notification. Keep Flower private and authenticated when deployed.

Acceptance: Kill and restart a worker; a retry does not duplicate a shipment or message. A job for A cannot access B; permanently failed jobs are visible for review.

## Stage 12: API contracts and test depth

Watch range: 11:23:48-12:09:17. Watch 45 min; build 2-4 hours.

- Document auth, pagination, transitions, errors, and representative fictional payloads.
- Separate pure service tests from real PostgreSQL/Redis integration tests and API tests.
- Add a two-tenant security matrix and concurrency tests. Use Schemathesis against a disposable test service, never production data.

Acceptance: CI runs from a clean clone; no test depends on the developer database. A deliberately broken tenant filter makes the security tests fail. Mock-based tests are complemented by real dependency behavior.

## Stage 13: Deployment and operations

Watch range: 12:09:17-12:52:54. Watch 44 min; build 2-4 hours plus hardening.

- Build an API image and a separate worker process; configure managed secrets and private database/cache access.
- Run reviewed migrations once per release, then smoke-test readiness and core workflows.
- Add backup/restore drills, safe rollback, logs/metrics, and alerting. Restrict CORS/hosts, protect operational dashboards, and validate token settings.

Acceptance: A clean deployment passes smoke tests without manual database edits. A failed dependency removes readiness but leaves process liveness intact. Restore a backup into a disposable database and verify representative records.

## Release gates

Demonstrate two-tenant isolation across CRUD, relationships, jobs, caches, and exports; atomic reservation under concurrent requests; independent and versioned approvals; readiness blocked by late delivery or missing checks; return/inspection/wipe evidence before reuse; duplicate-event safety; token replay rejection; safe retries; migration and restore drills.

Metrics such as ready-by-start-date percentage and stock reuse remain planned measurements. Do not present them as achieved improvements.
