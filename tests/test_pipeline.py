"""
test_pipeline.py — Comprehensive Unit & Integration Test Suite.

Verifies all six Course Outcomes (CO1 to CO6) and Bloom Levels (BL2 to BL6).

Usage:
    python -m unittest tests/test_pipeline.py
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
import pandas as pd

import analysis
import models
import plots
from app import app


class TestStudentRecord(unittest.TestCase):
    """CO3: Test StudentRecord class and special (dunder) methods."""

    def setUp(self):
        self.sample_row = {
            "student_id": "MAT-001",
            "school": "GP",
            "sex": "F",
            "age": 18,
            "studytime": 2,
            "failures": 0,
            "absences": 4,
            "G1": 10,
            "G2": 12,
            "G3": 14,
            "subject": "Mathematics",
        }
        self.student = models.StudentRecord(self.sample_row)

    def test_init_and_repr(self):
        """Test constructor and __repr__ string."""
        self.assertEqual(self.student.student_id, "MAT-001")
        self.assertIn("MAT-001", repr(self.student))
        self.assertIn("grade='B'", repr(self.student))

    def test_getitem(self):
        """Test __getitem__ dict-like access."""
        self.assertEqual(self.student["G3"], 14)
        self.assertEqual(self.student["subject"], "Mathematics")
        with self.assertRaises(KeyError):
            _ = self.student["non_existent_key"]

    def test_len(self):
        """Test __len__ returns number of graded terms with score > 0."""
        self.assertEqual(len(self.student), 3)

        zero_student = models.StudentRecord({"student_id": "MAT-002", "G1": 0, "G2": 0, "G3": 0})
        self.assertEqual(len(zero_student), 0)

    def test_iter(self):
        """Test __iter__ yields key-value tuples."""
        items = dict(list(self.student))
        self.assertEqual(items["student_id"], "MAT-001")
        self.assertEqual(items["G3"], 14)

    def test_equality(self):
        """Test __eq__ compares records by student_id."""
        same_student = models.StudentRecord({"student_id": "MAT-001", "G3": 20})
        different_student = models.StudentRecord({"student_id": "MAT-002", "G3": 14})
        self.assertEqual(self.student, same_student)
        self.assertNotEqual(self.student, different_student)

    def test_properties(self):
        """Test grade_letter, is_passing, improvement, study_hours_label."""
        self.assertEqual(self.student.grade_letter, "B")
        self.assertTrue(self.student.is_passing)
        self.assertEqual(self.student.improvement, 4)  # 14 - 10
        self.assertEqual(self.student.study_hours_label, "2-5 hours")


class TestStudentCohort(unittest.TestCase):
    """CO3: Test StudentCohort container sequence protocol."""

    def setUp(self):
        records = [
            models.StudentRecord({"student_id": "MAT-001", "G1": 10, "G3": 15, "subject": "Mathematics", "studytime": 2}),
            models.StudentRecord({"student_id": "MAT-002", "G1": 8, "G3": 8, "subject": "Mathematics", "studytime": 1}),
            models.StudentRecord({"student_id": "POR-001", "G1": 12, "G3": 16, "subject": "Portuguese", "studytime": 3}),
        ]
        self.cohort = models.StudentCohort(records, name="Test Cohort")

    def test_cohort_len_and_indexing(self):
        self.assertEqual(len(self.cohort), 3)
        self.assertEqual(self.cohort[0].student_id, "MAT-001")

        # Test slicing
        sliced = self.cohort[0:2]
        self.assertIsInstance(sliced, models.StudentCohort)
        self.assertEqual(len(sliced), 2)

    def test_cohort_filtering_and_pass_rate(self):
        math_cohort = self.cohort.filter_by_subject("Mathematics")
        self.assertEqual(len(math_cohort), 2)

        # 2 out of 3 students passed (15 >= 10, 8 < 10, 16 >= 10)
        self.assertAlmostEqual(self.cohort.pass_rate, 66.67, places=1)


class TestAnalysisPipeline(unittest.TestCase):
    """CO1, CO2, CO4, CO5: Test statistical analysis and validation pipeline."""

    @classmethod
    def setUpClass(cls):
        cls.df = analysis.load_all_data()
        cls.clean_df, cls.val_report = analysis.validate_grades(cls.df)

    def test_dataset_loading(self):
        """Test raw data contains 1044 rows across both subjects."""
        self.assertEqual(len(self.df), 1044)
        self.assertIn("Mathematics", self.df["subject"].values)
        self.assertIn("Portuguese", self.df["subject"].values)

    def test_grade_validation(self):
        """Test grade validation keeps valid range [0, 20]."""
        self.assertEqual(self.val_report["out_of_range_count"], 0)
        self.assertEqual(len(self.clean_df), 1044)

    def test_descriptive_stats_numpy(self):
        """CO4: Test NumPy summary statistics."""
        stats = analysis.compute_descriptive_stats(self.clean_df)
        self.assertIn("mean", stats)
        self.assertIn("median", stats)
        self.assertIn("std", stats)
        self.assertIn("studytime_g3_correlation", stats)
        self.assertTrue(0 <= stats["mean"] <= 20)
        self.assertTrue(stats["studytime_g3_correlation"] > 0)

    def test_outlier_detection_algorithms(self):
        """CO4, BL5: Test Z-score and Tukey IQR outlier functions."""
        g3 = self.clean_df["G3"].to_numpy(dtype=float)
        z_mask = analysis.detect_outliers_zscore(g3, threshold=2.0)
        iqr_mask = analysis.detect_outliers_iqr(g3, factor=1.5)

        self.assertEqual(len(z_mask), len(g3))
        self.assertEqual(len(iqr_mask), len(g3))
        self.assertTrue(np.sum(iqr_mask) > 0)

        outlier_eval = analysis.evaluate_outlier_methods(self.clean_df)
        self.assertGreater(outlier_eval["iqr_count"], 0)
        self.assertIn("interpretation", outlier_eval)

    def test_association_survival(self):
        """BL4, BL5: Test association survival under outliers."""
        survival_res = analysis.evaluate_association_under_outliers(self.clean_df)
        self.assertTrue(survival_res["survives"])
        self.assertGreater(survival_res["nonzero_r"], 0)
        self.assertGreater(survival_res["iqr_clean_r"], 0)
        self.assertIn("CAUSATION VS CORRELATION", survival_res["causation_evaluation"])

    def test_pandas_aggregations(self):
        """CO5: Test study hours and subject groupby summaries."""
        study_agg = analysis.study_hours_vs_performance(self.clean_df)
        self.assertEqual(len(study_agg), 4)

        subj_agg = analysis.subject_comparison(self.clean_df)
        self.assertEqual(len(subj_agg), 2)


class TestPlotGeneration(unittest.TestCase):
    """CO6: Test Matplotlib plot generation and file creation."""

    @classmethod
    def setUpClass(cls):
        cls.df = analysis.load_all_data()
        cls.clean_df, _ = analysis.validate_grades(cls.df)

    def test_generate_all_plots(self):
        results = plots.generate_all_plots(self.clean_df)
        self.assertEqual(len(results), 6)

        for key, pdata in results.items():
            self.assertTrue(os.path.exists(pdata["path"]))
            self.assertGreater(len(pdata["interpretation"]), 50)


class TestFlaskEndpoints(unittest.TestCase):
    """BL6: Test Flask web application routing and responses."""

    def setUp(self):
        self.client = app.test_client()

    def test_routes_status_200(self):
        endpoints = ["/", "/study-hours", "/subjects", "/failures", "/students", "/api/summary"]
        for ep in endpoints:
            response = self.client.get(ep)
            self.assertEqual(response.status_code, 200, f"Endpoint {ep} failed")

    def test_api_summary_json(self):
        response = self.client.get("/api/summary")
        data = json.loads(response.data)
        self.assertEqual(data["total_records"], 1044)
        self.assertIn("descriptive_stats", data)
        self.assertTrue(data["association_outlier_evaluation"]["survives"])


if __name__ == "__main__":
    unittest.main()
