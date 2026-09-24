# Development workflow

Use a separate virtual environment and Git repository for each product. The current dependency lock includes development and future-progression libraries; installed libraries are not implemented features.

## Daily work

```bash
git switch -c feat/describe-one-change
make services
make test
make lint
git diff
git add <specific-files>
git commit -m "feat: describe the working behavior"
git push -u origin HEAD
```

Review the diff for secrets and unrelated files before committing. Make one focused change, its tests, and relevant documentation per commit. Do not backdate commits or claim planned features as delivered. Initial history reflects actual scaffold, API, tests, infrastructure, and documentation work.

## Local service isolation

CareReady: API 8002, PostgreSQL 5434, Redis 6382. Compose uses its own named volume and network. Local credentials are deliberately non-production. Copy `.env.example` without overwriting an existing `.env`.

## Dependency updates

```bash
.venv/bin/python -m pip install --upgrade -e '.[dev,progression]'
.venv/bin/python -m pip freeze --exclude-editable > requirements.lock
make test
make lint
```

The lock is a pinned Python environment snapshot, not a cryptographically verified supply-chain lock. Validate on CI Linux as well as the local Mac. For production, derive a runtime-only lock and scan dependencies/images.

## Container smoke test

```bash
docker build -t careready-api:dev .
docker run --rm -p 127.0.0.1:8002:8000 --env-file .env careready-api:dev
```

Inside a container, 127.0.0.1 means the container itself. For readiness with Mac-hosted Compose ports, set DATABASE_URL and REDIS_URL to host.docker.internal instead of 127.0.0.1, or attach an API service to the Compose network and use postgres:5432 and redis:6379. The Dockerfile is a starting recipe; the supplied Compose file runs dependencies only.

## Planned hosted release

Deploy API and workers separately; run Alembic as a controlled release step once migrations exist. Configure managed PostgreSQL, private Redis, secret storage, TLS, allowed hosts/origins, rate limiting, structured logs, metrics, backups, and restore drills. Use /health/live for restarts and /health/ready for traffic gating. No hosted deployment is provisioned by this starter.

## Timestamp-aligned development

Use BUILD_PROGRESSION.md for watch ranges and exact commit checkpoints, and PROGRESS.md to record real dates, SHAs, and evidence. Video time is a pause marker; commit only after the relevant behavior and tests pass. Existing setup commits are already complete and must not be recreated.
