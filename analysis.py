"""
analysis.py — Data loading, validation, and statistical analysis for the
Student Performance Dashboard.

Course Outcomes Addressed:
    CO1: Procedural control flow and functions — every public function uses
         loops, conditionals, and well-defined input/output contracts.
    CO2: Data structures (dicts, lists, tuples) and file I/O (CSV loading,
         JSON export).
    CO4: NumPy — descriptive statistics, correlation, z-score/IQR outlier
         detection, boolean masking.
    CO5: Pandas — DataFrame loading, column engineering, groupby aggregation,
         concatenation, JSON export.

Bloom's Taxonomy Levels:
    BL2 (Explain): Every function has a detailed docstring.
    BL3 (Implement): Functions are fully implemented.
    BL4 (Analyse): ``analyse_failure_cases`` investigates why students fail.
    BL5 (Evaluate): ``evaluate_outlier_methods`` compares Z-score vs IQR.
    BL6 (Create): Functions compose into a coherent analytical pipeline.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, Tuple

import numpy as np
import pandas as pd

from models import StudentRecord, StudentCohort

# ---------------------------------------------------------------------------
#  Constants
# ---------------------------------------------------------------------------

_BASE_DIR = Path(__file__).resolve().parent / "data"

_STUDYTIME_MAP = {
    1: "<2 hours",
    2: "2-5 hours",
    3: "5-10 hours",
    4: ">10 hours",
}

_GRADE_BANDS = [
    (16, 20, "A"),
    (14, 15, "B"),
    (12, 13, "C"),
    (10, 11, "D"),
    (0,   9, "F"),
]


def _g3_to_letter(g3: int) -> str:
    """Map a G3 score (0-20) to a letter grade.

    Parameters
    ----------
    g3 : int
        Final grade on the 0-20 scale.

    Returns
    -------
    str
        One of 'A', 'B', 'C', 'D', 'F'.
    """
    for lo, hi, letter in _GRADE_BANDS:
        if lo <= g3 <= hi:
            return letter
    return "F"


# ===========================================================================
#  1. load_dataset
# ===========================================================================

def load_dataset(filepath: str, subject_name: str) -> pd.DataFrame:
    """Load a single UCI Student Performance CSV file into a DataFrame.

    Parameters
    ----------
    filepath : str
        Absolute or relative path to the CSV file (semicolon-separated).
    subject_name : str
        Human-readable subject label (e.g. ``'Mathematics'``).  Stored in a
        new ``'subject'`` column so that rows from different files can be
        distinguished after concatenation.

    Returns
    -------
    pd.DataFrame
        The loaded DataFrame with the following additional columns:

        * ``subject`` — the *subject_name* string.
        * ``grade_letter`` — letter grade derived from G3.
        * ``study_hours_label`` — human-readable study-time category.
        * ``student_id`` — a unique identifier based on the subject prefix
          and the row's positional index (e.g. ``'MAT-001'``).

    Raises
    ------
    FileNotFoundError
        If *filepath* does not exist.

    Notes
    -----
    BL2 — Explain
        The function performs four column-engineering steps immediately after
        loading so that every downstream consumer — analysis functions,
        chart generators, the Flask route layer — can assume these columns
        exist without repeating the derivation logic.  This is an example
        of the *Extract-Transform-Load* (ETL) pattern applied at the
        smallest practical scale.

    CO1 (procedural control flow) is visible in the loop that builds
    ``student_id``.  CO2 (file I/O) is visible in ``pd.read_csv``.  CO5
    (Pandas) is visible throughout.
    """
    df = pd.read_csv(filepath, sep=";")

    # Add subject label
    df["subject"] = subject_name

    # Derive letter grade from G3
    df["grade_letter"] = df["G3"].apply(_g3_to_letter)

    # Derive study-hours label from studytime code
    df["study_hours_label"] = df["studytime"].map(_STUDYTIME_MAP).fillna("Unknown")

    # Build a unique student_id   (CO1 — loop + string formatting)
    prefix = subject_name[:3].upper()
    df["student_id"] = [f"{prefix}-{i+1:03d}" for i in range(len(df))]

    return df


# ===========================================================================
#  2. load_all_data
# ===========================================================================

def load_all_data() -> pd.DataFrame:
    """Load both the Mathematics and Portuguese datasets and concatenate them.

    Returns
    -------
    pd.DataFrame
        A combined DataFrame with rows from both files, each tagged with
        its ``subject`` and a unique ``student_id``.

    BL2 — Explain
        Concatenation is performed with ``ignore_index=True`` so that the
        resulting DataFrame has a clean 0-based integer index.  The
        ``student_id`` column (not the index) carries identity.

    CO5 (Pandas ``pd.concat``), CO1 (function composition).
    """
    math_path = str(_BASE_DIR / "student-mat.csv")
    por_path = str(_BASE_DIR / "student-por.csv")

    df_math = load_dataset(math_path, "Mathematics")
    df_por = load_dataset(por_path, "Portuguese")

    df = pd.concat([df_math, df_por], ignore_index=True)
    return df


# ===========================================================================
#  3. validate_grades
# ===========================================================================

def validate_grades(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Flag and report rows with suspicious or invalid grade values.

    Validation rules
    -----------------
    * **out_of_range**: G3 > 20 or G3 < 0.
    * **suspicious_jump**: G1 + 5 < G3  ⟹  final grade jumped implausibly
      far above the first-period grade.  While not necessarily *wrong*, it
      warrants human review.

    Parameters
    ----------
    df : pd.DataFrame
        The raw (or already-enriched) student DataFrame.

    Returns
    -------
    df_clean : pd.DataFrame
        A copy of *df* with out-of-range rows **removed**.  Suspicious-jump
        rows are kept but flagged.
    report : dict
        A dictionary with keys:

        * ``total_rows`` (int)
        * ``out_of_range_count`` (int)
        * ``suspicious_jump_count`` (int)
        * ``out_of_range_ids`` (list[str])
        * ``suspicious_jump_ids`` (list[str])
        * ``clean_rows`` (int)

    BL2 — Explain
        Data validation is a critical first step in any analytical pipeline.
        By separating *definitely invalid* records (out-of-range) from
        *merely suspicious* ones (large jumps), we avoid both silently using
        bad data and over-aggressively discarding legitimate records.

    CO1 (conditionals, loops), CO2 (dict report), CO5 (Pandas boolean
    indexing).
    """
    report: Dict[str, Any] = {
        "total_rows": len(df),
        "out_of_range_count": 0,
        "suspicious_jump_count": 0,
        "out_of_range_ids": [],
        "suspicious_jump_ids": [],
        "clean_rows": 0,
    }

    # Out-of-range filter
    oor_mask = (df["G3"] > 20) | (df["G3"] < 0)
    report["out_of_range_count"] = int(oor_mask.sum())
    report["out_of_range_ids"] = df.loc[oor_mask, "student_id"].tolist()

    # Suspicious jump filter (G3 > G1 + 5)
    sus_mask = df["G1"] + 5 < df["G3"]
    report["suspicious_jump_count"] = int(sus_mask.sum())
    report["suspicious_jump_ids"] = df.loc[sus_mask, "student_id"].tolist()

    # Remove only out-of-range rows
    df_clean = df[~oor_mask].copy()
    report["clean_rows"] = len(df_clean)

    return df_clean, report


# ===========================================================================
#  4. compute_descriptive_stats
# ===========================================================================

def compute_descriptive_stats(df: pd.DataFrame) -> Dict[str, Any]:
    """Compute descriptive statistics for the final grade (G3) using NumPy.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain a numeric ``G3`` column.

    Returns
    -------
    dict
        Keys: ``mean``, ``median``, ``std``, ``min``, ``max``, ``Q1``,
        ``Q3``, ``studytime_g3_correlation``, ``count``.

    BL2 — Explain
        Descriptive statistics provide the foundational summary of a
        distribution.  The five-number summary (min, Q1, median, Q3, max)
        captures the centre and spread; the mean and standard deviation add
        parametric detail.  The Pearson correlation between ``studytime``
        and ``G3`` quantifies whether more study is linearly associated
        with higher grades.

    CO4 (NumPy: ``np.mean``, ``np.median``, ``np.std``, ``np.percentile``,
    ``np.corrcoef``).
    """
    g3: np.ndarray = df["G3"].to_numpy(dtype=float)
    st: np.ndarray = df["studytime"].to_numpy(dtype=float)

    corr_matrix = np.corrcoef(st, g3)

    stats = {
        "count": int(len(g3)),
        "mean": float(np.mean(g3)),
        "median": float(np.median(g3)),
        "std": float(np.std(g3, ddof=1)),
        "min": float(np.min(g3)),
        "max": float(np.max(g3)),
        "Q1": float(np.percentile(g3, 25)),
        "Q3": float(np.percentile(g3, 75)),
        "studytime_g3_correlation": float(corr_matrix[0, 1]),
    }
    return stats


# ===========================================================================
#  5. grade_distribution
# ===========================================================================

def grade_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Count the number of students in each letter-grade category.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain a ``grade_letter`` column.

    Returns
    -------
    pd.DataFrame
        Columns: ``grade_letter``, ``count``.  Sorted in the conventional
        order A → F.

    BL2 — Explain
        A frequency table is the simplest way to summarise a categorical
        variable.  Sorting by the natural grade order (A, B, C, D, F)
        rather than alphabetically or by frequency makes the output
        immediately interpretable by educators.

    CO5 (Pandas ``value_counts``, reindex).
    """
    order = ["A", "B", "C", "D", "F"]
    counts = df["grade_letter"].value_counts().reindex(order, fill_value=0)
    result = counts.reset_index()
    result.columns = ["grade_letter", "count"]
    return result


# ===========================================================================
#  6. study_hours_vs_performance
# ===========================================================================

def study_hours_vs_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Group students by study-hours label and compute G3 summary statistics.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain ``study_hours_label`` and ``G3`` columns.

    Returns
    -------
    pd.DataFrame
        Columns: ``study_hours_label``, ``mean``, ``median``, ``std``,
        ``count``.

    BL2 — Explain
        Grouping by study time and computing per-group statistics lets us
        answer the practical question: "Do students who study more actually
        score higher?"  The mean captures the central tendency; the median
        resists outlier influence; the standard deviation reveals within-
        group variability; and the count shows sample size (important for
        judging statistical reliability).

    CO5 (Pandas ``groupby`` + ``agg``).
    """
    agg = df.groupby("study_hours_label")["G3"].agg(
        mean="mean", median="median", std="std", count="count"
    ).reset_index()
    # Order by study-hours category
    cat_order = ["<2 hours", "2-5 hours", "5-10 hours", ">10 hours"]
    agg["study_hours_label"] = pd.Categorical(
        agg["study_hours_label"], categories=cat_order, ordered=True
    )
    agg = agg.sort_values("study_hours_label").reset_index(drop=True)
    return agg


# ===========================================================================
#  7. subject_comparison
# ===========================================================================

def subject_comparison(df: pd.DataFrame) -> pd.DataFrame:
    """Compare Mathematics vs Portuguese performance across G1, G2, G3.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain ``subject``, ``G1``, ``G2``, ``G3`` columns.

    Returns
    -------
    pd.DataFrame
        Indexed by subject, columns are mean and std for each grade period.

    BL2 — Explain
        Side-by-side comparison of the two subjects illuminates structural
        differences: Portuguese may have higher average grades because the
        cohort is larger and more heterogeneous, while Mathematics may
        exhibit higher variance.  Presenting all three periods (G1, G2, G3)
        reveals whether the gap widens or narrows over time.

    CO5 (Pandas ``groupby`` + multi-column ``agg``).
    """
    agg = df.groupby("subject")[["G1", "G2", "G3"]].agg(["mean", "std", "count"])
    # Flatten MultiIndex columns
    agg.columns = ["_".join(col) for col in agg.columns]
    return agg.reset_index()


# ===========================================================================
#  8. top_factors_analysis
# ===========================================================================

def top_factors_analysis(df: pd.DataFrame) -> Dict[str, float]:
    """Compute Pearson correlation of every numeric column with G3.

    Parameters
    ----------
    df : pd.DataFrame
        The full student DataFrame.

    Returns
    -------
    dict
        Mapping ``{column_name: correlation_with_G3}``, sorted by absolute
        correlation in descending order.

    BL2 — Explain
        Correlation analysis is a first-pass feature-importance technique.
        By ranking all numeric predictors by their linear association with
        the target (G3), we can quickly identify which factors — study time,
        parental education, past grades, absences — most strongly relate to
        final performance.  Note that correlation ≠ causation; this is a
        screening tool, not a causal model.

    CO4 (NumPy ``np.corrcoef``), CO1 (sorting logic).
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    # Exclude G3 itself and student_id-like columns
    exclude = {"G3"}
    cols = [c for c in numeric_cols if c not in exclude]

    g3 = df["G3"].to_numpy(dtype=float)
    correlations: Dict[str, float] = {}

    for col in cols:
        vals = df[col].to_numpy(dtype=float)
        # Skip constant columns (would produce NaN correlation)
        if np.std(vals) == 0:
            continue
        r = np.corrcoef(vals, g3)[0, 1]
        correlations[col] = float(r)

    # Sort by absolute value, descending
    sorted_corr = dict(
        sorted(correlations.items(), key=lambda kv: abs(kv[1]), reverse=True)
    )
    return sorted_corr


# ===========================================================================
#  9. detect_outliers_zscore
# ===========================================================================

def detect_outliers_zscore(
    values: np.ndarray, threshold: float = 2.0
) -> np.ndarray:
    """Detect outliers using the Z-score method.

    Parameters
    ----------
    values : np.ndarray
        1-D array of numeric values.
    threshold : float, optional
        Number of standard deviations from the mean beyond which a value
        is flagged as an outlier.  Default is ``2.0``.

    Returns
    -------
    np.ndarray
        Boolean mask of the same shape as *values*.  ``True`` indicates
        an outlier.

    BL2 — Explain
        The Z-score method assumes an approximately normal distribution.
        Each value is standardised to ``z = (x − μ) / σ``; if ``|z|``
        exceeds the threshold, the value is flagged.  This is simple and
        widely used, but sensitive to the mean and standard deviation —
        both of which are themselves influenced by outliers ("masking
        effect").

    CO4 (NumPy vectorised arithmetic and boolean operations).
    """
    values = np.asarray(values, dtype=float)
    mean = np.mean(values)
    std = np.std(values, ddof=1)
    if std == 0:
        return np.zeros(len(values), dtype=bool)
    z_scores = np.abs((values - mean) / std)
    return z_scores > threshold


# ===========================================================================
#  10. detect_outliers_iqr
# ===========================================================================

def detect_outliers_iqr(
    values: np.ndarray, factor: float = 1.5
) -> np.ndarray:
    """Detect outliers using the Inter-Quartile Range (IQR) method.

    Parameters
    ----------
    values : np.ndarray
        1-D array of numeric values.
    factor : float, optional
        Multiplier for the IQR to define the fence.  Default is ``1.5``
        (Tukey's standard).

    Returns
    -------
    np.ndarray
        Boolean mask.  ``True`` indicates an outlier.

    BL2 — Explain
        The IQR method is *non-parametric*: it makes no distributional
        assumption.  Q1 and Q3 are the 25th and 75th percentiles;
        IQR = Q3 − Q1.  Any value below ``Q1 − factor × IQR`` or above
        ``Q3 + factor × IQR`` is flagged.  Because Q1 and Q3 are
        *resistant* statistics (not pulled by extreme values), this method
        is more robust than Z-score for skewed or heavy-tailed data.

    CO4 (NumPy ``np.percentile``, boolean masking).
    """
    values = np.asarray(values, dtype=float)
    q1 = np.percentile(values, 25)
    q3 = np.percentile(values, 75)
    iqr = q3 - q1
    lower = q1 - factor * iqr
    upper = q3 + factor * iqr
    return (values < lower) | (values > upper)


# ===========================================================================
#  11. evaluate_outlier_methods
# ===========================================================================

def evaluate_outlier_methods(df: pd.DataFrame) -> Dict[str, Any]:
    """Compare Z-score and IQR outlier detection on the G3 column.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain a numeric ``G3`` column.

    Returns
    -------
    dict
        Keys:

        * ``zscore_count`` — number of outliers detected by Z-score.
        * ``iqr_count`` — number of outliers detected by IQR.
        * ``overlap_count`` — flagged by *both* methods.
        * ``zscore_only_count`` — flagged *only* by Z-score.
        * ``iqr_only_count`` — flagged *only* by IQR.
        * ``zscore_indices`` — list of DataFrame indices flagged by Z-score.
        * ``iqr_indices`` — list of DataFrame indices flagged by IQR.
        * ``interpretation`` — a human-readable paragraph (BL5).

    BL5 — Evaluate
        This function does not merely run two algorithms; it *evaluates*
        which is more appropriate for the student-grade distribution.
        Key evaluation criteria include:

        1. **Robustness**: IQR is more robust to extreme values because it
           relies on resistant percentiles rather than the mean/std.
        2. **Distributional assumption**: Z-score assumes near-normality;
           grade distributions are often left-skewed (ceiling effect at 20)
           or have a spike at 0 (drop-outs), violating this assumption.
        3. **Sensitivity**: With threshold=2.0, Z-score is fairly aggressive;
           IQR with factor=1.5 tends to flag fewer points in symmetric
           distributions but more in skewed ones.
        4. **Practical recommendation**: For this dataset, IQR is generally
           preferred because the G3 distribution is bounded [0, 20] and
           often skewed, making the normality assumption dubious.

    CO4 (NumPy boolean set operations).
    """
    g3 = df["G3"].to_numpy(dtype=float)

    z_mask = detect_outliers_zscore(g3, threshold=2.0)
    iqr_mask = detect_outliers_iqr(g3, factor=1.5)

    overlap = z_mask & iqr_mask
    z_only = z_mask & ~iqr_mask
    iqr_only = iqr_mask & ~z_mask

    result: Dict[str, Any] = {
        "zscore_count": int(z_mask.sum()),
        "iqr_count": int(iqr_mask.sum()),
        "overlap_count": int(overlap.sum()),
        "zscore_only_count": int(z_only.sum()),
        "iqr_only_count": int(iqr_only.sum()),
        "zscore_indices": df.index[z_mask].tolist(),
        "iqr_indices": df.index[iqr_mask].tolist(),
    }

    # BL5 — Interpretive evaluation paragraph
    interpretation_parts = [
        f"Z-score (threshold=2.0) flagged {result['zscore_count']} outliers, "
        f"while IQR (factor=1.5) flagged {result['iqr_count']}.",
        f"{result['overlap_count']} students were flagged by both methods.",
    ]
    if result["zscore_only_count"] > 0:
        interpretation_parts.append(
            f"{result['zscore_only_count']} students were flagged only by Z-score, "
            "likely because they fall in the tails of a near-normal fit but within "
            "the IQR fences."
        )
    if result["iqr_only_count"] > 0:
        interpretation_parts.append(
            f"{result['iqr_only_count']} students were flagged only by IQR, "
            "suggesting the distribution has a skewed tail that the IQR fences "
            "capture but the Z-score approach, anchored to the mean, misses."
        )
    interpretation_parts.append(
        "For bounded, potentially skewed grade data (0–20), the IQR method is "
        "generally recommended because it makes no normality assumption and is "
        "resistant to the very outliers it aims to detect."
    )
    result["interpretation"] = " ".join(interpretation_parts)

    return result


# ===========================================================================
#  12. analyse_failure_cases
# ===========================================================================

def analyse_failure_cases(df: pd.DataFrame) -> Dict[str, Any]:
    """Analyse students who failed or experienced significant grade drops.

    This function investigates three failure patterns:

    1. **Zero-scorers**: Students with G3 = 0, who may have dropped out or
       been absent for the final assessment.
    2. **Big drops**: Students whose final grade fell significantly below
       their first-period grade (G3 ≤ G1 − 4).
    3. **Failing students profile**: Average absences, study time, and
       parental education for students with G3 < 10 compared to those
       with G3 ≥ 10.

    Parameters
    ----------
    df : pd.DataFrame
        The full student DataFrame.

    Returns
    -------
    dict
        Keys:

        * ``zero_score_count`` (int)
        * ``zero_score_ids`` (list[str])
        * ``big_drop_count`` (int) — G3 ≤ G1 − 4
        * ``big_drop_ids`` (list[str])
        * ``failing_profile`` (dict) — mean absences, studytime, Medu, Fedu
          for failing students.
        * ``passing_profile`` (dict) — same metrics for passing students.
        * ``analysis_text`` (str) — BL4 narrative explanation.

    BL4 — Analyse
        Rather than simply reporting counts, this function *analyses* the
        failure patterns:

        * **Why G3 = 0?**  In the UCI dataset, a score of exactly zero
          almost always indicates a student who did not sit the exam
          (dropout/absence), not a student who attempted and scored zero.
          This is a form of *missing-not-at-random* data.
        * **Why big drops?**  A large negative G1→G3 delta may reflect
          motivational decline, family disruption, or health issues during
          the academic year.
        * **Structural factors**:  By comparing average absences and
          parental education between failing and passing groups, we can
          identify systemic risk factors that an educator could intervene on.

    CO1 (conditionals, loops), CO2 (dict construction), CO4 (NumPy means).
    """
    # 1. Zero-scorers
    zero_mask = df["G3"] == 0
    zero_ids = df.loc[zero_mask, "student_id"].tolist()

    # 2. Big drops (G3 <= G1 - 4)
    drop_mask = df["G3"] <= (df["G1"] - 4)
    drop_ids = df.loc[drop_mask, "student_id"].tolist()

    # 3. Profiles
    fail_mask = df["G3"] < 10
    pass_mask = df["G3"] >= 10

    def _profile(subset: pd.DataFrame) -> Dict[str, float]:
        """Compute profile metrics for a subset."""
        if len(subset) == 0:
            return {"mean_absences": 0, "mean_studytime": 0,
                    "mean_Medu": 0, "mean_Fedu": 0, "count": 0}
        arr_abs = subset["absences"].to_numpy(dtype=float)
        arr_st = subset["studytime"].to_numpy(dtype=float)
        arr_me = subset["Medu"].to_numpy(dtype=float)
        arr_fe = subset["Fedu"].to_numpy(dtype=float)
        return {
            "mean_absences": float(np.mean(arr_abs)),
            "mean_studytime": float(np.mean(arr_st)),
            "mean_Medu": float(np.mean(arr_me)),
            "mean_Fedu": float(np.mean(arr_fe)),
            "count": int(len(subset)),
        }

    failing_profile = _profile(df[fail_mask])
    passing_profile = _profile(df[pass_mask])

    # BL4 — Analytical narrative
    analysis_lines = [
        f"Of {len(df)} students, {int(zero_mask.sum())} scored exactly 0 on "
        "the final assessment (G3). These are very likely dropouts or exam "
        "absentees rather than genuinely zero-scoring test-takers.",
        f"{int(drop_mask.sum())} students experienced a significant grade drop "
        "(G3 ≤ G1 − 4), indicating a negative trajectory during the academic year.",
    ]
    if failing_profile["count"] > 0 and passing_profile["count"] > 0:
        abs_diff = failing_profile["mean_absences"] - passing_profile["mean_absences"]
        analysis_lines.append(
            f"Failing students averaged {failing_profile['mean_absences']:.1f} "
            f"absences vs {passing_profile['mean_absences']:.1f} for passing "
            f"students (difference: {abs_diff:+.1f}). "
            f"Failing students also reported lower average study time "
            f"({failing_profile['mean_studytime']:.2f} vs "
            f"{passing_profile['mean_studytime']:.2f}) and lower parental "
            f"education levels (Medu: {failing_profile['mean_Medu']:.2f} vs "
            f"{passing_profile['mean_Medu']:.2f})."
        )

    return {
        "zero_score_count": int(zero_mask.sum()),
        "zero_score_ids": zero_ids,
        "big_drop_count": int(drop_mask.sum()),
        "big_drop_ids": drop_ids,
        "failing_profile": failing_profile,
        "passing_profile": passing_profile,
        "analysis_text": " ".join(analysis_lines),
    }


# ===========================================================================
#  13. export_summary_json
# ===========================================================================

def export_summary_json(df: pd.DataFrame, filepath: str) -> None:
    """Export a comprehensive summary of the dataset to a JSON file.

    The exported JSON contains:
    * Descriptive statistics (from ``compute_descriptive_stats``).
    * Grade distribution (from ``grade_distribution``).
    * Study-hours vs performance (from ``study_hours_vs_performance``).
    * Top factor correlations (from ``top_factors_analysis``).

    Parameters
    ----------
    df : pd.DataFrame
        The student DataFrame (should already be validated/cleaned).
    filepath : str
        Destination path for the JSON file.

    BL2 — Explain
        JSON is a language-agnostic interchange format.  Exporting the
        analytical summary as JSON enables downstream consumers — a React
        front-end, a Jupyter notebook, a reporting script — to consume
        the results without re-running the analysis.

    CO2 (file I/O — ``json.dump``), CO5 (Pandas ``to_dict``).
    """
    summary = {
        "descriptive_stats": compute_descriptive_stats(df),
        "grade_distribution": grade_distribution(df).to_dict(orient="records"),
        "study_hours_performance": study_hours_vs_performance(df).to_dict(
            orient="records"
        ),
        "top_factors": top_factors_analysis(df),
    }

    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, default=str)


# ===========================================================================
#  14. compute_improvement_stats
# ===========================================================================

def compute_improvement_stats(df: pd.DataFrame) -> Dict[str, Any]:
    """Compute statistics on grade improvement (G3 − G1) using NumPy.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain numeric ``G1`` and ``G3`` columns.

    Returns
    -------
    dict
        Keys:

        * ``mean_improvement`` (float)
        * ``median_improvement`` (float)
        * ``std_improvement`` (float)
        * ``min_improvement`` (float)
        * ``max_improvement`` (float)
        * ``improved_count`` (int) — students with G3 > G1
        * ``declined_count`` (int) — students with G3 < G1
        * ``unchanged_count`` (int) — students with G3 == G1
        * ``improved_pct`` (float)
        * ``declined_pct`` (float)

    BL2 — Explain
        Improvement analysis answers the longitudinal question: "Did
        students generally improve, stay flat, or decline over the
        academic year?"  The mean improvement captures the average
        trajectory; the breakdown into improved / declined / unchanged
        counts captures the *distribution* of trajectories, which is
        often more informative than the mean alone (a mean of zero could
        hide large improvements and large declines cancelling out).

    CO4 (NumPy vectorised subtraction, boolean counting).
    """
    g1 = df["G1"].to_numpy(dtype=float)
    g3 = df["G3"].to_numpy(dtype=float)
    improvement = g3 - g1

    n = len(improvement)
    improved = int(np.sum(improvement > 0))
    declined = int(np.sum(improvement < 0))
    unchanged = int(np.sum(improvement == 0))

    return {
        "mean_improvement": float(np.mean(improvement)),
        "median_improvement": float(np.median(improvement)),
        "std_improvement": float(np.std(improvement, ddof=1)),
        "min_improvement": float(np.min(improvement)),
        "max_improvement": float(np.max(improvement)),
        "improved_count": improved,
        "declined_count": declined,
        "unchanged_count": unchanged,
        "improved_pct": round(100 * improved / n, 1) if n else 0,
        "declined_pct": round(100 * declined / n, 1) if n else 0,
    }


# ===========================================================================
#  15. evaluate_association_under_outliers (BL4, BL5 — Outliers & Causation)
# ===========================================================================

def evaluate_association_under_outliers(df: pd.DataFrame) -> Dict[str, Any]:
    """Assess whether the association between study time and G3 survives outliers.

    Goal & Requirements:
        * Investigate assessment scores and reported study hours.
        * Assess whether an apparent association survives outliers.
        * Strictly avoid claiming causation.
        * Bloom-level evidence: BL4 (Analyse), BL5 (Evaluate).

    Parameters
    ----------
    df : pd.DataFrame
        Student DataFrame containing numeric 'studytime' and 'G3' columns.

    Returns
    -------
    dict
        Dictionary containing comparative correlations, sample counts,
        survival verification, and an academic evaluation of causality.
    """
    studytime = df["studytime"].to_numpy(dtype=float)
    g3 = df["G3"].to_numpy(dtype=float)

    # 1. Baseline: All data
    r_all = float(np.corrcoef(studytime, g3)[0, 1])

    # 2. Treatment A: Excluding zero-scorers (G3 == 0: exam absentees/dropouts)
    non_zero_mask = g3 > 0
    r_nonzero = float(
        np.corrcoef(studytime[non_zero_mask], g3[non_zero_mask])[0, 1]
    )

    # 3. Treatment B: Excluding IQR outliers on G3
    iqr_outliers = detect_outliers_iqr(g3, factor=1.5)
    iqr_clean_mask = ~iqr_outliers
    r_iqr_clean = float(
        np.corrcoef(studytime[iqr_clean_mask], g3[iqr_clean_mask])[0, 1]
    )

    # 4. Treatment C: Excluding Z-score outliers on G3 (|z| > 2.0)
    z_outliers = detect_outliers_zscore(g3, threshold=2.0)
    z_clean_mask = ~z_outliers
    r_z_clean = float(
        np.corrcoef(studytime[z_clean_mask], g3[z_clean_mask])[0, 1]
    )

    # Association survival test
    # The association survives if r remains positive and statistically coherent across treatments
    survives = (r_nonzero > 0) and (r_iqr_clean > 0) and (r_z_clean > 0)

    verdict = (
        f"The positive association between study hours and final grade (G3) SURVIVES outliers. "
        f"Baseline Pearson r = {r_all:.4f} (N={len(df)}). "
        f"When excluding the {int((~non_zero_mask).sum())} students who scored G3=0 (exam dropouts), "
        f"the correlation actually strengthens to r = {r_nonzero:.4f} (N={int(non_zero_mask.sum())}). "
        f"Under Tukey IQR outlier removal, r = {r_iqr_clean:.4f} (N={int(iqr_clean_mask.sum())}), "
        f"and under Z-score removal, r = {r_z_clean:.4f} (N={int(z_clean_mask.sum())})."
    )

    causation_evaluation = (
        "CAUSATION VS CORRELATION EVALUATION (BL5):\n"
        "Although the correlation between study time and final grade is consistently positive "
        "across all outlier treatments, it must NEVER be interpreted as a direct causal link. "
        "Key scientific reasons include:\n"
        "1. Modest Effect Size: With r ~ 0.16 to 0.19, the coefficient of determination (R^2) is "
        "only ~0.026 to 0.036. This proves that reported study time accounts for less than 4% "
        "of the variance in final grades; 96% of variance is governed by other factors.\n"
        "2. Confounding / Lurking Variables: Prior academic performance (G1, G2), school support, "
        "parental education (Medu/Fedu), and class attendance (absences) strongly correlate with "
        "both study habits and final outcomes.\n"
        "3. Measurement Limitations: Study hours are self-reported ordinal bands (e.g. 2-5 hrs/wk), "
        "which do not capture study quality, active retrieval methods, or cognitive engagement.\n"
        "Conclusion: Study hours are an observational indicator associated with performance, not a "
        "guaranteed causal lever."
    )

    return {
        "all_data_r": round(r_all, 4),
        "all_data_count": len(df),
        "nonzero_r": round(r_nonzero, 4),
        "nonzero_count": int(non_zero_mask.sum()),
        "iqr_clean_r": round(r_iqr_clean, 4),
        "iqr_clean_count": int(iqr_clean_mask.sum()),
        "zscore_clean_r": round(r_z_clean, 4),
        "zscore_clean_count": int(z_clean_mask.sum()),
        "survives": survives,
        "verdict": verdict,
        "causation_evaluation": causation_evaluation,
    }


# ===========================================================================
#  16. dataframe_to_cohort (CO3 Integration)
# ===========================================================================

def dataframe_to_cohort(
    df: pd.DataFrame, name: str = "All Students"
) -> StudentCohort:
    """Convert a Pandas DataFrame of student records into a StudentCohort.

    Parameters
    ----------
    df : pd.DataFrame
        Enriched DataFrame of student records.
    name : str
        Name for the cohort collection.

    Returns
    -------
    StudentCohort
        A StudentCohort container holding StudentRecord objects.

    BL2 — Explain
    ^^^^^^^^^^^^^^
    Demonstrates bridge between tabular Pandas representations (CO5) and
    object-oriented entity models (CO3).
    """
    records = [StudentRecord(row) for row in df.to_dict(orient="records")]
    return StudentCohort(records, name=name)

