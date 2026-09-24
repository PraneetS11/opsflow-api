# OpsFlow architecture

## Implemented foundation

HTTP -> FastAPI router -> health probes -> async PostgreSQL engine / Redis client.
The application owns clients in lifespan and closes them at shutdown. Each future database request receives its own AsyncSession; sessions must not be shared across concurrent tasks. Transactions belong to service methods, not global middleware. Schema migrations will be explicit Alembic operations; startup does not create tables.

## Target architecture (not implemented)

HTTP -> validated schema -> authenticated principal -> tenant membership and permission check -> service transaction -> SQLModel/PostgreSQL.
Background work: committed transaction -> outbox -> Celery/Redis -> idempotent worker. Audit events should be stored with the domain mutation in the same transaction.

## Tenant boundary

Every tenant-owned table carries organization_id. Resolve organization membership from an authenticated principal; never trust an arbitrary organization header on its own. Scope list, detail, mutation, relationship, job, cache, and export operations. Composite foreign keys must prevent cross-tenant references. Add tests using two organizations and identical-looking resources before exposing any tenant endpoint. Consider PostgreSQL row-level security as defense in depth after request-level isolation works.

## Domain model direction

Organization -> locations, memberships, employees, vendors, assets, shipments, provisioning requests, approvals, evidence, audit events.
User -> organization memberships; roles belong to membership rather than global user.
AssetAssignment links an employee and asset with assigned/returned timestamps.
Shipment links a vendor and provisioning request; immutable shipment events capture progress.
Approval captures reviewer, decision, reason, and request version.

## Business invariants

- One active assignment per asset; enforce under a database transaction with a unique constraint or lock.
- Provisioning: draft -> submitted -> approved/rejected -> fulfilling -> completed. Reject invalid transitions with 409.
- A requester cannot approve their own request; approvals above a policy threshold require a second reviewer.
- Offboarding remains open until assigned assets are returned or an authorized exception is recorded.
- Audit events include tenant, actor, action, object, timestamp, and correlation ID; exclude secrets and unnecessary personal data.
- Compliance here means evidence tracking, not a certification or legal compliance guarantee.

## Authorization plan

Organization admin: memberships and policy. IT operator: assets and provisioning. Approver: scoped approval decisions. Employee: own requests and assignments. Auditor: read-only evidence and audit history. Deny by default and test both role and tenant boundaries.

## Security and reliability progression

Use Argon2 for passwords, short-lived access JWTs with issuer/audience/type checks, and rotating refresh tokens stored as hashes with family reuse detection. Redis revocation entries expire with tokens. Persist refresh-session state durably; define Redis-outage behavior before auth launch. Never log tokens or passwords.

Workers receive identifiers and tenant context, recheck authorization where appropriate, and retry transient failures with backoff. Use idempotency keys and an outbox to avoid lost or duplicated work. Shipping providers and email providers are future adapters, not integrated today.

## Decisions

Python 3.12 matches the local interpreter. FastAPI provides HTTP composition; SQLModel will define domain tables over SQLAlchemy's async engine. PostgreSQL is the source of truth. Redis is disposable support infrastructure, not authoritative inventory storage. One deployable API first; split services only when operational evidence justifies it.
