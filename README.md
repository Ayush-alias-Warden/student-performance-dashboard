# 🎓 Student Performance & Study-Hours Analytics Dashboard

An educational data analytics web application and CLI pipeline developed for undergraduate sophomore Python curricula. The system investigates student assessment scores and reported study hours using anonymized records from secondary schools, visibly integrating all six course outcomes (**CO1–CO6**) and Bloom's taxonomy cognitive levels (**BL2–BL6**).

---

## 🚀 Quick Start: How to Run

### Prerequisites
* Python 3.9 or higher (tested on Python 3.11, 3.12, 3.13)
* Dependencies: `Flask`, `pandas`, `numpy`, `matplotlib`

```bash
# 1. Navigate to the project folder
cd student_dashboard

# 2. (Optional but recommended) Create and activate a virtual environment
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On macOS / Linux:
source venv/bin/activate

# 3. Install required packages
pip install -r requirements.txt
```

---

### Option A: Launch the Interactive Web Dashboard 🌐
To run the full web application with modern responsive UI and interactive filters:

```bash
python app.py
```
Open your web browser and navigate to:
👉 **`http://127.0.0.1:5000`**

#### Available Web Routes:
* `/` — **Executive Overview**: KPI metrics cards, grade distribution, and project outcomes.
* `/study-hours` — **Study Hours Deep Dive**: Scatter plot with regression line, boxplots, grouped table, outlier sensitivity comparison, and correlation vs. causation evaluation.
* `/subjects` — **Course Comparison**: Mathematics vs. Portuguese longitudinal comparison (G1 → G2 → G3).
* `/failures` — **Failure Cases & Outliers**: Dropout analysis (G3 = 0), risk profile comparisons, and Z-score vs. Tukey IQR evaluation.
* `/students` — **Student Directory (OOP)**: Searchable, paginated student records demonstrating OOP encapsulation.
* `/api/summary` — **JSON Export Endpoint**: Direct JSON serialization of analytical results.

---

### Option B: Run the Command-Line Pipeline (CLI) 💻
To run the end-to-end analytical pipeline directly in the terminal without opening a browser:

```bash
python main.py
```
This executes all 7 data processing steps, prints formatted tables to the terminal, regenerates all 6 Matplotlib charts, and exports the JSON summary to `data/summary_report.json`.

---

### Option C: Run the Automated Test Suite 🧪
To execute the comprehensive unit and integration test suite:

```bash
python -m unittest tests/test_pipeline.py
```
Runs 17 test cases covering all course outcomes, special methods, statistical functions, and HTTP routes.

---

## 📚 Course Outcomes (CO1 to CO6) Cross-Reference

| Outcome | Description | Demonstrated Implementation in Codebase | Primary File & Functions |
| :--- | :--- | :--- | :--- |
| **CO1** | **Procedural Control Flow & Functions** | Grade-banding branch logic (`if/elif/else`), grade validation bounds checking, ID generator loops, defensive error handling (`try/except`), pagination arithmetic. | `analysis.py` (`_g3_to_letter`, `validate_grades`, `load_dataset`)<br>`app.py` (`students`) |
| **CO2** | **Data Structures & File I/O** | Dictionaries, lists of tuples, parsing semicolon-delimited CSV files (`pd.read_csv`), exporting summary metrics as formatted JSON (`json.dump`). | `analysis.py` (`load_dataset`, `export_summary_json`)<br>`models.py` (`__iter__`) |
| **CO3** | **Classes & Special (Dunder) Methods** | `StudentRecord` and `StudentCohort` classes implementing `__init__`, `__len__`, `__getitem__`, `__iter__`, `__repr__`, and `__eq__`, plus properties (`grade_letter`, `is_passing`, `improvement`). | `models.py` (`StudentRecord`, `StudentCohort`) |
| **CO4** | **NumPy Arrays & Numerical Operations** | Array extraction (`.to_numpy()`), descriptive statistics (`np.mean`, `np.median`, `np.std`, `np.percentile`), Pearson correlation (`np.corrcoef`), polynomial regression fit (`np.polyfit`), vectorised boolean masking. | `analysis.py` (`compute_descriptive_stats`, `detect_outliers_zscore`, `detect_outliers_iqr`)<br>`plots.py` (`generate_study_vs_g3_scatter`) |
| **CO5** | **Pandas Series/DataFrames & CSV/JSON** | Multi-table concatenation (`pd.concat`), column engineering, categorical ordering, multi-column grouped aggregations (`groupby(['study_hours_label']).agg(...)`), DataFrame export to dictionary/JSON. | `analysis.py` (`load_all_data`, `study_hours_vs_performance`, `subject_comparison`) |
| **CO6** | **Matplotlib Plots & End-to-End Interpretation** | Publication-quality figures: scatter plot with OLS trendline, score histogram with summary lines, categorical grade bar chart, boxplot by study tier, grouped subject comparison, and dual outlier sensitivity panels. Each figure is paired with an end-to-end interpretation text block. | `plots.py` (`generate_all_plots`) |

---

## 🎯 Bloom's Taxonomy Cognitive Levels Evidence

* **BL2 (Understand / Explain)**:
  Every public function and class contains docstrings and UI explanations detailing inputs, data structures, axes, and geometric distributions (e.g., explaining why Portuguese grades use a 0–20 scale, and why `__len__` counts valid assessment periods).
* **BL3 (Apply / Implement)**:
  Working end-to-end pipeline ingesting 1,044 raw records, validating hygiene, deriving metrics, and serving results across web and CLI interfaces.
* **BL4 (Analyse / Investigate)**:
  Investigating failure cases (`analyse_failure_cases`): profiling 53 zero-scorers as exam absentees, tracking 90 students with significant grade drops ($G3 \le G1 - 4$), and contrasting school absences and parental education between failing and passing cohorts.
* **BL5 (Evaluate / Justify)**:
  1. **Algorithmic Evaluation**: Comparing Z-Score ($|z| > 2.0$) vs. Tukey's IQR fences ($1.5 \times IQR$) for outlier detection. Tukey's IQR is evaluated as superior because the bounded 20-point grade distribution with dropout clusters violates the Gaussian normality assumed by Z-scores.
  2. **Outlier Survival Evaluation**: Assessing whether the positive association between study time and score survives outlier removal (see detailed analysis below).
  3. **Causation vs. Correlation Evaluation**: Rigorous evaluation demonstrating why claiming study hours *cause* grade increases is a scientific fallacy ($R^2 < 0.04$, lurking variables).
  4. **Architecture Evaluation**: Evaluating why a dedicated `StudentRecord` domain class with dunder methods is architecturally superior to bare dictionaries.
* **BL6 (Create / Synthesize)**:
  Synthesizing all components into a coherent, production-grade, reproducible web dashboard application.

---

## 🔍 In-Depth Analytical Findings & Evaluation

### 1. Does the Association Between Study Hours and Score Survive Outliers?
**Finding:** **Yes, the positive association survives and actually strengthens.**

| Treatment Condition | Sample Size ($N$) | Pearson Correlation ($r$) | Coefficient of Determination ($R^2$) |
| :--- | :---: | :---: | :---: |
| **1. All Raw Data** | 1,044 | **+0.1616** | 2.61% |
| **2. Excluding G3 = 0 Dropouts** | 991 | **+0.1893** | 3.58% |
| **3. Excluding Tukey IQR Outliers** | 990 | **+0.1908** | 3.64% |
| **4. Excluding Z-Score Outliers** | 989 | **+0.1852** | 3.43% |

* **Empirical Takeaway**: The 53 zero-scorers in the dataset represent students who were absent from or disqualified before the final exam. These individuals reported various study habits but earned $G3 = 0$ for non-academic administrative reasons. When this cluster is properly isolated, the correlation coefficient increases from $+0.162$ to $+0.189$, proving that the positive slope is not an artifact of anomalous data points.

### 2. Why We Avoid Claiming Causation (BL5 Evaluation)
While the association is statistically consistent, **it must never be claimed that increasing study hours directly causes higher scores**:
1. **Negligible Effect Size ($R^2 < 0.04$)**: Reported study hours explain less than 4% of score variation. Over 96% of variance is governed by unmodeled factors.
2. **Confounding Variables**: Prior academic aptitude ($G1, G2$), student attendance (absences), and home academic reinforcement (`Medu`/`Fedu`) strongly correlate with both study habits and final outcomes.
3. **Study Efficiency vs. Seated Time**: The ordinal metric measures self-reported hours seated, not active retrieval, cognitive focus, or task comprehension.

### 3. OOP Design Evaluation: `StudentRecord` vs. Plain Dictionaries
* **Validation & Type Safety**: Prevents malformed rows (e.g. negative grades) from corrupting downstream calculations.
* **Encapsulation**: Domain business rules (e.g. $G3 \ge 10$ is passing, grade banding A–F) reside in a single authoritative class rather than duplicated across multiple modules.
* **Pythonic Protocol**: Dunder methods (`__len__`, `__getitem__`, `__iter__`, `__repr__`, `__eq__`) allow instances to seamlessly integrate into standard loops, dictionary constructors, and print diagnostics.

---

## 📖 Public Dataset Citation & References

This project uses the publicly available, anonymized secondary education dataset from the **UCI Machine Learning Repository**:

### Academic Citations (For Project Report)

#### APA Format:
> Cortez, P., & Silva, A. (2008). *Using Data Mining to Predict Secondary School Student Performance*. In A. Brito & J. Teixeira (Eds.), Proceedings of the 5th Annual Future Business Technology Conference (FUBUTEC 2008), pp. 5–12, Porto, Portugal. EUROSIS. https://doi.org/10.24432/C5TG7T

#### BibTeX Entry:
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

### Dataset Characteristics:
* **Source Institutions**: Two Portuguese public secondary schools (Gabriel Pereira and Mousinho da Silveira).
* **Subjects**: Mathematics (`student-mat.csv`, $N=395$) and Portuguese Language (`student-por.csv`, $N=649$). Total combined cohort: $N=1,044$.
* **Ethical Attribution**: Fully anonymized, consented survey and school registry records. Zero personally identifiable information (PII).
* **Target Features**: $G1$ (Period 1 mark, 0–20), $G2$ (Period 2 mark, 0–20), $G3$ (Final assessment mark, 0–20), and `studytime` (1: $<2$ hrs, 2: $2–5$ hrs, 3: $5–10$ hrs, 4: $>10$ hrs).
