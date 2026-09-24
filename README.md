# OpsFlow API

An IT operations backend for multi-location businesses managing employee equipment from onboarding through offboarding. OpsFlow is designed to connect asset custody, vendor fulfillment, approvals, shipment tracking, and operational evidence in one tenant-aware system.

## Product context

A fictional Canadian professional-services company has 250 employees across Toronto, Waterloo, and remote locations. A new hire needs an approved laptop, an assigned asset, vendor fulfillment, delivery confirmation, and a custody record before their first day. Offboarding must recover equipment and record evidence. This is a product design scenario, not a claim of an existing customer or production deployment.

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

1. Vendor and asset schemas, validation, pagination, and service boundaries.
2. PostgreSQL persistence with SQLModel, async sessions, and Alembic migrations.
3. User registration, Argon2 password hashing, JWT access and rotating refresh tokens.
4. Organizations, memberships, tenant isolation, and role-based authorization.
5. Employee onboarding/offboarding, asset assignment, shipment events, and approval state machines.
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

- [Architecture and decisions](docs/ARCHITECTURE.md)
- [Milestones and acceptance criteria](docs/ROADMAP.md)
- [Development and deployment](docs/DEVELOPMENT.md)

## Configuration

`.env.example` contains only local development values. Never commit `.env`, tokens, or real employee/customer records. Compose binds database/cache ports to loopback. Replace local credentials and use managed secrets, TLS, network restrictions, and validated deployment settings before hosting externally.

Dependency ranges express compatibility intent; `requirements.lock` records the tested environment. Update dependencies deliberately and rerun checks. No license has been selected yet.
