# CareReady build progression

Video: [FastAPI Beyond CRUD](https://www.youtube.com/watch?v=TO4aQ3ghFOc) - 12:52:54.

CareReady is the staff and device readiness product for multi-site care organizations. Watch to a checkpoint, pause, build and test, then commit. Times are video positions, not coding deadlines. Never backdate or create an empty feature commit.

The foundation already exists. All business checkpoints below remain planned. Record actual evidence in [PROGRESS.md](PROGRESS.md).

## 01: HTTP foundations | 0:00-0:49:43

Watch 50 min; build 30-45 min.

Understand how method, URL, path parameter, query parameter, headers, and JSON body reach a Python function. The existing starter is your launch point, not a reason to skip understanding routing.

### Build in CareReady

- Create SiteCreate with name, city, timezone, and active; use fictional Hamilton and Toronto care sites.
- Implement GET /api/v1/sites, GET /api/v1/sites/{id}, and POST /api/v1/sites using temporary memory. Add an active filter.
- Sketch ReadinessRequestCreate with site_id, staff_reference, role_template, start_date, and end_date. Validate end_date >= start_date. The request workflow is implemented later; do not imply persistence or tenant protection yet.

### Bookly parallel

Build the corresponding book list/detail/create operations with title, author, ISBN, and publication date.

### Required checks

- POST valid data returns 201; malformed data returns 422.
- Unknown ID returns 404; query filtering changes the result.

Explain: What belongs in a path versus a query? Why can validation reject a request before the handler runs?

### Commit checkpoints

#### C01 - pause 0:49:43: Site HTTP contract

Create/list/detail and active filtering; malformed data 422, missing site 404, placement date schema rejects reversed dates.

CareReady: `feat: add validated care site endpoints`

Bookly: `feat: add validated book endpoints`

## 02: CRUD and route boundaries | 0:49:43-1:38:22

Watch 49 min; build 35-60 min.

Follow list-based REST operations, then route grouping at 1:23:37. Understand HTTP semantics before adding database complexity.

### Build in CareReady

- Move site handlers to app/api/sites.py and add PATCH and DELETE. Distinguish omitted fields from explicit nulls.
- Add status/city filters and consistent 404/422 responses. Use a fictional staff kit request to explain why site identity matters.
- Document future archive behavior: a site referenced by a placement must not disappear from its audit history. Physical delete is limited to unused prototype records.

### Bookly parallel

Organize /books in its own router; add edits, deletion behavior, and author filtering.

### Required checks

- Missing site returns 404 consistently across read/update/delete.
- Invalid patch preserves prior state. A 204 delete response has no JSON body.

Explain: When is PATCH different from PUT? Which rules belong in schemas versus services?

### Commit checkpoints

#### C02 - pause 1:23:37: Site CRUD

PATCH preserves omitted fields; deletion and missing IDs have documented responses.

CareReady: `feat: implement care site CRUD`

Bookly: `feat: implement book CRUD`

#### C03 - pause 1:38:22: Router separation

Site routes live under /api/v1; filters and all earlier tests still pass.

CareReady: `refactor: organize care site API routes`

Bookly: `refactor: organize catalog API routes`

## 03: Async persistence | 1:38:22-2:29:48

Watch 51 min; build 75-120 min.

Slow down for settings, async engine/session setup, lifespan, models, and SQLModel persistence. The starter already owns clients in lifespan; extend that design.

### Build in CareReady

- Define a Site SQLModel with UUID, organization_id, name, timezone, active, and UTC timestamps. Use a fixed fictional organization until real membership enforcement exists.
- Extend the existing request-scoped async session dependency to persist site creation and listing in PostgreSQL.
- Verify data survives an API restart and failed writes roll back. Understand disposable table creation, then replace it with reviewed Alembic migrations in session 05.

### Bookly parallel

Define a Book table, separate request/response schemas, and verify catalog persistence.

### Required checks

- Create data, restart API, and read it back.
- Reject duplicate business identifiers using database constraints; roll back failed transactions.

Explain: Why is an async session per request necessary? How are validation schemas different from persisted tables?

### Commit checkpoints

#### C04 - pause 2:29:48: Persistent sites

Create a site, restart the API, read it back; failed transaction rolls back.

CareReady: `feat: persist care sites with async PostgreSQL`

Bookly: `feat: persist books with async PostgreSQL`

## 04: Services and dependency injection | 2:29:48-3:33:35

Watch 64 min; build 60-90 min.

Watch service extraction at 2:29:48, dependency injection at 2:55:53, and handler integration at 3:01:20. Complete the block at 3:33:35 before starting accounts.

### Build in CareReady

- Introduce SiteService with an explicit session; keep HTTP parsing and response codes in routers.
- Move create/update/archive rules into service methods and define transaction ownership. Add deterministic pagination with a maximum page size.
- Describe the future ReadinessService contract: create a request, validate its site and placement, apply policy, and compute readiness from required checks. Do not implement the full workflow before relationships.

### Bookly parallel

Move book persistence and ISBN-conflict handling into BookService.

### Required checks

- Service tests exercise conflicts without relying on route internals.
- API tests verify that domain failures become the intended status codes.

Explain: Which layer commits? How would two parallel tasks behave if they shared one session?

### Commit checkpoints

#### C05 - pause 2:55:53: Service boundary

Business rules are testable outside handlers; no shared session across concurrent work.

CareReady: `refactor: extract care site service`

Bookly: `refactor: extract book catalog service`

#### C06 - pause 3:33:35: Injected services

Handlers use injected sessions/services; pagination is stable and bounded.

CareReady: `refactor: inject services and paginate sites`

Bookly: `refactor: inject services and paginate books`

## 05: Users and schema evolution | 3:33:35-4:42:57

Watch 69 min; build 90-150 min.

Learn user models, Alembic, account creation, and password hashing. The video uses passlib; this workspace plans pwdlib with Argon2. Understand the security concept and use the selected maintained dependency consistently.

### Build in CareReady

- Create User and OrganizationMembership models; membership will carry tenant role.
- Initialize Alembic, generate and review the first migration, and test upgrade on a clean database.
- Add registration with normalized email uniqueness, a password policy, and a response that never includes password_hash.

### Bookly parallel

Create reader accounts and the initial Bookly migrations.

### Required checks

- Duplicate email is handled consistently; raw passwords never persist.
- Correct password verifies and incorrect password fails.
- Clean database upgrade succeeds; inspect generated constraints and indexes.

Explain: Why hash rather than encrypt passwords? Why review generated migration code?

### Commit checkpoints

#### C07 - pause 3:59:57: Reviewed schema

User and membership migration upgrades a clean DB; inspect indexes and constraints.

CareReady: `feat: add account and membership migrations`

Bookly: `feat: add reader account migrations`

#### C08 - pause 4:42:57: Account creation

Registration hashes passwords, rejects duplicate normalized email, and never returns a hash.

CareReady: `feat: register accounts with Argon2 passwords`

Bookly: `feat: register reader accounts securely`

## 06: Sessions, JWTs, and revocation | 4:42:57-6:07:39

Watch 85 min; build 120-180 min.

Follow JWT setup, login, Bearer validation, refresh, and Redis revocation. Treat authentication as an end-to-end session design rather than token creation alone.

### Build in CareReady

- Implement login with short-lived access tokens and explicit issuer, audience, expiry, and token-type checks.
- Store hashed refresh tokens durably; rotate them on use and revoke the token family on reuse.
- Implement logout/revocation with Redis TTLs. Decide how revocation behaves if Redis is unavailable; document and test the chosen policy.

### Bookly parallel

Use the same auth concepts for readers and editors, with separate signing secrets per deployed product.

### Required checks

- Expired/wrong-audience/wrong-type tokens fail.
- A reused refresh token cannot create a new session; logout makes the session unusable.
- Authentication errors never echo secrets or disclose whether a password was close.

Explain: Why are access and refresh tokens different? What happens when a token is stolen or Redis fails?

### Commit checkpoints

#### C09 - pause 5:33:14: Access authentication

Login and Bearer dependency validate expiry, issuer, audience, and token type.

CareReady: `feat: authenticate CareReady access tokens`

Bookly: `feat: authenticate Bookly access tokens`

#### C10 - pause 5:50:04: Rotating refresh sessions

Durable hashed refresh tokens rotate; replay revokes the affected session family.

CareReady: `feat: rotate refresh sessions and detect reuse`

Bookly: `feat: rotate reader refresh sessions`

#### C11 - pause 6:07:39: Revocation

Logout revokes access; Redis TTL and outage policy are tested.

CareReady: `feat: revoke sessions with Redis`

Bookly: `feat: revoke reader sessions with Redis`

## 07: Authorization and tenant context | 6:07:39-6:39:24

Watch 32 min; build 90-150 min.

Use the current-user and role-checker concepts, then extend them into organization-scoped memberships. Multi-tenancy is an independent CareReady requirement.

### Build in CareReady

- Resolve active membership from the authenticated user and selected organization. Never accept a tenant header without membership validation.
- Add admin, IT operator, approver, employee, and auditor permission rules.
- Apply tenant predicates to every site operation; include tenant identity in cache and job boundaries later.

### Bookly parallel

Add reader/editor/moderator permissions plus ownership checks for reader-generated content.

### Required checks

- A user from organization A cannot list, read, edit, or delete B records even with a known UUID.
- An employee cannot grant roles; an auditor cannot mutate data.

Explain: Why is checking role alone insufficient? What is the distinction between 401 and 403?

### Commit checkpoints

#### C12 - pause 6:39:24: Tenant permissions

Two organizations cannot access each other; coordinator/operator/approver/admin/auditor permissions deny by default.

CareReady: `feat: enforce tenant memberships and permissions`

Bookly: `feat: enforce reader editor and moderator permissions`

## 08: Relationships and operational workflows | 6:39:24-7:59:58

Watch 81 min; build in several 60-90 minute blocks. Expect 5-8 hours for this domain-heavy stage.

Translate relationships into a coherent operations domain. Do not add every entity in one commit; establish one complete provisioning flow.

### Build in CareReady

- Add StaffPlacement, KitTemplate, ReadinessRequest, checklist items, Vendor, Asset, Reservation, Assignment, PurchaseRequest, Approval, Shipment, and ReturnCase in small migrations.
- Reserve available equipment atomically; route stock shortages into an independent purchase approval. Enforce same-tenant references and invalidate approval if the requested amount changes.
- Track draft -> submitted -> approved -> preparing -> dispatched -> ready; rejected/cancelled are explicit alternatives. Derive readiness from delivery and required setup checks.
- Track return -> received -> inspected -> wipe_verified -> closed. Only then release equipment for reuse; record authorized exceptions and prevent duplicate assignment.

### Bookly parallel

Build book-review-user and book-tag relationships, then curated collections and moderation ownership.

### Required checks

- Cross-tenant relationships fail even if IDs are valid.
- Two concurrent requests cannot assign the same asset.
- An invalid workflow transition returns 409; rejected requests cannot silently ship.

Explain: Which relationships need a join table? Which invariant requires a database constraint or lock?

### Commit checkpoints

#### C13 - pause 7:05:53: Relational foundation

Sites, placements, kit templates, requests, and assets use same-tenant foreign keys; reversed placement dates fail.

CareReady: `feat: model placements kits and readiness requests`

Bookly: `feat: relate books readers and reviews`

#### C14 - pause 7:59:58: Inventory reservation

After finishing this watch block, pause for multiple build checkpoints. Competing requests cannot reserve the same device; expired reservations release safely.

CareReady: `feat: reserve equipment atomically`

Bookly: `feat: add book tags and curated collections`

#### C15 - pause 7:59:58: Approval policy

At the same pause: requester cannot approve own purchase; changing amount invalidates approval.

CareReady: `feat: enforce independent purchase approvals`

#### C16 - pause 7:59:58: Delivery and readiness

At the same pause: delayed delivery or an incomplete checklist prevents ready status; duplicate shipment events do not repeat side effects.

CareReady: `feat: derive staff readiness from fulfillment checks`

#### C17 - pause 7:59:58: Return and reuse

At the same pause: missing inspection or wipe evidence blocks reuse; authorized exceptions have a reason.

CareReady: `feat: gate equipment reuse on return evidence`

## 09: Error contracts, logs, and audit evidence | 7:59:58-9:05:04

Watch 65 min; build 90-150 min.

Follow exception types, handlers, middleware, CORS, and trusted hosts. Add audit behavior as an independent product requirement.

### Build in CareReady

- Define stable error codes for not-found, conflict, invalid transition, and insufficient permission.
- Add correlation IDs and structured request logs; omit tokens, passwords, and unnecessary employee details.
- Write append-only audit events in the same transaction as state changes. Configure explicit allowed origins/hosts for deployment.

### Bookly parallel

Add consistent catalog/review errors and moderation audit events.

### Required checks

- Unexpected failures return safe 500 responses while logs retain a correlation ID.
- Failed transactions do not leave a misleading success audit record.
- Tenant-scoped audit export never includes another organization.

Explain: How does operational logging differ from durable audit history? Why is CORS not authorization?

### Commit checkpoints

#### C18 - pause 8:33:25: Domain errors

Translate invalid transition, stale approval, and stock conflict into safe stable errors.

CareReady: `feat: add readiness domain error contracts`

Bookly: `feat: add catalog and review error contracts`

#### C19 - pause 9:05:04: Logs and evidence

Correlation IDs, explicit hosts/origins, and audit events work; mutation and audit commit together.

CareReady: `feat: record transactional audit events and request traces`

Bookly: `feat: audit moderation and trace requests`

## 10: Email and account recovery | 9:05:04-10:40:38

Watch 96 min; build 90-150 min.

Understand transport setup, verification, and password reset. Keep templates simple and use a local capture service or provider sandbox while building.

### Build in CareReady

- Define a mail adapter so business logic is independent of a provider.
- Add single-use, expiring verification and reset tokens; store only safe token representations.
- Use generic reset responses to reduce account enumeration; invalidate relevant sessions after reset. Do not send real employee mail from test fixtures.

### Bookly parallel

Add verification and account recovery for reader accounts.

### Required checks

- Expired and reused reset links fail.
- Reset responses do not reveal account existence.
- A failed mail send is observable and safely retryable.

Explain: What can a reset token authorize? Why must retries not generate duplicate side effects?

### Commit checkpoints

#### C20 - pause 9:31:21: Mail adapter

Use local capture or provider sandbox; transport failures can be simulated without real recipients.

CareReady: `feat: add a testable notification mail adapter`

Bookly: `feat: add a testable reader mail adapter`

#### C21 - pause 10:07:51: Account verification

Confirmation tokens expire and are single-use.

CareReady: `feat: verify staff accounts with expiring tokens`

Bookly: `feat: verify reader accounts`

#### C22 - pause 10:40:38: Account recovery

Generic reset response; expired/reused tokens fail; reset invalidates relevant sessions.

CareReady: `feat: add safe account recovery`

Bookly: `feat: add safe reader account recovery`

## 11: Durable background work | 10:40:38-11:23:48

Watch 43 min; build 120-180 min.

Compare in-process tasks with Celery/Redis and worker monitoring. Use in-process tasks only for short, non-critical work.

### Build in CareReady

- Create Celery jobs for approaching start dates, late shipments, expiring reservations, and overdue returns.
- Pass organization and record identifiers; reload state and check tenant scope inside the worker.
- Add retry/backoff, idempotency keys, and an outbox so committing a request cannot lose its notification. Keep Flower private and authenticated when deployed.

### Bookly parallel

Add catalog-import or review-notification jobs with the same reliability principles.

### Required checks

- Kill and restart a worker; a retry does not duplicate a shipment or message.
- A job for A cannot access B; permanently failed jobs are visible for review.

Explain: Why can an in-process task disappear? What does at-least-once delivery require from your code?

### Commit checkpoints

#### C23 - pause 10:45:44: Task boundary

Only disposable post-response work uses BackgroundTasks; document crash-loss behavior.

CareReady: `chore: define critical and disposable task boundaries`

Bookly: `chore: define notification task boundaries`

#### C24 - pause 11:16:17: Durable jobs

Celery handles due-date, late-shipment, and return reminders; tenant context, outbox, retry/backoff, and idempotency are tested.

CareReady: `feat: queue reliable readiness and return jobs`

Bookly: `feat: queue reliable catalog and review jobs`

#### C25 - pause 11:23:48: Worker visibility

Flower is private; failed/retried jobs are visible; worker restart does not duplicate effects.

CareReady: `ops: monitor worker retries and failures`

Bookly: `ops: monitor catalog worker jobs`

## 12: API contracts and test depth | 11:23:48-12:09:17

Watch 45 min; build 2-4 hours.

Use OpenAPI examples, unit tests, mocks, and schema-driven tests. Build on tests already written throughout the guide; do not defer all testing until this point.

### Build in CareReady

- Document auth, pagination, transitions, errors, and representative fictional payloads.
- Separate pure service tests from real PostgreSQL/Redis integration tests and API tests.
- Add a two-tenant security matrix and concurrency tests. Use Schemathesis against a disposable test service, never production data.

### Bookly parallel

Test search/filtering, review ownership, duplicate ISBNs, moderation, and authentication.

### Required checks

- CI runs from a clean clone; no test depends on the developer database.
- A deliberately broken tenant filter makes the security tests fail.
- Mock-based tests are complemented by real dependency behavior.

Explain: What failure could pass a mock test and still occur against PostgreSQL?

### Commit checkpoints

#### C26 - pause 11:36:02: API documentation

Document auth, pagination, transition rules, examples, and failure responses in OpenAPI.

CareReady: `docs: describe staff readiness API contracts`

Bookly: `docs: describe book discovery API contracts`

#### C27 - pause 12:01:27: Behavior tests

Run service/API and real PostgreSQL/Redis tests, tenant isolation, races, and refresh replay cases in CI.

CareReady: `test: verify tenancy reservations and session security`

Bookly: `test: verify reviews permissions and sessions`

#### C28 - pause 12:09:17: Contract tests

Schemathesis runs against disposable fixtures; deliberately broken validation produces a failing test.

CareReady: `test: exercise OpenAPI contracts with Schemathesis`

Bookly: `test: exercise Bookly OpenAPI contracts`

## 13: Deployment and operations | 12:09:17-12:52:54

Watch 44 min; build 2-4 hours plus hardening.

Observe the deployment lifecycle and adapt it to current provider documentation and your budget. This starter has no hosted deployment or paid resources.

### Build in CareReady

- Build an API image and a separate worker process; configure managed secrets and private database/cache access.
- Run reviewed migrations once per release, then smoke-test readiness and core workflows.
- Add backup/restore drills, safe rollback, logs/metrics, and alerting. Restrict CORS/hosts, protect operational dashboards, and validate token settings.

### Bookly parallel

Deploy Bookly independently with its own credentials, database, and release checks.

### Required checks

- A clean deployment passes smoke tests without manual database edits.
- A failed dependency removes readiness but leaves process liveness intact.
- Restore a backup into a disposable database and verify representative records.

Explain: How will you roll back code without corrupting a migrated schema? How do you know a worker is stuck?

### Commit checkpoints

#### C29 - pause 12:52:54: Release and restore

Build API/worker images; validate release migrations, secrets, health, rollback, and a restore drill before declaring deployed.

CareReady: `ops: document and verify CareReady deployment`

Bookly: `ops: document and verify Bookly deployment`

## Complete chapter index

| Timestamp | Concept | CareReady action |
|---|---|---|
| 0:00 | Orientation | Define the provisioning story |
| 0:01:00 | Workspace setup | Use the two isolated repositories |
| 0:07:30 | First HTTP server | Explain the existing health route |
| 0:10:45 | Server commands | Run each API on its own port |
| 0:14:11 | URL identifiers | Site UUID detail route |
| 0:17:23 | Request tooling | Save repeatable site requests |
| 0:20:58 | Query inputs | Filter active sites |
| 0:24:40 | Combined inputs | Site detail plus optional fields |
| 0:26:51 | Optional filters | Define safe filter defaults |
| 0:31:48 | JSON validation | SiteCreate plus placement-date validation |
| 0:39:11 | Header handling | Understand request metadata |
| 0:49:43 | Memory-backed CRUD | Site create/read/update/delete |
| 1:23:37 | Router modules | Move site routes out of main |
| 1:38:22 | ORM introduction | Map care sites to persisted models |
| 1:42:33 | Database preparation | Start isolated PostgreSQL |
| 1:44:13 | Typed settings | Read database configuration safely |
| 1:53:38 | Async ORM wiring | Use per-request async sessions |
| 1:58:38 | Resource lifetime | Own clients in app lifespan |
| 2:10:02 | Persisted models | Define Site identity and fields |
| 2:20:00 | Table creation | Distinguish prototype schema from migrations |
| 2:27:08 | ORM operations | Persist and retrieve a site |
| 2:29:48 | Service boundary | Extract SiteService |
| 2:55:53 | Dependency patterns | Inject sessions and principal context |
| 3:01:20 | Handler integration | Keep routes thin and explicit |
| 3:33:35 | Account model | User plus organization membership |
| 3:42:09 | Schema migrations | Review Alembic revisions |
| 3:59:57 | Registration logic | Normalize and validate accounts |
| 4:18:55 | Password storage | Argon2 through pwdlib in this plan |
| 4:25:42 | Registration route | Return safe account fields |
| 4:42:57 | Token concepts | Define access and refresh responsibilities |
| 4:48:29 | JWT library | Validate issuer audience and expiry |
| 5:01:13 | Sign-in flow | Verify credentials and issue sessions |
| 5:13:59 | Bearer dependency | Reject invalid principals |
| 5:33:14 | Session renewal | Rotate durable refresh tokens |
| 5:50:04 | Revocation store | Redis TTL and logout behavior |
| 6:07:39 | Permission design | Organization-scoped roles |
| 6:09:45 | Principal lookup | Resolve active membership |
| 6:20:25 | Role persistence | Roles on membership not global user |
| 6:26:55 | Permission dependency | Deny unauthorized operations |
| 6:39:24 | Relational modeling | Staff placements, kits, requests, and assets |
| 7:05:53 | Relationship expansion | Reservations, approvals, shipments, returns |
| 7:59:58 | Failure semantics | Consistent safe API errors |
| 8:04:06 | Domain error types | ReadinessConflict and InvalidTransition |
| 8:18:14 | Exception translation | Map domain errors to HTTP |
| 8:23:26 | Handler registration | Apply errors across routers |
| 8:33:25 | Middleware lifecycle | Understand request ordering |
| 8:36:54 | Request logging | Correlation IDs without secrets |
| 8:53:28 | Middleware practice | Measure latency and failure paths |
| 8:59:36 | ASGI integration | Check middleware compatibility |
| 9:00:21 | Origin policy | Allow only intended frontends |
| 9:03:34 | Host policy | Configure deployed hostnames |
| 9:05:04 | Mail requirements | Define notification adapter |
| 9:06:39 | Mail configuration | Use sandbox credentials |
| 9:21:46 | Delivery check | Send only controlled test messages |
| 9:31:21 | Account confirmation | Single-use verification token |
| 10:07:51 | Recovery flow | Expiring reset plus session invalidation |
| 10:40:38 | Deferred work | Separate deadline jobs from disposable tasks |
| 10:43:00 | In-process tasks | Use only for non-critical work |
| 10:45:44 | Queue and worker | Tenant-scoped deadline and return jobs |
| 11:16:17 | Worker visibility | Monitor retries without public dashboards |
| 11:23:48 | OpenAPI presentation | Document operation contracts |
| 11:36:02 | Test strategy | Unit integration and API layers |
| 11:37:10 | Mocks and pytest | Test business decisions and failures |
| 12:01:27 | Schema-based tests | Exercise disposable API contracts |
| 12:09:17 | Hosted release | Secrets migrations health and rollback |
