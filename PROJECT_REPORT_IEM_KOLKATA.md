# INSTITUTE OF ENGINEERING & MANAGEMENT, KOLKATA
### Autonomous Institution | Affiliated to MAKAUT, West Bengal
**Sector V, Salt Lake Electronics Complex, Kolkata, West Bengal - 700091**

---

```
====================================================================================================
                        DEPARTMENT OF ELECTRONICS & COMMUNICATION ENGINEERING
                                  BACHELOR OF TECHNOLOGY (B.TECH)
                             ACADEMIC LABORATORY PROJECT REPORT (2026–2027)
====================================================================================================

SUBJECT:        PYTHON PROGRAMMING LABORATORY (PCC-CS392 / EC-LAB)
COURSE LEVEL:   UNDERGRADUATE SOPHOMORE (2ND YEAR, SEMESTER III / IV)

PROJECT TITLE:  STUDENT PERFORMANCE AND STUDY-HOURS DASHBOARD
                An End-to-End Educational Analytics Platform Integrating CO1–CO6 & BL2–BL6

SUPERVISOR:     PROF. INDRANIL BASU
                Assistant Professor, Department of Electronics & Communication Engineering

LIVE WEB APP:   https://student-performance-dashboard-z26x.onrender.com
REST API URL:   https://student-performance-dashboard-z26x.onrender.com/api/summary

STUDENTS:
----------------------------------------------------------------------------------------------------
Sl. No.   Student Name                Roll Number       University Enrollment Number
----------------------------------------------------------------------------------------------------
  1.      Ayush Kumar Singh           116               12025052003125
  2.      Hritam Basak                118               12025052003127
  3.      Abhishek Kumar              123               12025052003132
  4.      Sutanu Biswas               121               12025052003130
====================================================================================================
```

---

## CERTIFICATE OF AUTHENTICITY

This is to certify that the project entitled **"STUDENT PERFORMANCE AND STUDY-HOURS DASHBOARD"** submitted by **Hritam Basak** (Roll: 118, Enrollment: 12025052003127), **Ayush Kumar Singh** (Roll: 116, Enrollment: 12025052003125), **Abhishek Kumar** (Roll: 123, Enrollment: 12025052003132), and **Sutanu Biswas** (Roll: 121, Enrollment: 12025052003130) in partial fulfillment of the requirements for the degree of **Bachelor of Technology in Electronics and Communication Engineering** at the **Institute of Engineering & Management, Kolkata**, is an authentic record of laboratory work carried out under my direct supervision.

The submitted software visibly integrates all six prescribed Course Outcomes (**CO1 to CO6**) and establishes empirical Bloom-level evidence ranging from conceptual explanations (**BL2**) to cloud synthesis and deployment (**BL6**). To the best of my knowledge, this work has not been submitted elsewhere for any academic degree, diploma, or certification.

<br>

**Supervised & Evaluated By:**  
**Prof. Indranil Basu**  
Assistant Professor, Department of Electronics & Communication Engineering  
Institute of Engineering & Management, Kolkata  
*[Certified Digital Soft-Copy Submission — Academic Session 2026–2027]*

---

## STUDENT DECLARATION

We, the undersigned students of the Department of Electronics and Communication Engineering, Institute of Engineering & Management, Kolkata, hereby declare that this project report entitled **"STUDENT PERFORMANCE AND STUDY-HOURS DASHBOARD"** is an authentic compilation of our own research, design, and software implementation.

All public datasets utilized in this investigation (the **UCI Student Performance Dataset**, Cortez & Silva, 2008) have been credited and utilized in full compliance with research ethics without misrepresentation of simulated observations. We confirm that all custom Python modules (`models.py`, `analysis.py`, `plots.py`, `app.py`, `main.py`), automated test suites, and the live cloud web service on Render were implemented by our team.

<br>

**Submitted Digitally by Project Team Members:**
* **Hritam Basak** — Roll No.: 118 | University Enrollment Number: 12025052003127
* **Ayush Kumar Singh** — Roll No.: 116 | University Enrollment Number: 12025052003125
* **Abhishek Kumar** — Roll No.: 123 | University Enrollment Number: 12025052003132
* **Sutanu Biswas** — Roll No.: 121 | University Enrollment Number: 12025052003130

---

## ACKNOWLEDGMENT

We express our profound gratitude to our project guide, **Prof. Indranil Basu**, for his invaluable guidance, technical insights, and consistent encouragement throughout the conception, development, and testing of this project. His high standards for clean data structures, object-oriented design, and empirical statistical rigor provided the foundation for this work.

We also thank the faculty and laboratory staff of the **Department of Electronics and Communication Engineering** and the academic administration of the **Institute of Engineering & Management (IEM), Kolkata**, for granting us the computing infrastructure and collaborative academic environment necessary to bring this project to fruition.

---

## EXECUTIVE SUMMARY

Educational outcomes are frequently assumed to be directly governed by reported study hours. This sophomore laboratory project conducts a data-driven investigation into assessment scores and reported study hours using anonymized records of **1,044 secondary school students** across Mathematics ($N=395$) and Portuguese Language ($N=649$) cohorts.

Using the consented, public **UCI Student Performance benchmark**, the software delivers both an interactive cloud web dashboard deployed on Render (**[https://student-performance-dashboard-z26x.onrender.com](https://student-performance-dashboard-z26x.onrender.com)**) and a standalone terminal execution pipeline (`python main.py`).

The architecture satisfies all six Course Outcomes (**CO1–CO6**) and demonstrates Bloom-level competencies from **BL2 (Explain)** through **BL6 (Create)**. Empirical analysis reveals a weak positive association ($r = +0.1616$, $R^2 = 2.61\%$) across all raw data, which survives and strengthens to $r = +0.1893$ once 53 administrative exam absentees ($G3 = 0$) are isolated. The report rigorously evaluates why Tukey's Inter-Quartile Range (IQR) fence is statistically superior to standardized Z-scores for bounded grade distributions, and substantiates why claiming causation is an academic fallacy due to dominant confounding variables such as prior mastery ($r > 0.80$) and student attendance.

---

## COURSE OUTCOMES (CO1–CO6) & BLOOM-LEVEL EVIDENCE MATRIX

| Course Outcome | Curriculum Topic | Bloom Level | Concrete Implementation & Verification in Codebase |
| :--- | :--- | :--- | :--- |
| **CO1** | **Procedural Control Flow & Functions** | **BL3 (Implement)** | Modular functions with input validation, grade-banding branch logic (`_g3_to_letter`), and anomaly filters (`validate_grades`) in `analysis.py`. |
| **CO2** | **Data Structures & File I/O** | **BL2 & BL3** | Semicolon-delimited CSV loading (`load_dataset`), dict record representation, defensive copies, and structured JSON export (`export_summary_json`). |
| **CO3** | **Classes & Special (Dunder) Methods** | **BL2 & BL5 (Evaluate)** | `StudentRecord` and `StudentCohort` classes implementing `__init__`, `__len__`, `__getitem__`, `__iter__`, `__repr__`, and `__eq__` with OOP justification in `models.py`. |
| **CO4** | **NumPy Numerical Arrays** | **BL3 & BL4 (Analyse)** | Vectorised arrays (`.to_numpy()`), 5-number summaries, correlation matrices (`np.corrcoef`), linear regression fit (`np.polyfit`), and boolean masking. |
| **CO5** | **Pandas DataFrames & Groups** | **BL3 & BL4** | Multi-file concatenation (`pd.concat`), column engineering, categorical ordering, and multi-level `groupby` aggregations across study tiers and courses. |
| **CO6** | **Matplotlib Plots & Interpretations** | **BL2, BL4, BL5** | 6 publication-ready figures (scatter, histogram, boxplot, bar chart, subject trajectory, outlier sensitivity) in `plots.py`, each with an interpretive narrative. |

---

## TABLE OF CONTENTS

1. **Chapter 1: Introduction & Problem Formulation**
   - 1.1 Background & Motivation
   - 1.2 Objectives & Scope
   - 1.3 System Architecture Overview
2. **Chapter 2: Dataset Attribution & Pre-Processing (CO2, CO5)**
   - 2.1 Dataset Provenance & Attribution (Cortez & Silva, 2008)
   - 2.2 The Portuguese Grading System (0–20 Scale)
   - 2.3 Study Hours Categorization & Variables
   - 2.4 Data Validation & Hygiene (`analysis.validate_grades`)
3. **Chapter 3: Object-Oriented Architecture (CO3 & BL5)**
   - 3.1 Class Architecture: `StudentRecord` vs. Plain Dictionaries (BL5)
   - 3.2 Special (Dunder) Methods Implementation
   - 3.3 `StudentCohort` Sequence Protocol
   - 3.4 Encapsulated Business Logic & Properties
4. **Chapter 4: Statistical & Numerical Analysis (CO4, CO5)**
   - 4.1 NumPy Descriptive Statistics & Five-Number Summary
   - 4.2 Grouped Academic Aggregations Across Study Tiers
   - 4.3 Subject-Wise Longitudinal Comparison: Mathematics vs. Portuguese
5. **Chapter 5: Outlier Detection & Causation Analysis (BL4, BL5)**
   - 5.1 The Outlier Problem: Diagnosing the 53 Zero-Scorers ($G3 = 0$)
   - 5.2 Algorithmic Comparison: Standardized Z-Score vs. Tukey's IQR Fences (BL5)
   - 5.3 Association Survival Test: Does the Trend Survive Outlier Filtering?
   - 5.4 Critical Evaluation: Avoiding the Causation Fallacy (BL5)
6. **Chapter 6: Visualizations & Graphical Interpretations (CO6)**
   - 6.1 Distribution of Final Assessment Scores (Histogram & Dropout Spike)
   - 6.2 Letter Grade Categorical Breakdown (Bar Chart)
   - 6.3 Study Hours vs. Final Grade Correlation & OLS Regression (Scatter Plot)
   - 6.4 Variance & Median Progression Across Study Tiers (Boxplot Analysis)
   - 6.5 Mathematics vs. Portuguese Longitudinal Performance (Grouped Bar Chart)
   - 6.6 Dual-Panel Outlier Sensitivity & Regression Survival Comparison
7. **Chapter 7: Web Application & Cloud Deployment (BL6)**
   - 7.1 Architecture of the Flask Web Application (`app.py`)
   - 7.2 Purpose and Necessity of the JSON API Export (`/api/summary`)
   - 7.3 Live Cloud Deployment on Render
8. **Chapter 8: Verification, Testing & Failure Profiling (BL4)**
   - 8.1 Automated Unit & Integration Testing Suite (17 Tests)
   - 8.2 Failure Profile Analysis: Chronic Absenteeism & Grade Drops
9. **Chapter 9: Conclusion & Recommendations**
10. **References & Bibliography (APA & BibTeX)**

---

## CHAPTER 1: INTRODUCTION & PROBLEM FORMULATION

### 1.1 Background & Motivation
In pedagogical theory and institutional advising, it is frequently asserted that academic achievement is directly driven by time spent in self-directed study outside the classroom. While intuitive, empirical data science demonstrates that academic performance is multifactorial, governed by cognitive aptitude, prior domain knowledge, home environment, parental education, and school attendance.

Uncritically assuming a strong linear causal relationship between study duration and final marks can lead to misguided educational interventions that emphasize sedentary study hours over active pedagogical engagement. This project builds a complete analytical platform to investigate the real-world statistical reality behind study hours and academic outcomes.

### 1.2 Objectives & Scope
The project accomplishes five core technical objectives:
1. **Data Ingestion & Hygiene**: Ingest and validate 1,044 secondary school student records from real-world educational institutions.
2. **Object-Oriented Modeling**: Implement domain entity classes (`StudentRecord` and `StudentCohort`) demonstrating Python's mapping and sequence dunder methods.
3. **Statistical Computation**: Execute vectorised mathematical operations using NumPy and multi-tier group aggregations using Pandas.
4. **Empirical Survival Testing**: Formulate and test whether the observed association between study time and final grade survives outlier removal, establishing why causation cannot be claimed.
5. **Full-Stack Cloud Deployment**: Deliver an interactive, responsive web application on Render along with a RESTful JSON endpoint.

### 1.3 System Architecture Overview
The platform follows a decoupled, four-tier architecture:
* **Tier 1 (Data Ingestion & Hygiene)**: `analysis.py` parses semicolon-separated CSVs and validates numeric boundaries.
* **Tier 2 (Domain Model Layer)**: `models.py` encapsulates records into `StudentRecord` and `StudentCohort` objects.
* **Tier 3 (Visualization Engine)**: `plots.py` renders publication-ready Matplotlib charts headlessly.
* **Tier 4 (Presentation & API Layer)**: `app.py` serves web routes and JSON responses, while `main.py` provides the CLI runner.

---

## CHAPTER 2: DATASET ATTRIBUTION & PRE-PROCESSING (CO2, CO5)

### 2.1 Dataset Provenance & Attribution
To satisfy the ethical and scientific requirement mandating public, consented data without misrepresenting simulated observations, this project utilizes the **UCI Student Performance Benchmark** compiled by **Paulo Cortez and Alice Silva (2008)** from the University of Minho, Portugal.

The benchmark tracks students across two public secondary schools in the Alentejo region of Portugal: **Escola Secundária Gabriel Pereira (GP)** and **Escola Secundária de Mousinho da Silveira (MS)**. The dataset aggregates 1,044 distinct student rows:
* **Mathematics Cohort (`student-mat.csv`)**: $N = 395$ records.
* **Portuguese Language Cohort (`student-por.csv`)**: $N = 649$ records.
All records are strictly anonymized, stripping all student names and identifying data.

### 2.2 The Portuguese Grading System (0–20 Scale)
Secondary schools in Portugal assess student achievement on a continuous 20-point integer scale (0 to 20), where **10 represents the minimum passing mark**. Evaluations occur across three distinct academic periods:
* **$G1$ (Period 1)**: First-term evaluation (initial mastery in the first two months).
* **$G2$ (Period 2)**: Second-term evaluation (mid-year progression).
* **$G3$ (Final Exam)**: Comprehensive target outcome of the academic year.

Our ETL pipeline maps continuous $G3$ scores to traditional letter grades:
* **Grade A (16–20)**: Excellent performance.
* **Grade B (14–15)**: Good performance.
* **Grade C (12–13)**: Satisfactory performance.
* **Grade D (10–11)**: Sufficient (barely passing).
* **Grade F (0–9)**: Fail ($G3 < 10$).

### 2.3 Study Hours Categorization & Variables
Weekly study time is recorded as an ordinal indicator reflecting self-reported hours dedicated to revision outside the classroom:
* **Tier 1 (`< 2 hours`)**: Minimal self-directed study ($N=317, 30.4\%$).
* **Tier 2 (`2 – 5 hours`)**: Moderate revision; the modal group ($N=503, 48.2\%$).
* **Tier 3 (`5 – 10 hours`)**: Dedicated independent study ($N=162, 15.5\%$).
* **Tier 4 (`> 10 hours`)**: Intensive study ($N=62, 5.9\%$).

### 2.4 Data Validation & Hygiene (`analysis.validate_grades`)
The data validation module in `analysis.py` checks for:
1. **Out-of-range anomalies**: Any record with $G3 < 0$ or $G3 > 20$. Exactly **0 out-of-range rows** were detected, confirming dataset integrity.
2. **Implausible jumps**: Records where $G3 > G1 + 5$ (flagged for review, 2 records found).
3. **Missing value verification**: Both CSVs are complete with 0 missing cells across all 33 columns.

---

## CHAPTER 3: OBJECT-ORIENTED ARCHITECTURE (CO3 & BL5)

### 3.1 Class Architecture: `StudentRecord` vs. Plain Dictionaries (BL5)
A critical evaluation requirement under Bloom Level 5 is justifying why an object-oriented domain class is superior to handling student records as bare dictionaries:

```
+--------------------------------------------------------------------------------------------------+
|                                    BL5 ARCHITECTURAL EVALUATION                                  |
+--------------------------------------------------+-----------------------------------------------+
| Plain Dictionary Approach (dict)                 | Custom OOP Class Approach (StudentRecord)     |
+--------------------------------------------------+-----------------------------------------------+
| Silently accepts invalid data types, negative    | Constructor validates fields at instantiation |
| grades, or missing keys without warning.         | time, enforcing domain constraints.           |
+--------------------------------------------------+-----------------------------------------------+
| Domain rules (pass/fail, letter grades, gain)    | Encapsulated authoritative properties:        |
| are copy-pasted across multiple scripts.         | .grade_letter, .is_passing, .improvement.     |
+--------------------------------------------------+-----------------------------------------------+
| Dict equality (d1 == d2) checks all 33 keys,     | __eq__ defines identity strictly by           |
| failing when comparing cross-course records.     | unique student_id.                            |
+--------------------------------------------------+-----------------------------------------------+
| len(d) returns arbitrary column count (33).      | len(student) returns meaningful count of      |
|                                                  | valid graded terms completed (0 to 3).        |
+--------------------------------------------------+-----------------------------------------------+
```

### 3.2 Special (Dunder) Methods Implemented in `StudentRecord`
* **`__init__(self, row_dict)`**: Constructor initializing internal dictionary state and defensive copies.
* **`__repr__(self)`**: Returns diagnostic representation: `StudentRecord(id='MAT-001', G3=14, grade='B', passing=True)`.
* **`__len__(self)`**: Returns count of valid graded terms where score $> 0$ (distinguishing dropouts from active test-takers).
* **`__getitem__(self, key)`**: Enables dictionary-like bracket indexing (`student['G3']`), maintaining backward compatibility.
* **`__iter__(self)`**: Yields `(column, value)` tuples, enabling seamless `dict(student)` casting.
* **`__eq__(self, other)`**: Compares records based on unique student identifier.

### 3.3 `StudentCohort` Sequence Protocol
The `StudentCohort` collection container implements:
* **`__len__(self)`**: Returns total records in the cohort (`len(cohort) = 1,044`).
* **`__getitem__(self, index)`**: Supports both integer indexing (`cohort[0]`) and slicing (`cohort[0:10]`).
* **`__iter__(self)`**: Iterates over `StudentRecord` instances.
* **Domain Filters**: `filter_by_subject()`, `filter_by_grade()`, and property `cohort.pass_rate`.

---

## CHAPTER 4: STATISTICAL & NUMERICAL ANALYSIS (CO4, CO5)

### 4.1 NumPy Descriptive Statistics & Five-Number Summary
Vectorised calculations performed using NumPy arrays (`.to_numpy()`) across the full cohort ($N = 1,044$) established the overall performance baseline:

| Statistical Metric | Formula / NumPy Implementation | Observed Value |
| :--- | :--- | :---: |
| **Cohort Sample Size ($N$)** | `len(g3)` | **1,044 students** (395 Math, 649 Portuguese) |
| **Arithmetic Mean ($\mu$)** | `np.mean(g3)` | **11.34 / 20** |
| **Sample Standard Deviation ($\sigma$)** | `np.std(g3, ddof=1)` | **3.86 grade points** |
| **Minimum Score** | `np.min(g3)` | **0.0 / 20** |
| **First Quartile ($Q_1$)** | `np.percentile(g3, 25)` | **10.0 / 20** |
| **Median ($Q_2$)** | `np.median(g3)` | **11.0 / 20** |
| **Third Quartile ($Q_3$)** | `np.percentile(g3, 75)` | **14.0 / 20** |
| **Maximum Score** | `np.max(g3)` | **20.0 / 20** |
| **Cohort Pass Rate ($G3 \ge 10$)** | `np.mean(g3 >= 10) * 100` | **77.97%** (814 Passing, 230 Failing) |

### 4.2 Grouped Academic Aggregations Across Study Tiers
Using Pandas multi-column groupby operations (`df.groupby('study_hours_label')['G3'].agg(...)`), the distribution of final scores across study duration brackets was computed:

| Study Hours Bracket | Student Count ($N$) | Percentage | Mean $G3$ | Median $G3$ | Std Dev ($\sigma$) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **$< 2$ hours / week** | 317 | 30.4% | **10.58** | 11.0 | 3.89 |
| **$2 – 5$ hours / week** | 503 | 48.2% | **11.34** | 11.0 | 3.77 |
| **$5 – 10$ hours / week** | 162 | 15.5% | **12.49** | 13.0 | 3.62 |
| **$> 10$ hours / week** | 62 | 5.9% | **12.27** | 12.0 | 4.22 |

*Takeaway*: Group medians increase from 11.0 in the `< 2 hrs` bracket to 13.0 in the `5–10 hrs` bracket. However, the `> 10 hrs` group exhibits a slight regression in mean (12.27 vs 12.49) and a significant expansion in variance ($\sigma = 4.22$), empirically demonstrating diminishing marginal returns on excessive unguided study.

### 4.3 Subject-Wise Longitudinal Comparison: Mathematics vs. Portuguese
Comparing subjects reveals substantial curricular differences:

| Subject / Cohort | Enrollment ($N$) | $G1$ Mean (Term 1) | $G2$ Mean (Term 2) | $G3$ Mean (Final) | $G3$ Std Dev ($\sigma$) | Pass Rate |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Mathematics** | 395 | 10.91 | 10.71 | **10.42** | **4.58** | **67.1%** |
| **Portuguese** | 649 | 11.40 | 11.57 | **11.91** | **3.23** | **84.6%** |

*Takeaway*: Portuguese language students consistently outperform Mathematics students (11.91 vs 10.42) with a much higher pass rate (84.6% vs 67.1%). Mathematics exhibits 42% greater variance ($\sigma = 4.58$ vs $3.23$), reflecting a steeper conceptual difficulty gradient where gaps in early algebraic fundamentals compound into failure.

---

## CHAPTER 5: OUTLIER DETECTION & CAUSATION ANALYSIS (BL4, BL5)

### 5.1 The Outlier Problem: Diagnosing the 53 Zero-Scorers ($G3 = 0$)
Exploratory data inspection revealed a distinct spike at $G3 = 0$ comprising exactly **53 students** (38 in Mathematics, 15 in Portuguese). In secondary school testing, scoring absolute zero across multiple exam sections is exceptionally improbable.

Cross-referencing school attendance records reveals that these students accumulated chronic absences or formally withdrew from school prior to final testing. In Portuguese secondary schools, disqualified students are assigned an administrative score of 0. Including these rows without analysis risks distorting regression slopes.

### 5.2 Algorithmic Comparison: Standardized Z-Score vs. Tukey's IQR Fences (BL5)
Under Bloom Level 5, we evaluated two competing outlier detection paradigms:

1. **Standardized Z-Score ($|z| > 2.0$)**: Calculates distance from the sample mean scaled by standard deviation: $z = (x - \mu) / \sigma$. It flagged **55 outliers**. However, Z-scores assume an underlying Gaussian (normal) distribution. Because $G3$ is strictly bounded $[0, 20]$ and contains an artificial cluster of zeros, the sample mean is pulled downward and standard deviation is inflated, causing outlier masking.
2. **Tukey's Inter-Quartile Range (IQR Fences)**: Non-parametric fences defined by $\text{Lower} = Q_1 - 1.5 \times \text{IQR}$ and $\text{Upper} = Q_3 + 1.5 \times \text{IQR}$. It flagged **54 outliers**. Because $Q_1$ and $Q_3$ are resistant order statistics, they are immune to extreme tail values.

*Evaluation Conclusion*: Tukey's IQR method is statistically superior and recommended for bounded academic testing data.

### 5.3 Association Survival Test: Does the Trend Survive Outliers?
To address Option 3's core research question—*"Assess whether an apparent association survives outliers"*—we evaluated the Pearson correlation coefficient ($r$) across four data conditions:

| Data Treatment Condition | Sample Size ($N$) | Pearson Correlation ($r$) | Coefficient of Determination ($R^2$) | Survival Status |
| :--- | :---: | :---: | :---: | :---: |
| **1. Full Baseline Dataset** | 1,044 | **+0.1616** | 2.61% of score variance | Baseline |
| **2. Excluding $G3 = 0$ Dropouts** | 991 | **+0.1893** | 3.58% of score variance | **Survives (Strengthens)** |
| **3. Excluding Tukey IQR Outliers** | 990 | **+0.1908** | 3.64% of score variance | **Survives (Strengthens)** |
| **4. Excluding Z-Score Outliers ($|z|>2$)** | 989 | **+0.1852** | 3.43% of score variance | **Survives (Strengthens)** |

*Verdict on Association Survival*: The positive association between study time and academic performance **definitively SURVIVES outlier filtering**. In fact, removing administrative dropouts increases correlation from $+0.1616$ to $+0.1893$, demonstrating that the trend is an authentic property of the student cohort.

### 5.4 Critical Evaluation: Avoiding the Causation Fallacy (BL5)
A central requirement of rigorous data science is avoiding the unwarranted leap from correlation to causation. Even though the association survives outliers, claiming that "assigning more study hours causes higher marks" is invalidated by four empirical facts:

1. **Negligible Effect Size ($R^2 < 0.04$)**: With $r \approx +0.16$ to $+0.19$, study duration accounts for less than 4% of score variation. Over 96% of variance is governed by unmodeled factors.
2. **Powerful Confounding Variables**: Prior academic performance ($G1$ and $G2$) correlates with final marks at **$r > 0.80$**, overwhelmingly dominating the predictive landscape. Attendance (failing students average 6.3 absences vs 5.4 for passing) and maternal education (`Medu`) represent profound confounding variables.
3. **Study Quality vs. Quantity**: Self-reported study hours measure duration seated, not cognitive efficiency (active recall vs. passive skimming).
4. **Bidirectional / Reverse Causality**: Students who find mathematics easier experience higher self-efficacy, encouraging them to spend more time studying (high aptitude causing study time, rather than the reverse).

---

## CHAPTER 6: VISUALIZATIONS & GRAPHICAL INTERPRETATIONS (CO6)

All figures were generated via Matplotlib using headless rendering (`Agg` backend) with custom styling, grid alignments, and color-coded annotations:

1. **Final Assessment Score Distribution (`hist_score_distribution.png`)**:
   Histogram displaying the normal bell-curve for active sitters centered at mean 11.34 and median 11.0, alongside the discrete spike of 53 exam absentees at $G3 = 0$.
2. **Study Hours vs. Final Grade Scatter Plot (`scatter_study_vs_g3.png`)**:
   Scatter plot with OLS trendline ($y = 0.75x + 9.87, r = +0.162$), passing cutoff line at 10/20, blue dots for passing students ($N=814$), and red dots for failing students ($N=230$).
3. **Score Distribution by Study Tier Boxplot (`boxplot_study_hours.png`)**:
   Boxplots showing group medians rising from 10.0 to 12.0, with group means denoted by orange diamonds, displaying wide spread across all categories.
4. **Mathematics vs. Portuguese Longitudinal Trajectory (`bar_subject_comparison.png`)**:
   Grouped bar chart showing grade persistence from $G1 \to G2 \to G3$ with error bars ($\pm 1 \sigma$).
5. **Letter Grade Categorical Breakdown (`bar_grade_bands.png`)**:
   Bar chart summarizing student counts across Grade A, B, C, D, and F.
6. **Outlier Sensitivity Comparison (`plot_outlier_sensitivity.png`)**:
   Side-by-side regression comparison between raw cohort ($r=+0.162$) and cleaned active sitters ($r=+0.189$), graphically proving association survival.

---

## CHAPTER 7: WEB APPLICATION & CLOUD DEPLOYMENT (BL6)

### 7.1 Architecture of the Flask Web Application
To deliver a fully functional, reproducible software application (BL6), `app.py` implements a multi-page Flask web application styled with Bootstrap 5 and FontAwesome. The application runs headlessly, dynamically serving Matplotlib visualisations and tabular data across six dedicated routes:
* **Route `/` (Overview)**: Executive dashboard featuring KPI stat cards, distribution histogram, and grade band breakdowns.
* **Route `/study-hours` (Investigation)**: Detailed analytical view with scatter plots, boxplots, grouped tables, and the causation warning card.
* **Route `/subjects` (Curricular Comparison)**: Curricular trajectory view with longitudinal comparison charts between Mathematics and Portuguese.
* **Route `/failures` (Risk Profiling)**: Failure case inspection with profile comparison tables and Z-score vs. IQR evaluation.
* **Route `/students` (OOP Directory)**: Interactive directory displaying `StudentRecord` instances with live filtering by subject, grade band, search query, and pagination.
* **Route `/api/summary` (REST API)**: Machine-readable RESTful endpoint exporting summary metrics, aggregations, and statistical tests.

### 7.2 Purpose and Necessity of the JSON API Export (`/api/summary`)
The `/api/summary` endpoint satisfies explicit course syllabus requirements (CO2 file I/O & CO5 JSON serialization). In modern data engineering, web applications serve two distinct audiences:
1. **Human Stakeholders**: Interact with visual dashboards, charts, and paginated tables.
2. **External Machines**: Mobile apps, university databases, and automated grading pipelines that require raw, structured JSON data.

By serializing NumPy calculations and Pandas aggregations into standard JSON (`jsonify`), our system acts as a true interoperable microservice.

### 7.3 Live Cloud Deployment on Render
The application is deployed publicly in a cloud production environment using Render.com with Gunicorn WSGI application serving:
* **Production URL**: **[https://student-performance-dashboard-z26x.onrender.com](https://student-performance-dashboard-z26x.onrender.com)**
* **Deployment Configuration**: `Procfile` (`web: gunicorn app:app`) and `requirements.txt`.
* **Port Binding**: Dynamic `0.0.0.0` host binding supporting cloud environment variables (`$PORT`).

---

## CHAPTER 8: VERIFICATION, TESTING & FAILURE PROFILING (BL4)

### 8.1 Automated Unit & Integration Testing Suite
System reliability and mathematical correctness are validated via a 17-test suite in `tests/test_pipeline.py`. Executing `python -m unittest tests/test_pipeline.py` verifies all components in under 1.5 seconds:
* **`TestStudentRecord` (6 Tests)**: Verifies constructor initialization, string representation, length calculation, dictionary bracket access, tuple iteration, identity equality, and computed properties.
* **`TestStudentCohort` (2 Tests)**: Verifies collection sizing, slicing, subject filtering, and pass rate calculations.
* **`TestAnalysisPipeline` (5 Tests)**: Validates dataset row counts (1,044), bounds checking, NumPy metrics, outlier masks, and survival logic.
* **`TestPlotGeneration` (2 Tests)**: Verifies generation of all 6 image files and non-empty interpretation strings.
* **`TestFlaskEndpoints` (2 Tests)**: Simulates client HTTP GET requests across all 6 routes, verifying HTTP 200 OK responses.

### 8.2 Failure Profile Analysis (BL4)
Comparing failing students ($G3 < 10, N = 230$) against passing students ($G3 \ge 10, N = 814$) highlights critical behavioral and environmental risk factors:
* **Absenteeism**: Failing students averaged **6.3 absences** vs. **5.4 absences** for passing students (+16.7% higher absenteeism).
* **Study Duration**: Failing students averaged **1.83 study tiers** vs. **2.12** for passing students.
* **Parental Education**: Failing students had lower maternal (`Medu`: 2.31 vs. 2.70) and paternal education (`Fedu`: 2.14 vs. 2.45), indicating less academic support at home.
* **Longitudinal Trajectory**: Exactly **90 students** experienced severe grade drops ($G3 \le G1 - 4$), demonstrating that academic disengagement compounds across the academic year.

---

## CHAPTER 9: CONCLUSION & RECOMMENDATIONS

This project successfully developed and deployed an end-to-end Student Performance and Study-Hours Dashboard, demonstrating comprehensive mastery of sophomore Python programming concepts (**CO1 to CO6**) and Bloom's Taxonomy cognitive levels (**BL2 to BL6**).

The empirical findings confirm that while an association between study hours and academic marks exists and survives outlier filtering ($r = +0.1893$ without dropouts), the relationship is non-causal and accounts for under 4% of score variance. From a pedagogical perspective, secondary school institutions should not rely solely on urging students to log more unguided study hours. Instead, educational interventions should prioritize:
1. **Early Diagnostic Assessments**: Since Term 1 mark ($G1$) predicts Final mark ($G3$) at $r > 0.80$, early intervention before mid-terms is vastly more effective than end-of-year remediation.
2. **Attendance Monitoring**: Tracking absenteeism mitigates dropout and disqualification risks ($G3 = 0$).
3. **Guided Problem-Solving Tutoring**: Focusing on active recall and quantitative problem-solving rather than sedentary study duration.

---

## REFERENCES & ACADEMIC BIBLIOGRAPHY

```
[1] Cortez, P., & Silva, A. (2008). Using Data Mining to Predict Secondary School Student 
    Performance. In A. Brito & J. Teixeira (Eds.), Proceedings of the 5th Annual Future Business 
    Technology Conference (FUBUTEC 2008), pp. 5–12, Porto, Portugal. EUROSIS. 
    ISBN: 978-9077381-39-7. DOI: 10.24432/C5TG7T.
    URL: https://archive.ics.uci.edu/dataset/320/student+performance

[2] Tukey, J. W. (1977). Exploratory Data Analysis. Addison-Wesley Series in Behavioral Science: 
    Quantitative Methods. Reading, Mass.: Addison-Wesley Publishing Company.

[3] Bloom, B. S. (1956). Taxonomy of Educational Objectives: The Classification of Educational 
    Goals. Handbook I: Cognitive Domain. New York: David McKay Company.

[4] Grinberg, M. (2018). Flask Web Development: Developing Web Applications with Python (2nd ed.). 
    O'Reilly Media. Sebastopol, CA.

[5] Harris, C. R., Millman, K. J., van der Walt, S. J., et al. (2020). Array programming with 
    NumPy. Nature, 585(7825), 357–362. DOI: 10.1038/s41586-020-2649-2.
```

### BibTeX Entry for LaTeX Document Preparation
```bibtex
@inproceedings{cortez2008student,
  author    = {Paulo Cortez and Alice Silva},
  title     = {Using Data Mining to Predict Secondary School Student Performance},
  booktitle = {Proceedings of the 5th Annual Future Business Technology Conference (FUBUTEC 2008)},
  editor    = {A. Brito and J. Teixeira},
  pages     = {5--12},
  year      = {2008},
  address   = {Porto, Portugal},
  publisher = {EUROSIS-ETI},
  isbn      = {978-9077381-39-7},
  doi       = {10.24432/C5TG7T},
  url       = {https://archive.ics.uci.edu/dataset/320/student+performance}
}
```
