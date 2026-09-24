# CareReady

**Staff & Device Readiness for Multi-site Care Organizations**

Repository and Python package: `careready-api`.

CareReady helps IT teams at multi-site care organizations get staff equipment ready before a start date and recover it reliably when a placement ends. It connects staff-readiness requests, device reservations, vendor fulfillment, approvals, deliveries, and evidence across locations and organizations.

## Product context

A fictional Canadian care network operates six locations with a small central IT team. New hires, rotating placements, and location transfers create time-sensitive equipment requests. Today a request may be marked complete in a ticket while the laptop is still with a vendor or missing its handoff record. CareReady makes that readiness gap explicit.

A site coordinator submits a starter-kit request with a start date and role template. IT reserves an available device or requests a purchase. A separate budget approver reviews the spend, a vendor fulfills the order, and the receiving site confirms delivery and custody. At placement end, IT tracks the return, inspection, and wipe evidence before releasing a device for reuse.

This independently designed product is motivated by my interest in IT support and workflow automation. It uses fictional organizations and staff; it is not affiliated with an employer, does not reproduce an internal system, and does not handle patient records or clinical decisions.

## Current status: foundation

Implemented and available now:

- FastAPI application factory, async lifespan, environment settings, and OpenAPI docs.
- `GET /health/live`: process liveness, independent of database/cache availability.
- `GET /health/ready`: bounded PostgreSQL and Redis probes; HTTP 503 on an outage.
- Request-scoped async SQLAlchemy session dependency; SQLModel dependency installed for upcoming models.
- Isolated local PostgreSQL/Redis Compose services, Python packaging, automated tests, linting, and GitHub Actions configuration.
- Container build recipe and a documented development workflow.

Business endpoints, domain tables, migrations, authentication, authorization, tenant enforcement, and background workers are **planned, not implemented**. This is not yet a production service. Health routes do not expose business data.

## Local quick start

Clone with `git clone git@github.com:PraneetS11/careready-api.git`, then `cd careready-api`.

Requires Python 3.12, Git, and Docker Desktop running. Run from this repository:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.lock
python -m pip install --no-deps -e .
cp -n .env.example .env
docker compose up -d --wait
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8002
```

Open http://127.0.0.1:8002/docs. In another terminal:

```bash
curl --fail http://127.0.0.1:8002/health/live
curl --fail http://127.0.0.1:8002/health/ready
.venv/bin/python -m pytest -q
.venv/bin/ruff check .
.venv/bin/ruff format --check .
```

`make run`, `make test`, `make lint`, and `make services` provide equivalent shortcuts. The API can start without Docker, but readiness correctly returns 503 until both dependencies are available. `docker compose stop` preserves the database volume.

## Planned delivery

1. Site, vendor, staff-readiness request, and asset schemas with validation and service boundaries.
2. PostgreSQL persistence with SQLModel, async sessions, and Alembic migrations.
3. User registration, Argon2 password hashing, JWT access and rotating refresh tokens.
4. Organizations, memberships, tenant isolation, and role-based authorization.
5. Start-date readiness, stock reservation, staff onboarding/offboarding, shipment events, and approval state machines.
6. Append-only audit records, compliance evidence, request logging, and safe error contracts.
7. Redis-backed revocation and caching; Celery jobs with retries and idempotency.
8. Integration/security tests, container deployment, backup/restore, and operational monitoring.

## Repository map

```text
app/main.py         Application composition and resource lifecycle
app/api/            HTTP routes (health only today)
app/core/           Typed configuration
app/db/             Request-scoped session dependency
app/models/         Future persisted domain models
app/schemas/        Future request/response contracts
app/services/       Future business rules and transactions
tests/              Automated behavior checks
docs/               Architecture, roadmap, and development notes
```

## Documentation

- [Product brief and realistic scope](docs/PRODUCT.md)
- [Technology-to-feature evidence map](docs/TECHNOLOGY_MAP.md)
- [Architecture and decisions](docs/ARCHITECTURE.md)
- [Milestones and acceptance criteria](docs/ROADMAP.md)
- [Development and deployment](docs/DEVELOPMENT.md)
- [Build progression and commit checkpoints](docs/BUILD_PROGRESSION.md)
- [Personal progress log](docs/PROGRESS.md)
- [CareReady build guide (PDF)](docs/CareReady_Watch_Build_Guide.pdf)

## Configuration

`.env.example` contains only local development values. Never commit `.env`, tokens, or real employee/customer records. Compose binds database/cache ports to loopback. Replace local credentials and use managed secrets, TLS, network restrictions, and validated deployment settings before hosting externally.

Dependency ranges express compatibility intent; `requirements.lock` records the tested environment. Update dependencies deliberately and rerun checks. No license has been selected yet.
