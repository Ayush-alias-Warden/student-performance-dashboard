"""
main.py — Standalone CLI Pipeline for Student Performance Dashboard.

This script executes the entire educational analytics pipeline from the
command line, demonstrating all six Course Outcomes (CO1-CO6) and Bloom
levels (BL2-BL6) without requiring a browser.

Usage:
    python main.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Ensure local modules are importable
current_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(current_dir))

import analysis
import models
import plots


def print_banner(title: str) -> None:
    """Print formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def main() -> int:
    """Execute complete CLI analytical pipeline."""
    print_banner("STUDENT PERFORMANCE & STUDY-HOURS DASHBOARD (CLI)")
    print("Undergraduate Sophomore Python Project")
    print("Integrating CO1-CO6 and Bloom-level Evidence BL2-BL6")
    print("Dataset: UCI Student Performance (Cortez & Silva, 2008)")

    # -----------------------------------------------------------------------
    # Step 1: Data Loading & Validation (CO1, CO2, CO5)
    # -----------------------------------------------------------------------
    print_banner("STEP 1: Data Ingestion & Hygiene Validation (CO1, CO2, CO5)")
    df_raw = analysis.load_all_data()
    print(f"[+] Loaded raw dataset: {len(df_raw)} records across Math & Portuguese.")

    df_clean, val_report = analysis.validate_grades(df_raw)
    print(f"[+] Grade Validation Report:")
    print(f"    - Total records evaluated: {val_report['total_rows']}")
    print(f"    - Out-of-range rows (<0 or >20): {val_report['out_of_range_count']}")
    print(f"    - Implausible grade jumps (>5): {val_report['suspicious_jump_count']}")
    print(f"    - Clean validated rows: {val_report['clean_rows']}")

    # -----------------------------------------------------------------------
    # Step 2: Object-Oriented Modeling (CO3)
    # -----------------------------------------------------------------------
    print_banner("STEP 2: Object-Oriented Modeling with Special Methods (CO3)")
    cohort = analysis.dataframe_to_cohort(df_clean, name="Secondary School Cohort")
    print(f"[+] Instantiated StudentCohort collection: {repr(cohort)}")
    print(f"[+] Special method __len__: len(cohort) = {len(cohort)}")

    sample_student = cohort[0]
    print(f"[+] Special method __getitem__: cohort[0] = {repr(sample_student)}")
    print(f"[+] Special method __len__ on StudentRecord: len(student) = {len(sample_student)} graded terms")
    print(f"[+] Student properties:")
    print(f"    - Final Score G3: {sample_student['G3']}/20 (via __getitem__)")
    print(f"    - Letter Grade: {sample_student.grade_letter}")
    print(f"    - Study Tier: {sample_student.study_hours_label}")
    print(f"    - Passing Status: {sample_student.is_passing}")
    print(f"    - Improvement (G3 - G1): {sample_student.improvement}")
    print(f"[+] Cohort Overall Pass Rate: {cohort.pass_rate}%")

    # -----------------------------------------------------------------------
    # Step 3: Numerical & Descriptive Analysis (CO4)
    # -----------------------------------------------------------------------
    print_banner("STEP 3: NumPy Array Analytics & Summary Statistics (CO4)")
    stats = analysis.compute_descriptive_stats(df_clean)
    print(f"[+] Five-Number Summary + Parameters for Final Grade (G3):")
    print(f"    - Minimum:  {stats['min']:.1f}")
    print(f"    - Q1 (25%): {stats['Q1']:.1f}")
    print(f"    - Median:   {stats['median']:.1f}")
    print(f"    - Mean:     {stats['mean']:.2f} (Std Dev: {stats['std']:.2f})")
    print(f"    - Q3 (75%): {stats['Q3']:.1f}")
    print(f"    - Maximum:  {stats['max']:.1f}")
    print(f"    - Study Time vs G3 Pearson r: +{stats['studytime_g3_correlation']:.4f}")

    # -----------------------------------------------------------------------
    # Step 4: Grouped Aggregations (CO5)
    # -----------------------------------------------------------------------
    print_banner("STEP 4: Pandas Groupby Aggregations by Study Tier & Course (CO5)")
    study_summary = analysis.study_hours_vs_performance(df_clean)
    print("\n[+] Performance by Weekly Study Hours Tier:")
    print(study_summary.to_string(index=False))

    subject_summary = analysis.subject_comparison(df_clean)
    print("\n[+] Longitudinal Comparison: Mathematics vs Portuguese:")
    print(subject_summary.to_string(index=False))

    # -----------------------------------------------------------------------
    # Step 5: Matplotlib Plot Generation (CO6)
    # -----------------------------------------------------------------------
    print_banner("STEP 5: Matplotlib Visualizations & Interpretations (CO6)")
    generated_plots = plots.generate_all_plots(df_clean)
    for key, pdata in generated_plots.items():
        print(f"[+] Generated: {pdata['title']}")
        print(f"    Saved image to: {pdata['path']}")

    # -----------------------------------------------------------------------
    # Step 6: Outlier Evaluation & Association Survival (BL4, BL5)
    # -----------------------------------------------------------------------
    print_banner("STEP 6: Outlier Evaluation & Association Survival (BL4, BL5)")
    outlier_res = analysis.evaluate_association_under_outliers(df_clean)
    print(f"[+] Association Survival Assessment:")
    print(f"    - All Data Pearson r:        +{outlier_res['all_data_r']:.4f} (N={outlier_res['all_data_count']})")
    print(f"    - Excluding G3=0 Dropouts:   +{outlier_res['nonzero_r']:.4f} (N={outlier_res['nonzero_count']})")
    print(f"    - Excluding Tukey IQR:       +{outlier_res['iqr_clean_r']:.4f} (N={outlier_res['iqr_clean_count']})")
    print(f"    - Excluding Z-Score (|z|>2): +{outlier_res['zscore_clean_r']:.4f} (N={outlier_res['zscore_clean_count']})")
    print(f"\n[+] Survival Verdict: {outlier_res['verdict']}")

    print("\n" + "-" * 70)
    print(outlier_res["causation_evaluation"])
    print("-" * 70)

    # -----------------------------------------------------------------------
    # Step 7: Export JSON Summary (CO2, CO5)
    # -----------------------------------------------------------------------
    print_banner("STEP 7: Structured JSON Export (CO2, CO5)")
    json_path = current_dir / "data" / "summary_report.json"
    analysis.export_summary_json(df_clean, str(json_path))
    print(f"[+] Exported analytical summary to: {json_path}")

    print_banner("EXECUTION COMPLETE: ALL 6 OUTCOMES VISIBLY DEMONSTRATED")
    print("To launch the web dashboard, run:")
    print("    python app.py")
    print("And navigate to: http://127.0.0.1:5000 in your browser.")
    print("=" * 70 + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
