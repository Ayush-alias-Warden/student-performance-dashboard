"""
app.py — Flask Web Application for Student Performance & Study-Hours Dashboard.

Course Outcomes Addressed:
    CO1: Procedural control flow, routing functions, and query validation.
    CO2: Data structures (dictionaries, lists) and JSON API serialization.
    CO3: Instantiating and presenting StudentRecord & StudentCohort OOP objects.
    CO4: NumPy statistics computed dynamically and presented in dashboard cards.
    CO5: Pandas DataFrames converted to structured tabular templates.
    CO6: Serving publication-ready Matplotlib plots with embedded interpretations.

Bloom's Taxonomy Levels:
    BL2 (Explain): Detailed UI annotations, metric cards, and charts.
    BL3 (Implement): Fully functioning interactive web server.
    BL4 (Analyse): Outlier detection, failure pattern drill-down, subject comparisons.
    BL5 (Evaluate): Comparing Z-score vs IQR, evaluating association survival,
         and rigorously warning against correlation/causation conflation.
    BL6 (Create): A coherent, full-stack educational analytics web dashboard.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict

from flask import Flask, jsonify, render_template, request

import analysis
import models
import plots

# Initialise Flask application
app = Flask(__name__)
app.config["SECRET_KEY"] = "academic-student-dashboard-2026"

# Load and validate dataset on startup
print("[INFO] Loading and preparing student performance dataset...")
_raw_df = analysis.load_all_data()
_clean_df, _validation_report = analysis.validate_grades(_raw_df)

# Generate publication-grade Matplotlib visualisations (CO6)
print("[INFO] Generating Matplotlib figures and interpretations...")
_plot_metadata = plots.generate_all_plots(_clean_df)

# Instantiate StudentCohort container (CO3)
_cohort = analysis.dataframe_to_cohort(_clean_df, name="Secondary School Cohort")
print(f"[INFO] Cohort instantiated with {len(_cohort)} StudentRecord instances.")


# ---------------------------------------------------------------------------
#  Route 1: Overview / Home Dashboard
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    """Render executive overview dashboard.

    CO1 (routing & templating), CO4 (NumPy summary statistics),
    CO5 (grade distribution), CO6 (rendered plots).
    """
    stats = analysis.compute_descriptive_stats(_clean_df)
    pass_rate = _cohort.pass_rate

    return render_template(
        "index.html",
        active_page="index",
        stats=stats,
        pass_rate=pass_rate,
        plot_meta=_plot_metadata,
        validation_report=_validation_report,
    )


# ---------------------------------------------------------------------------
#  Route 2: Study Hours & Association Deep-Dive
# ---------------------------------------------------------------------------
@app.route("/study-hours")
def study_hours():
    """Investigate reported study hours vs final assessment scores.

    CO4 (NumPy correlation & regression), CO5 (Pandas groupby table),
    BL4 (outlier sensitivity), BL5 (evaluating association survival & causation).
    """
    study_table = analysis.study_hours_vs_performance(_clean_df).to_dict(
        orient="records"
    )
    eval_outliers = analysis.evaluate_association_under_outliers(_clean_df)

    return render_template(
        "study_hours.html",
        active_page="study_hours",
        study_table=study_table,
        eval_outliers=eval_outliers,
        plot_meta=_plot_metadata,
    )


# ---------------------------------------------------------------------------
#  Route 3: Course / Subject Comparison
# ---------------------------------------------------------------------------
@app.route("/subjects")
def subjects():
    """Compare Mathematics vs Portuguese student cohorts across G1, G2, G3.

    CO5 (multi-column groupby aggregation), CO6 (comparative grouped bar chart).
    """
    subject_table = analysis.subject_comparison(_clean_df).to_dict(
        orient="records"
    )

    return render_template(
        "subjects.html",
        active_page="subjects",
        subject_table=subject_table,
        plot_meta=_plot_metadata,
    )


# ---------------------------------------------------------------------------
#  Route 4: Failures & Outlier Detection Evaluation
# ---------------------------------------------------------------------------
@app.route("/failures")
def failures():
    """Analyse academic failure cases and evaluate outlier detection rules.

    BL4 (failure analysis: zero-scorers, grade drops, profile risks),
    BL5 (evaluating Z-score vs Tukey IQR fences).
    """
    failure_data = analysis.analyse_failure_cases(_clean_df)
    outlier_eval = analysis.evaluate_outlier_methods(_clean_df)

    return render_template(
        "failures.html",
        active_page="failures",
        failures=failure_data,
        outlier_eval=outlier_eval,
    )


# ---------------------------------------------------------------------------
#  Route 5: Student Directory & OOP Explorer (CO3)
# ---------------------------------------------------------------------------
@app.route("/students")
def students():
    """Browse student records with filtering, search, and pagination.

    CO1 (control flow & filtering logic), CO3 (StudentRecord OOP properties).
    """
    subject_filter = request.args.get("subject", "all")
    grade_filter = request.args.get("grade", "all")
    search_query = request.args.get("search", "").strip().lower()
    page = int(request.args.get("page", 1))
    per_page = 25

    # Filter using StudentCohort and list comprehension
    filtered_records = []
    for record in _cohort:
        # Subject filter
        if subject_filter != "all" and record.data.get("subject", "").lower() != subject_filter.lower():
            continue
        # Grade band filter
        if grade_filter != "all" and record.grade_letter != grade_filter.upper():
            continue
        # Search query filter (matches ID or school)
        if search_query:
            if search_query not in record.student_id.lower() and search_query not in str(record.data.get("school", "")).lower():
                continue
        filtered_records.append(record)

    # Simple pagination (CO1)
    total_records = len(filtered_records)
    total_pages = max(1, (total_records + per_page - 1) // per_page)
    page = max(1, min(page, total_pages))
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_records = filtered_records[start_idx:end_idx]

    return render_template(
        "students.html",
        active_page="students",
        records=paginated_records,
        page=page,
        total_pages=total_pages,
        current_subject=subject_filter,
        current_grade=grade_filter,
        search_query=search_query,
    )


# ---------------------------------------------------------------------------
#  Route 6: JSON Summary API Endpoint (CO2, CO5)
# ---------------------------------------------------------------------------
@app.route("/api/summary")
def api_summary():
    """Export summary metrics as JSON for external integration.

    CO2 (JSON serialization), CO4 (NumPy stats), CO5 (Pandas export).
    """
    summary = {
        "dataset_name": "UCI Student Performance (Cortez & Silva, 2008)",
        "total_records": len(_clean_df),
        "descriptive_stats": analysis.compute_descriptive_stats(_clean_df),
        "grade_distribution": analysis.grade_distribution(_clean_df).to_dict(
            orient="records"
        ),
        "study_hours_performance": analysis.study_hours_vs_performance(
            _clean_df
        ).to_dict(orient="records"),
        "association_outlier_evaluation": analysis.evaluate_association_under_outliers(
            _clean_df
        ),
        "outlier_methods_evaluation": analysis.evaluate_outlier_methods(_clean_df),
        "failure_analysis": analysis.analyse_failure_cases(_clean_df),
    }
    return jsonify(summary)


# ---------------------------------------------------------------------------
#  Main Runner
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "0.0.0.0")
    print(f"\n=======================================================")
    print(f"🚀 Student Performance Dashboard is running!")
    print(f"👉 Local Access: http://127.0.0.1:{port}")
    print(f"👉 Network Access: http://localhost:{port}")
    print(f"=======================================================\n")
    app.run(host=host, port=port, debug=False)
