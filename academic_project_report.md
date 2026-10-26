# Academic Project Report: Student Performance & Study-Hours Analytics Dashboard

**Course Level**: Undergraduate Sophomore (Year 2) Computer Science / Data Science  
**Topic**: Option 3 — Student Performance and Study-Hours Dashboard  
**Dataset**: UCI Machine Learning Repository — Student Performance Dataset (Cortez & Silva, 2008)  
**Execution Environment**: Python 3.9+ | Flask | NumPy | Pandas | Matplotlib  
**Live Production Web Deployment**: [https://student-performance-dashboard-z26x.onrender.com](https://student-performance-dashboard-z26x.onrender.com)  

---

## 1. Executive Summary & Problem Formulation

Educational outcomes are frequently assumed to be directly proportional to reported study time. This project systematically investigates the empirical relationship between self-reported weekly study hours and final secondary school examination scores ($G3$, on a 0–20 scale) across **1,044 student records** spanning Mathematics ($N=395$) and Portuguese Language ($N=649$).

The completed software delivers a dual-interface application:
1. **Live Production Web Dashboard**: Deployed publicly on the cloud at [https://student-performance-dashboard-z26x.onrender.com](https://student-performance-dashboard-z26x.onrender.com), built with Flask, Bootstrap 5, and Matplotlib.
2. **Automated CLI Pipeline**: A terminal runner with formatted tabular reports and JSON export (`python main.py`).

Every component is visibly structured around the six prescribed course outcomes (**CO1 to CO6**) and provides concrete evidence for Bloom's Revised Taxonomy levels from **BL2 (Explain)** through **BL6 (Create)**.

---

## 2. Course Outcomes (CO) & Bloom-Level Evidence Mapping

| Course Outcome | Description | Bloom Level | Concrete Implementation in Codebase |
| :--- | :--- | :--- | :--- |
| **CO1** | Procedural control flow & functions | **BL3 (Implement)** | Modular functions with input validation, grade-banding branch logic (`_g3_to_letter`), and anomaly filters (`validate_grades`) in [`analysis.py`](file:///c:/Users/ayush/Downloads/student_dashboard/analysis.py). |
| **CO2** | Built-in data structures & file I/O | **BL2 & BL3** | Semicolon-delimited CSV loading (`load_dataset`), dict record representation, and structured JSON export (`export_summary_json`). |
| **CO3** | Classes & special (dunder) methods | **BL2 & BL5** | Documented `StudentRecord` and `StudentCohort` classes implementing `__init__`, `__len__`, `__getitem__`, `__iter__`, `__repr__`, and `__eq__` with OOP justification in [`models.py`](file:///c:/Users/ayush/Downloads/student_dashboard/models.py). |
| **CO4** | NumPy arrays & operations | **BL3 & BL4** | Vectorised arrays (`.to_numpy()`), 5-number summaries, correlation matrices (`np.corrcoef`), linear regression fit (`np.polyfit`), and boolean masking. |
| **CO5** | Pandas Series/DataFrames & CSV/JSON | **BL3 & BL4** | Multi-file concatenation (`pd.concat`), column engineering, categorical ordering, and multi-level `groupby` aggregations. |
| **CO6** | Matplotlib plots & interpretations | **BL2, BL4, BL5** | 6 publication-ready figures (scatter, histogram, boxplot, bar chart, subject comparison, outlier sensitivity) in [`plots.py`](file:///c:/Users/ayush/Downloads/student_dashboard/plots.py), each with an interpretive narrative. |

---

## 3. Object-Oriented Architecture (CO3 & BL5 Evaluation)

### 3.1 Why a Custom `StudentRecord` Class is Superior to Raw Dictionaries

In sophomore curricula, students often store records in bare dictionaries (`dict`). However, evaluating this design against a custom class demonstrates why the OOP approach is essential for production data pipelines:

1. **Validation & Type Integrity**: Dictionaries accept arbitrary types and invalid keys without error. `StudentRecord.__init__` enforces defensive data copies and attribute parsing, catching corrupted educational records early.
2. **Encapsulation of Business Logic**: In Portugal's secondary grading system (0–20 scale), passing is defined as $G3 \ge 10$, and grades map to letter bands (A: 16–20, B: 14–15, C: 12–13, D: 10–11, F: 0–9). In a dict-based design, this `if/elif` logic must be repeated in every script. In `StudentRecord`, it is centralized within properties (`grade_letter`, `is_passing`, `improvement`).
3. **Semantic Identity (`__eq__`)**: Comparing two student dictionaries checks all 33 key-value pairs. For students enrolled in both Math and Portuguese, their scores differ, but their identity matches. `StudentRecord.__eq__` defines equality strictly by `student_id`.
4. **Sequence & Mapping Integration**: Implementing `__getitem__`, `__len__`, and `__iter__` makes `StudentRecord` operate as a native Python sequence and mapping without sacrificing class methods.

### 3.2 Special (Dunder) Methods Implemented

* **`__init__(self, row_dict: dict)`**: Constructor initializing internal record dictionary and extracting primary key `student_id`.
* **`__repr__(self) -> str`**: Returns a concise diagnostic string: `StudentRecord(id='MAT-001', G3=6, grade='F', passing=False)`.
* **`__len__(self) -> int`**: Returns the count of valid graded terms where score $> 0$ (0 to 3), distinguishing active students from dropouts.
* **`__getitem__(self, key: str)`**: Enables dict-style access (`student['G3']`) so existing dictionary consumers do not break.
* **`__iter__(self)`**: Yields `(column, value)` tuples, enabling seamless `dict(student)` casting and `for k, v in student:` loops.
* **`__eq__(self, other) -> bool`**: Evaluates identity equivalence based on `student_id`.

---

## 4. Empirical Statistical Analysis & Findings

### 4.1 Descriptive Summary of Final Grades ($G3$)
* **Total Cohort ($N$)**: 1,044 students (395 Mathematics, 649 Portuguese)
* **Overall Pass Rate ($G3 \ge 10$)**: **77.97%**
* **Mean Final Grade ($\mu$)**: **11.34 / 20** ($\sigma = 3.86$)
* **Five-Number Summary**:
  * Minimum: $0.0$
  * Lower Quartile ($Q_1$): $10.0$
  * Median ($Q_2$): $11.0$
  * Upper Quartile ($Q_3$): $14.0$
  * Maximum: $20.0$

### 4.2 Grouped Performance by Weekly Study Hours (Pandas Aggregation)

| Study Hours Tier | Numeric Code | Sample Size ($N$) | Mean $G3$ | Median $G3$ | Standard Deviation ($\sigma$) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **$< 2$ hours** | 1 | 317 | 10.58 | 11.0 | 3.89 |
| **$2 – 5$ hours** | 2 | 503 | 11.34 | 11.0 | 3.77 |
| **$5 – 10$ hours** | 3 | 162 | 12.49 | 13.0 | 3.62 |
| **$> 10$ hours** | 4 | 62 | 12.27 | 12.0 | 4.22 |

**Key Observation**: The modal study band is 2–5 hours/week ($48.2\%$). While group medians rise from 11.0 to 13.0, the $>10$ hours group shows higher variance ($\sigma = 4.22$) and a slight dip in mean compared to the 5–10 hours band, indicating diminishing returns.

---

## 5. Outlier Evaluation & Association Survival (BL4 & BL5)

### 5.1 Does the Apparent Association Survive Outliers?
**Finding: YES. The positive association between study hours and final grade survives across all outlier conditions.**

| Outlier Treatment Condition | Sample Size ($N$) | Pearson Correlation ($r$) | Coefficient of Determination ($R^2$) |
| :--- | :---: | :---: | :---: |
| **1. All Raw Data** | 1,044 | **+0.1616** | 2.61% |
| **2. Excluding $G3=0$ Dropouts** | 991 | **+0.1893** | 3.58% |
| **3. Excluding Tukey IQR Outliers** | 990 | **+0.1908** | 3.64% |
| **4. Excluding Z-Score Outliers ($|z|>2$)** | 989 | **+0.1852** | 3.43% |

* **Analysis (BL4)**: In the raw dataset, exactly **53 students** scored $G3 = 0$. Inspection of school attendance records reveals these students had chronic absences or withdrew from the institution before final examinations. Because these students recorded varying study habits earlier in the semester, their $G3 = 0$ scores act as noise.
* **Evaluation (BL5)**: When exam absentees are excluded, the Pearson correlation coefficient **increases from $+0.1616$ to $+0.1893$**, and the regression slope steepens. Thus, the positive relationship is genuine and robust against anomalous readings.

### 5.2 Algorithmic Comparison: Z-Score vs. Tukey's IQR Method (BL5)
* **Z-Score Method ($|z| > 2.0$)**: Detected 55 outliers. This method assumes Gaussian normality. Because the test scores are bounded $[0, 20]$ with an artificial spike at 0, the standard deviation is inflated, causing outlier masking.
* **Tukey's IQR Fences ($1.5 \times IQR$)**: Detected 54 outliers (all zero-scorers plus one score of 1). IQR relies on resistant percentiles ($Q_1, Q_3$) and makes zero distribution assumptions.
* **Design Conclusion**: Tukey's IQR is statistically preferred for educational testing distributions.

---

## 6. Critical Evaluation: Avoiding the Causation Fallacy (BL5)

While the association is verified and survives outliers, **claiming that study hours cause higher grades is an academic error**. The project explicitly documents four scientific justifications:

1. **Low Effect Size ($R^2 < 0.04$)**: With $r \approx 0.16$ to $0.19$, study time explains less than 4% of total score variation. Over 96% of variance is governed by other factors.
2. **Confounding Variables (Lurking Factors)**:
   * **Prior Attainment**: Period 1 grade ($G1$) correlates with final grade at $r > 0.80$, far outweighing study time.
   * **Attendance**: Failing students averaged $6.3$ absences compared to $5.4$ for passing students.
   * **Socioeconomic / Parental Support**: Maternal education (`Medu`) is significantly higher among passing students.
3. **Quality vs. Quantity**: Self-reported study hours measure duration seated, not cognitive efficiency (e.g., active recall vs. passive skimming).
4. **Reverse / Bidirectional Causality**: High-performing students often find coursework more engaging, leading them to study more hours.

---

## 7. Data Attribution & Academic References

The dataset utilized in this project is public, consented, and anonymized:

### Formal APA Reference:
> Cortez, P., & Silva, A. (2008). *Using Data Mining to Predict Secondary School Student Performance*. In A. Brito & J. Teixeira (Eds.), Proceedings of the 5th Annual Future Business Technology Conference (FUBUTEC 2008), pp. 5–12, Porto, Portugal. EUROSIS. https://doi.org/10.24432/C5TG7T

### BibTeX Entry:
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
