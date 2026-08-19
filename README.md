# Agent Zero University

**Copyright & Ownership (c) 2026 Melvyn Douglas Braun (Prince Mel Braun). All Rights Reserved.**  
**Business Entity:** Dual Sovereign Braun Autonomous Ecosystems

Agent Zero University is a Flask service that publishes a four-tier curriculum catalog and validates learning-plan requests. It is deliberately **not** an enrollment, payment, learner-record, or identity-verification system.

## Implemented capabilities

| Endpoint | Purpose | Side effects |
| --- | --- | --- |
| `GET /health` | Liveness and release metadata | None |
| `GET /api/v1/curriculum/tiers` | Published four-tier curriculum catalog | None |
| `POST /api/v1/learning-plans` | Validates and returns a learning-plan recommendation | None; no account or enrollment is created |
| `POST /api/v1/access/hardware-token` | States access-integration readiness | Returns `503` until an approved identity provider exists |

The service rejects malformed JSON and oversized request bodies. Browser-origin access is disabled by default and can be restricted with `CORS_ALLOWED_ORIGINS` when a browser client is introduced.

## Local run

Create a virtual environment, install dependencies, and start the service:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
gunicorn --bind 0.0.0.0:${PORT:-5000} app:app
```

For local development only, `python app.py` is also supported. Do not use Flask development mode for a public deployment.

## Configuration

Copy `.env.example` to your deployment provider’s environment configuration. `APP_VERSION` is optional. Set `CORS_ALLOWED_ORIGINS` only to the exact HTTPS origins that need browser access. No identity, payment, or banking credentials belong in this repository.

## Release checks

Before releasing, run:

```bash
gunicorn --check-config app:app
curl http://127.0.0.1:5000/health
```

Enrollment, learner records, authentication, payments, and hardware-token verification require separately approved authenticated integrations, durable storage, authorization controls, webhook verification, rate limiting, and operational monitoring.

## Ownership

Unauthorized copying, distribution, modification, or commercial utilization of this platform, its tier structures, or security protocols without explicit written consent from the owner is prohibited.
