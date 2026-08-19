import unittest

from app import create_app


class AgentZeroUniversityTests(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def test_health_is_operational(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["service"], "Agent Zero University")
        self.assertEqual(response.json["status"], "operational")

    def test_curriculum_catalog_has_four_tiers(self):
        response = self.client.get("/api/v1/curriculum/tiers")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["count"], 4)

    def test_learning_plan_is_non_enrolling(self):
        response = self.client.post(
            "/api/v1/learning-plans",
            json={"learner_reference": "learner-001", "target_tier": "advanced"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["enrollment"], "not_started")

    def test_invalid_learning_plan_is_rejected(self):
        response = self.client.post(
            "/api/v1/learning-plans",
            json={"learner_reference": "", "target_tier": "not-a-tier"},
        )
        self.assertEqual(response.status_code, 400)

    def test_hardware_token_requires_real_identity_provider(self):
        response = self.client.post("/api/v1/access/hardware-token", json={"token": "test"})
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json["status"], "not_configured")


if __name__ == "__main__":
    unittest.main()
