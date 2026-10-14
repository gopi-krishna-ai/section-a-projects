"""
test_ml.py

Verifies that the saved ML models load correctly and that predictions are
real model output (not hardcoded). Run with:

    python -m unittest discover -s tests -v
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ml.predict import (
    ModelLoadError,
    crop_model_info,
    fertilizer_categories,
    fertilizer_model_info,
    predict_crop,
    predict_fertilizer,
)


class CropModelTest(unittest.TestCase):
    def setUp(self):
        self.info = crop_model_info()

    def test_model_exists_and_reports_accuracy(self):
        self.assertIn("classes", self.info)
        self.assertIn("accuracy", self.info)
        self.assertGreater(self.info["accuracy"], 0.9)
        self.assertEqual(len(self.info["classes"]), 22)

    def test_predicts_known_training_row(self):
        # Row 1 of datasets/crop_recommendation.csv must still predict Rice.
        result = predict_crop({
            "nitrogen": 90,
            "phosphorus": 42,
            "potassium": 43,
            "temperature": 20.87974371,
            "humidity": 82.00274423,
            "ph": 6.502985292,
            "rainfall": 202.9355362,
        })
        self.assertEqual(result["crop"], "Rice")
        self.assertTrue(0 <= result["confidence"] <= 1)

    def test_accepts_zero_nutrient_values(self):
        result = predict_crop({
            "nitrogen": 0,
            "phosphorus": 0,
            "potassium": 0,
            "temperature": 25,
            "humidity": 70,
            "ph": 6.5,
            "rainfall": 200,
        })
        self.assertIn("crop", result)

    def test_missing_feature_raises(self):
        with self.assertRaises(ValueError):
            predict_crop({
                "nitrogen": 90,
                "phosphorus": 42,
                "potassium": 43,
                "temperature": 20.88,
                "humidity": 82,
                "ph": 6.5,
                # rainfall missing
            })


class FertilizerModelTest(unittest.TestCase):
    def setUp(self):
        self.info = fertilizer_model_info()
        self.cats = fertilizer_categories()

    def test_model_exists_and_reports_accuracy(self):
        self.assertIn("classes", self.info)
        self.assertIn("accuracy", self.info)
        self.assertEqual(len(self.info["classes"]), 7)

    def test_known_categories(self):
        self.assertIn("Sandy", self.cats["soil_types"])
        self.assertIn("Maize", self.cats["crop_types"])

    def test_predicts_known_training_row(self):
        # Row 1 of datasets/fertilizer_prediction.csv must still predict Urea.
        result = predict_fertilizer({
            "temperature": 26,
            "humidity": 52,
            "moisture": 38,
            "soil_type": "Sandy",
            "crop_type": "Maize",
            "nitrogen": 37,
            "potassium": 0,
            "phosphorous": 0,
        })
        self.assertEqual(result["fertilizer"], "Urea")
        self.assertTrue(0 <= result["confidence"] <= 1)

    def test_zero_values_are_valid(self):
        result = predict_fertilizer({
            "temperature": 29,
            "humidity": 52,
            "moisture": 45,
            "soil_type": "Loamy",
            "crop_type": "Sugarcane",
            "nitrogen": 12,
            "potassium": 0,
            "phosphorous": 36,
        })
        self.assertIn("fertilizer", result)


if __name__ == "__main__":
    unittest.main()
