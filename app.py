"""Agent Zero University service.

This service presents a four-tier curriculum catalog and validates learning-plan
requests. Hardware-token access remains unavailable until a real identity service
is formally approved and configured.
"""

from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone
from typing import Any

from flask import Flask, jsonify, request
from flask_cors import CORS

APP_NAME = "Agent Zero University"
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
TIERS = (
    {
        "id": "foundation",
        "title": "Foundation",
        "description": "Core operating principles and introductory learning pathways.",
        "modules": 4,
    },
    {
        "id": "practitioner",
        "title": "Practitioner",
        "description": "Applied workflows and supervised implementation practice.",
        "modules": 6,
    },
    {
        "id": "advanced",
        "title": "Advanced",
        "description": "Cross-functional systems design and advanced execution patterns.",
        "modules": 8,
    },
    {
        "id": "sovereign",
        "title": "Sovereign",
        "description": "Independent operational design and governance readiness.",
        "modules": 10,
    },
)
TIER_IDS = {tier["id"] for tier in TIERS}


def _allowed_origins() -> list[str]:
    raw_origins = os.getenv("CORS_ALLOWED_ORIGINS", "")
    return [origin.strip() for origin in raw_origins.split(",") if origin.strip()]


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _error(message: str, status: int) -> tuple[Any, int]:
    return jsonify({"status": "error", "message": message}), status


def create_app() -> Flask:
    """Create the HTTP application without enabling development-only settings."""
    app = Flask(__name__)
    app.config.update(JSON_SORT_KEYS=False, MAX_CONTENT_LENGTH=16 * 1024)

    origins = _allowed_origins()
    if origins:
        CORS(app, resources={r"/api/*": {"origins": origins}}, methods=["GET", "POST"])

    @app.get("/health")
    def health_check() -> tuple[Any, int]:
        return jsonify(
            {
                "service": APP_NAME,
                "version": APP_VERSION,
                "status": "operational",
                "timestamp": _timestamp(),
            }
        ), 200

    @app.get("/api/v1/curriculum/tiers")
    def list_tiers() -> tuple[Any, int]:
        return jsonify({"count": len(TIERS), "tiers": TIERS}), 200

    @app.post("/api/v1/learning-plans")
    def create_learning_plan() -> tuple[Any, int]:
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return _error("A JSON object is required.", 400)

        learner_reference = data.get("learner_reference")
        target_tier = data.get("target_tier")
        if not isinstance(learner_reference, str) or not learner_reference.strip() or len(learner_reference) > 80:
            return _error("learner_reference must be a non-empty string of at most 80 characters.", 400)
        if target_tier not in TIER_IDS:
            return _error("target_tier must identify a published curriculum tier.", 400)

        tier = next(item for item in TIERS if item["id"] == target_tier)
        return jsonify(
            {
                "status": "planned",
                "plan_id": str(uuid.uuid4()),
                "learner_reference": learner_reference.strip(),
                "target_tier": target_tier,
                "recommended_modules": tier["modules"],
                "enrollment": "not_started",
                "notice": "This endpoint prepares a learning plan only; no account is created and no payment is processed.",
                "timestamp": _timestamp(),
            }
        ), 200

    @app.post("/api/v1/access/hardware-token")
    def hardware_token_status() -> tuple[Any, int]:
        return jsonify(
            {
                "status": "not_configured",
                "message": "Hardware-token authentication is unavailable until an approved identity provider is configured.",
            }
        ), 503

    @app.errorhandler(404)
    def not_found(_: Any) -> tuple[Any, int]:
        return _error("The requested resource was not found.", 404)

    @app.errorhandler(413)
    def request_too_large(_: Any) -> tuple[Any, int]:
        return _error("Request body exceeds the 16 KB limit.", 413)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
