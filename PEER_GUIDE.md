# 🎓 Student Performance & Study-Hours Project: Peer Walkthrough Guide

Hey everyone! 👋  
Here is a straightforward, friendly explainer of what we built, what the data actually discovered, and how to test and run the project yourself. Use this guide to quickly understand the project before presentations, viva sessions, or group discussions.

---

## 📌 1. The Core Question (Why are we doing this?)

Every teacher, parent, and textbook tells students:  
> *"If you study more hours, you will get higher marks."*

As data science / computer science students, we wanted to put this belief to the test with real data:
1. **Does the data actually show that more study hours = higher grades?**
2. **If a student studies 10+ hours a week but gets a 0 because they got sick or dropped out, does that one weird score ruin the whole trend?** (This is the **outlier problem**).
3. **Can we scientifically claim that studying *causes* high marks?** *(Spoiler: No! We'll explain why).*

---

## 📂 2. The Dataset (In Plain English)

* **Source**: Real, anonymized records collected from two public high schools in Portugal by researchers Paulo Cortez and Alice Silva in 2008 (hosted on the public **UCI Machine Learning Repository**).
* **Total Students**: **1,044 students** ($395$ in Mathematics, $649$ in Portuguese Language).
* **Grading System**: Portuguese high schools grade on a **0 to 20 scale**:
  * **16 – 20**: Grade A (Excellent)
  * **14 – 15**: Grade B (Good)
  * **12 – 13**: Grade C (Satisfactory)
  * **10 – 11**: Grade D (Barely passing)
  * **0 – 9**: Grade F (Fail — **10 is the pass mark**)
* **Study Time Tiers**: Students reported their weekly study time in 4 categories:
  * Tier 1: `< 2 hours/week`
  * Tier 2: `2 – 5 hours/week` (most common: ~48% of students)
  * Tier 3: `5 – 10 hours/week`
  * Tier 4: `> 10 hours/week`

### 🔎 The Mystery of the 53 Zero-Scorers:
If you look at the raw data, **53 students scored exactly 0 on the final exam ($G3$)**.  
Did 53 students answer every single question wrong? No! In the Portuguese education system, if you miss too many classes or drop out during the semester, you are disqualified from sitting the final exam and given an administrative 0. These are textbook **outliers** that our code had to detect and handle.

---

## 💡 3. The Three Big Discoveries

### 1. There is a positive link, but it's surprisingly small!
* The Pearson correlation coefficient is **$r = +0.16$**.
* In statistics, $0$ means no link, and $+1.0$ means a perfect lockstep link.
* A value of **$+0.16$** means that studying more *is* linked to higher scores, but study time alone explains **less than 4% of the variation** in final grades ($R^2 \approx 0.026 - 0.036$). Over 96% of the outcome is governed by other things!

### 2. Does the link survive outliers? YES!
* When we stripped out the 53 students who scored 0 (the exam dropouts), the correlation didn't disappear—**it actually got STRONGER, jumping from $r = +0.16$ to $r = +0.19$**.
* When we used Tukey's Boxplot rule (IQR) or the Z-Score rule, the correlation stayed positive and steady (~$+0.19$).
* **Conclusion**: The upward trend is genuine. It is not an optical illusion caused by weird scores.

### 3. Why we CANNOT say "studying causes higher marks" (Correlation $\neq$ Causation)
* Just because two things go up together doesn't mean one causes the other.
* *Analogy*: People who wear expensive running shoes often finish 5K races faster. Does buying the shoes make your legs faster? No! Serious runners just happen to buy good shoes.
* In our student data:
  * **Past Performance ($G1$)**: A student's first-term grade predicts their final exam with an **$r > 0.80$** (that's massive!). Past foundation matters 10x more than cramming.
  * **Class Attendance**: Failing students averaged significantly more missed classes ($6.3$ absences vs. $5.4$ for passing students).
  * **Quality vs. Quantity**: Sitting at a desk for 8 hours scrolling through your phone is not the same as 2 hours of focused problem-solving.

---

## 🌐 4. Guided Tour of the Web Dashboard

When you launch `python app.py` and open `http://127.0.0.1:5000`, here is what each tab shows:

```
[Overview] ─── [Study Hours & G3] ─── [Course Comparison] ─── [Failures & Outliers] ─── [Student Roster]
```

1. **Executive Overview (`/`)**:
   * Stat cards: 1,044 students, 78.0% overall pass rate, 11.34/20 average grade.
   * Score distribution histogram showing the bell curve and the spike of 53 dropouts at 0.
   * Letter grade breakdown (A through F).
2. **Study Hours & G3 (`/study-hours`)**:
   * Jittered scatter plot showing every single student with a red linear regression trendline.
   * Boxplots showing group medians rising from 10 to 12 as study tiers increase.
   * Groupby summary table (average score for each study time bracket).
   * **Outlier Sensitivity Panel**: Shows side-by-side regression lines proving the trend survives.
   * Warning callout on the Causation Fallacy.
3. **Course Comparison (`/subjects`)**:
   * Mathematics vs. Portuguese side-by-side.
   * Portuguese students score higher (average 11.9 vs 10.4) with lower failure rates.
   * Math scores have much higher variance ($\sigma = 4.58$ vs $3.23$), proving math is a higher-risk subject.
4. **Failures & Outliers (`/failures`)**:
   * In-depth profile of failing students (higher absences, lower parental education).
   * **Z-Score vs. Tukey IQR comparison**: Evaluates why Tukey's IQR is better for test score data (grades are bounded 0–20 and not a clean Gaussian curve).
5. **Student Roster (`/students`)**:
   * Interactive table with search bar and dropdown filters (Filter by Math/Portuguese or Grade A–F).
   * Demonstrates our custom Python `StudentRecord` class in action.
6. **JSON API Export (`/api/summary`)**:
   * Returns clean, structured JSON data for external developers or automated grading scripts.

---

## 🛠️ 5. How the Code is Built

* **`models.py` (CO3 - Object-Oriented Programming)**:
  * Contains the `StudentRecord` class.
  * Why did we use a class instead of a regular dictionary? A dictionary is just a passive bucket of text. A class validates data when created, bundles business logic (like whether a score of 10 is passing or failing), and supports Python's special "dunder" methods (`__len__`, `__getitem__`, `__iter__`, `__repr__`).
* **`analysis.py` (CO1, CO2, CO4, CO5)**:
  * The computational brain. Cleans CSV data, computes NumPy statistics, runs Pandas groupby operations, and detects outliers using both Z-Score and Tukey's IQR.
* **`plots.py` (CO6 - Matplotlib)**:
  * Generates all 6 charts with clean styling and saves them as images to `static/img/`.
  * Every single chart includes a written interpretation explaining what the axes mean.
* **`app.py`**:
  * Flask web server delivering the UI and handling URL routing.
* **`main.py`**:
  * Standalone CLI runner. Runs the entire pipeline in the terminal with zero browser required.

---

## ⚡ 6. How to Run it on Your Own Laptop in 60 Seconds

1. Open PowerShell or Terminal and go to the project folder:
   ```bash
   cd student_dashboard
   ```
2. Run the web app:
   ```bash
   python app.py
   ```
3. Open your browser to **`http://127.0.0.1:5000`**!

*(Prefer running it in the terminal without a browser? Just run: `python main.py`)*  
*(Want to run the 17 automated tests? Run: `python -m unittest tests/test_pipeline.py`)*

---

## 🎓 7. Quick Viva / Presentation Q&A Cheat Sheet

* **Q: Why did you build a `StudentRecord` class instead of just using normal dicts?**  
  *A:* "A dictionary has no validation—it silently accepts bad or negative grades. Our `StudentRecord` class validates data at creation time, centralizes domain rules like grade-letter mapping, and provides dunder methods like `__len__` to count how many terms a student completed."
* **Q: Did the association survive outliers?**  
  *A:* "Yes! In the raw data, the correlation is $r = +0.16$. When we filter out the 53 exam absentees who scored 0, the correlation actually strengthens to $r = +0.19$, proving the positive trend is robust."
* **Q: Can we conclude that studying more causes higher grades?**  
  *A:* "No! That would be committing the causation fallacy. Study hours explain less than 4% of score variation. Confounding variables like prior academic foundation ($G1$ has an $r > 0.80$), attendance, and study quality play a vastly bigger role."
* **Q: Why did you prefer Tukey's IQR over Z-Score for finding outliers?**  
  *A:* "Z-Score assumes data is a symmetric normal distribution. But grades are bounded between 0 and 20, with an artificial spike at 0 from dropouts. The mean and standard deviation get distorted by those very zeros. Tukey's IQR uses percentiles ($Q1, Q3$), which are resistant to extreme values."
