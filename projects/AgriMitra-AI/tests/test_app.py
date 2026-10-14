"""
test_app.py

End-to-end checks of the Flask routes using a throwaway SQLite database.

Run with:

    python -m unittest discover -s tests -v
"""

import os
import shutil
import sys
import tempfile
import unittest

# Use a temporary database BEFORE importing the app.
TMP_DIR = tempfile.mkdtemp(prefix="agrimitra_test_")
os.environ["AGRIMITRA_DB_PATH"] = os.path.join(TMP_DIR, "test.db")
os.environ["SECRET_KEY"] = "test-secret-key"

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import app as app_module

TEST_USER = "tester1"
TEST_PASSWORD = "testpass123"


class BaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app_module.app
        cls.app.config["TESTING"] = True
        cls.client = cls.app.test_client()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TMP_DIR, ignore_errors=True)

    def register_and_login(self):
        self.client.post("/register", json={
            "fullname": "Test Farmer",
            "userid": TEST_USER,
            "email": "tester1@example.com",
            "phone": "9876543210",
            "password": TEST_PASSWORD,
            "language": "en",
        })
        return self.client.post("/login", json={
            "userid": TEST_USER,
            "password": TEST_PASSWORD,
            "language": "en",
        })


class PublicPagesTest(BaseTestCase):
    def test_splash(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"AgriMitra AI", resp.data)

    def test_login_page(self):
        resp = self.client.get("/login")
        self.assertEqual(resp.status_code, 200)

    def test_register_page(self):
        resp = self.client.get("/register")
        self.assertEqual(resp.status_code, 200)

    def test_health(self):
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["status"], "ok")

    def test_404_page(self):
        resp = self.client.get("/no-such-page")
        self.assertEqual(resp.status_code, 404)

    def test_login_required_redirect(self):
        resp = self.client.get("/dashboard")
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/login", resp.headers["Location"])


class AuthTest(BaseTestCase):
    def test_register_login_flow(self):
        resp = self.register_and_login()
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.get_json()["success"])

    def test_register_duplicate_user(self):
        self.register_and_login()
        resp = self.client.post("/register", json={
            "fullname": "Another",
            "userid": TEST_USER,
            "email": "other@example.com",
            "password": "pass1234",
        })
        self.assertEqual(resp.status_code, 409)

    def test_login_wrong_password(self):
        self.register_and_login()
        resp = self.client.post("/login", json={
            "userid": TEST_USER,
            "password": "wrongpass",
            "language": "en",
        })
        self.assertEqual(resp.status_code, 401)

    def test_logout(self):
        self.register_and_login()
        resp = self.client.get("/logout")
        self.assertEqual(resp.status_code, 302)
        resp = self.client.get("/dashboard")
        self.assertIn("/login", resp.headers["Location"])


class PredictionApiTest(BaseTestCase):
    def setUp(self):
        self.register_and_login()

    def test_crop_prediction_valid(self):
        resp = self.client.post("/api/crop", json={
            "nitrogen": 90, "phosphorus": 42, "potassium": 43,
            "temperature": 20.88, "humidity": 82, "ph": 6.5, "rainfall": 202.9,
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data["success"])
        self.assertIn("crop", data)
        self.assertIn("confidence", data)

    def test_crop_prediction_zero_nutrients(self):
        resp = self.client.post("/api/crop", json={
            "nitrogen": 0, "phosphorus": 0, "potassium": 0,
            "temperature": 25, "humidity": 70, "ph": 6.5, "rainfall": 200,
        })
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.get_json()["success"])

    def test_crop_prediction_invalid_ph(self):
        resp = self.client.post("/api/crop", json={
            "nitrogen": 90, "phosphorus": 42, "potassium": 43,
            "temperature": 20.88, "humidity": 82, "ph": 99, "rainfall": 202.9,
        })
        self.assertEqual(resp.status_code, 400)

    def test_crop_prediction_missing_field(self):
        resp = self.client.post("/api/crop", json={
            "nitrogen": 90, "phosphorus": 42, "potassium": 43,
            "temperature": 20.88, "humidity": 82, "ph": 6.5,
        })
        self.assertEqual(resp.status_code, 400)

    def test_fertilizer_prediction_valid(self):
        resp = self.client.post("/api/fertilizer", json={
            "temperature": 26, "humidity": 52, "moisture": 38,
            "soil_type": "Sandy", "crop_type": "Maize",
            "nitrogen": 37, "potassium": 0, "phosphorous": 0,
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["fertilizer"], "Urea")

    def test_fertilizer_prediction_zero_phosphorous(self):
        # Regression: a valid 0 for phosphorous must not be rejected.
        resp = self.client.post("/api/fertilizer", json={
            "temperature": 26, "humidity": 52, "moisture": 38,
            "soil_type": "Sandy", "crop_type": "Maize",
            "nitrogen": 37, "potassium": 0, "phosphorous": 0,
        })
        self.assertEqual(resp.status_code, 200)

    def test_fertilizer_meta(self):
        resp = self.client.get("/api/fertilizer/meta")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data["success"])
        self.assertIn("Sandy", data["soil_types"])
        self.assertIn("Maize", data["crop_types"])

    def test_model_info(self):
        resp = self.client.get("/api/model-info")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("crop", data)
        self.assertIn("fertilizer", data)

    def test_combined_recommendation(self):
        resp = self.client.post("/api/recommend", json={
            "nitrogen": 90, "phosphorus": 42, "potassium": 43,
            "temperature": 20.88, "humidity": 82, "ph": 6.5, "rainfall": 202.9,
            "soil_type": "Sandy", "moisture": 50,
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data["success"])
        self.assertIn("crop", data)
        self.assertIn("fertilizer", data)

    def test_history_saved_and_returned(self):
        self.client.post("/api/crop", json={
            "nitrogen": 90, "phosphorus": 42, "potassium": 43,
            "temperature": 20.88, "humidity": 82, "ph": 6.5, "rainfall": 202.9,
        })
        resp = self.client.get("/api/history")
        self.assertEqual(resp.status_code, 200)
        history = resp.get_json()["history"]
        self.assertTrue(len(history) >= 1)
        self.assertEqual(history[0]["predicted_crop"], "Rice")


class LanguagePreferenceTest(BaseTestCase):
    def test_set_language_persists_across_pages(self):
        self.register_and_login()

        # Pick Kannada - this is what the frontend calls on every language change.
        resp = self.client.post("/api/language", json={"language": "kn"})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.get_json()["success"])

        # The very next page must render with the selected language.
        resp = self.client.get("/crop")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'data-language="kn"', resp.data)

        # Switching again works and overrides the stored preference.
        self.client.post("/api/language", json={"language": "ta"})
        resp = self.client.get("/dashboard")
        self.assertIn(b'data-language="ta"', resp.data)

    def test_set_language_rejects_unknown(self):
        self.register_and_login()
        resp = self.client.post("/api/language", json={"language": "xx"})
        self.assertEqual(resp.status_code, 400)


class AssistantTest(BaseTestCase):
    def test_assistant_knowledge_base(self):
        resp = self.client.post("/api/assistant", json={
            "question": "How should I irrigate my crops?",
            "language": "en",
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["source"], "knowledge-base")
        self.assertTrue(len(data["reply"]) > 0)

    def test_assistant_empty_question(self):
        resp = self.client.post("/api/assistant", json={"question": "", "language": "en"})
        self.assertEqual(resp.status_code, 400)

    def test_assistant_invalid_language_falls_back_to_english(self):
        resp = self.client.post("/api/assistant", json={
            "question": "Hello",
            "language": "xx",
        })
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.get_json()["success"])


if __name__ == "__main__":
    unittest.main()
