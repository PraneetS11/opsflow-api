# Delivery roadmap

Foundation is implemented. All milestones below remain open.

## M1: Vendor and asset schemas, validation, pagination, and service boundaries

Acceptance: implement the smallest end-to-end behavior, document its API, add success and failure tests, and demonstrate it with fictional fixtures. Commit only working increments.

## M2: PostgreSQL persistence with SQLModel, async sessions, and Alembic migrations

Acceptance: implement the smallest end-to-end behavior, document its API, add success and failure tests, and demonstrate it with fictional fixtures. Commit only working increments.

## M3: User registration, Argon2 password hashing, JWT access and rotating refresh tokens

Acceptance: implement the smallest end-to-end behavior, document its API, add success and failure tests, and demonstrate it with fictional fixtures. Commit only working increments.

## M4: Organizations, memberships, tenant isolation, and role-based authorization

Acceptance: implement the smallest end-to-end behavior, document its API, add success and failure tests, and demonstrate it with fictional fixtures. Commit only working increments.

## M5: Employee onboarding/offboarding, asset assignment, shipment events, and approval state machines

Acceptance: implement the smallest end-to-end behavior, document its API, add success and failure tests, and demonstrate it with fictional fixtures. Commit only working increments.

## M6: Append-only audit records, compliance evidence, request logging, and safe error contracts

Acceptance: implement the smallest end-to-end behavior, document its API, add success and failure tests, and demonstrate it with fictional fixtures. Commit only working increments.

## M7: Redis-backed revocation and caching; Celery jobs with retries and idempotency

Acceptance: implement the smallest end-to-end behavior, document its API, add success and failure tests, and demonstrate it with fictional fixtures. Commit only working increments.

## M8: Integration/security tests, container deployment, backup/restore, and operational monitoring

Acceptance: implement the smallest end-to-end behavior, document its API, add success and failure tests, and demonstrate it with fictional fixtures. Commit only working increments.

## Release gates

Tenant isolation tests must cover list/detail/update/delete, nested relationships, background jobs, cache keys, and audit exports. Test refresh-token replay, revoked sessions, self-approval, duplicate assignment races, duplicate shipment callbacks, failed worker retries, and offboarding exceptions. Run integration tests against PostgreSQL rather than substituting SQLite for constraint behavior.

## Domain-specific acceptance gates

First vertical slice: fictional Cedar Care site -> staff placement -> kit request -> stock reservation -> independent approval when needed -> shipment -> readiness checklist -> custody -> return -> wipe evidence -> reusable stock. Build one transition per focused increment.

Then test concurrent reservations, stale approvals after amount changes, overdue delivery, expired reservations, duplicate shipment events, tenant-scoped reminder jobs, and blocked reuse without wipe evidence. Product measures must be derived from recorded events and must not be advertised as achieved improvements before measurement.
