"""
models.py — StudentRecord class for the Student Performance Dashboard.

Course Outcomes Addressed:
    CO3: Classes and special methods (__init__, __repr__, __len__, __getitem__,
         __iter__, __eq__) with properties and detailed docstrings.

Bloom's Taxonomy Levels:
    BL2 (Explain): Each method and property includes a docstring that explains
         its purpose, parameters, return value, and design rationale.
    BL5 (Evaluate): The class-level docstring below evaluates why an OOP
         approach with a dedicated class is superior to using plain dicts.

Why a StudentRecord class is better than a plain dictionary (BL5 — Evaluate):
------------------------------------------------------------------------
1. **Type Safety & Validation**: A class constructor can validate incoming data
   at creation time (e.g. ensuring grades are numeric, student_id is present).
   A plain dict silently accepts any key/value, making silent data-corruption
   bugs likely in a 33-column educational dataset.

2. **Encapsulated Derived Logic**: Properties such as ``grade_letter``,
   ``is_passing``, and ``improvement`` encode domain rules in one authoritative
   place.  With dicts, the same if/elif grade-banding logic would be copy-pasted
   across every module that needs a letter grade, violating DRY and inviting
   inconsistency.

3. **Rich Comparison & Identity**: ``__eq__`` lets us define *what it means* for
   two student records to be the same (matching ``student_id``), which is
   essential when merging Math and Portuguese datasets that may share students.
   Dict equality compares *all* keys and values, which is semantically wrong
   here.

4. **Iteration & Introspection**: ``__iter__`` and ``__len__`` give each record
   a Pythonic interface that integrates with for-loops, unpacking, and built-in
   functions.  A dict's ``__iter__`` yields *keys only*, which is rarely what
   analytical code wants.

5. **Readable Debugging**: ``__repr__`` provides a human-friendly summary in the
   REPL and in log files, whereas ``repr(dict)`` dumps every column — unusable
   for a 33-column row.

6. **Extensibility**: Adding new computed fields (e.g. weighted GPA, risk score)
   requires only a new ``@property``; no calling code changes.  With dicts, you
   would need to mutate every dict or wrap every access in a helper function.

In summary, the class trades a small amount of boilerplate for significant gains
in correctness, readability, maintainability, and extensibility — all critical
qualities in a data-analysis application.
"""

from __future__ import annotations



class StudentRecord:
    """Represents a single student's record from the UCI Student Performance dataset.

    This class wraps a single CSV row (parsed as a dictionary) and exposes
    domain-specific properties and Pythonic special methods so that downstream
    analysis and charting code can work with clean, validated, self-documenting
    objects rather than raw dictionaries.

    Attributes
    ----------
    data : dict
        The raw key-value pairs from the CSV row (all original columns).
    student_id : str
        A unique identifier assigned during data loading (e.g. "MAT-042").

    See Also
    --------
    analysis.load_dataset : Factory that creates StudentRecord instances.
    """

    # ------------------------------------------------------------------ #
    #  Mapping tables (class-level constants)
    # ------------------------------------------------------------------ #

    _STUDYTIME_LABELS = {
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

    # ------------------------------------------------------------------ #
    #  Special methods (CO3)
    # ------------------------------------------------------------------ #

    def __init__(self, row_dict: dict) -> None:
        """Initialise a StudentRecord from a dictionary row.

        Parameters
        ----------
        row_dict : dict
            A dictionary whose keys are column names from the UCI dataset
            (e.g. 'school', 'sex', 'age', …, 'G1', 'G2', 'G3') and whose
            values are the corresponding cell values.  Numeric columns are
            expected to be already cast to ``int`` or ``float`` by the CSV
            reader / Pandas loader.

        Notes
        -----
        The constructor stores the entire dictionary internally so that
        any original column can still be retrieved via ``__getitem__``.
        It also extracts ``student_id`` as a first-class attribute for
        fast identity checks in ``__eq__``.

        BL2 — Explain
        ^^^^^^^^^^^^^^
        ``__init__`` is the *constructor* in Python's data model.  It is
        called automatically when ``StudentRecord(row)`` is evaluated.
        Storing ``row_dict`` directly (rather than copying each field to a
        separate attribute) keeps the class flexible: if the CSV gains a
        new column tomorrow, no code change is needed here.
        """
        self.data: dict = dict(row_dict)  # defensive copy
        self.student_id: str = str(row_dict.get("student_id", "UNKNOWN"))

    def __repr__(self) -> str:
        """Return a concise, human-readable summary of this student record.

        Returns
        -------
        str
            A string of the form
            ``StudentRecord(id='MAT-042', G3=15, grade='B', passing=True)``.

        BL2 — Explain
        ^^^^^^^^^^^^^^
        ``__repr__`` is invoked by ``repr()`` and by the interactive REPL
        when an object is echoed.  A good ``__repr__`` should be
        *unambiguous* and ideally look like a valid constructor call or
        at least convey the most important state at a glance.  For a
        student record the most important facts are the ID, final grade,
        letter grade, and pass/fail status.
        """
        g3 = self.data.get("G3", "?")
        return (
            f"StudentRecord(id='{self.student_id}', G3={g3}, "
            f"grade='{self.grade_letter}', passing={self.is_passing})"
        )

    def __len__(self) -> int:
        """Return the number of graded assessments (G1, G2, G3) that are > 0.

        Returns
        -------
        int
            An integer between 0 and 3 inclusive.

        BL2 — Explain
        ^^^^^^^^^^^^^^
        ``__len__`` is called by the built-in ``len()`` function.  Here it
        answers the question "how many meaningful grade data-points does
        this student have?"  A value of 0 may indicate a student who
        dropped out before any assessment; a value of 3 means all three
        periodic grades are recorded.  This is useful for filtering
        incomplete records during analysis.
        """
        count = 0
        for key in ("G1", "G2", "G3"):
            val = self.data.get(key, 0)
            try:
                if float(val) > 0:
                    count += 1
            except (ValueError, TypeError):
                pass
        return count

    def __getitem__(self, key: str):
        """Access any attribute by name, dict-style.

        Parameters
        ----------
        key : str
            The column name (e.g. ``'G3'``, ``'school'``, ``'absences'``).

        Returns
        -------
        object
            The stored value for *key*.

        Raises
        ------
        KeyError
            If *key* is not present in the record.

        BL2 — Explain
        ^^^^^^^^^^^^^^
        ``__getitem__`` is the hook behind the ``obj[key]`` syntax.
        Implementing it lets analytical code treat a ``StudentRecord``
        like a dictionary when convenient (``student['G3']``), while
        still benefiting from the class's properties and methods.
        """
        return self.data[key]

    def __iter__(self):
        """Iterate over ``(attribute_name, value)`` pairs.

        Yields
        ------
        tuple[str, object]
            Each element is a ``(column_name, cell_value)`` pair, in the
            order the columns appear in the underlying dictionary.

        BL2 — Explain
        ^^^^^^^^^^^^^^
        ``__iter__`` makes the object usable in a ``for`` loop and with
        ``dict()`` conversion::

            for col, val in student:
                print(col, val)

        Unlike a plain dict (which yields keys only), this yields
        key-value *tuples*, which is almost always what analysis code
        actually needs.
        """
        for key, value in self.data.items():
            yield (key, value)

    def __eq__(self, other) -> bool:
        """Compare two StudentRecord instances by ``student_id``.

        Parameters
        ----------
        other : StudentRecord
            Another record to compare against.

        Returns
        -------
        bool
            ``True`` if both records share the same ``student_id``.

        BL2 — Explain
        ^^^^^^^^^^^^^^
        Identity in this domain is defined by the ``student_id`` field,
        not by grade equality.  Two records for the same student in Math
        and Portuguese would have different G3 scores but should still be
        recognised as the *same person* when merging datasets.
        """
        if not isinstance(other, StudentRecord):
            return NotImplemented
        return self.student_id == other.student_id

    # ------------------------------------------------------------------ #
    #  Properties
    # ------------------------------------------------------------------ #

    @property
    def grade_letter(self) -> str:
        """Convert the final grade G3 (0-20 scale) to a letter grade.

        Mapping
        -------
        * **A**: 16–20  (Excellent)
        * **B**: 14–15  (Good)
        * **C**: 12–13  (Satisfactory)
        * **D**: 10–11  (Sufficient — still passing)
        * **F**: 0–9    (Fail)

        Returns
        -------
        str
            One of ``'A'``, ``'B'``, ``'C'``, ``'D'``, ``'F'``.

        BL2 — Explain
        ^^^^^^^^^^^^^^
        The Portuguese grading system uses a 0–20 numeric scale.  This
        property translates that into a familiar letter-grade scheme so
        that bar charts, group-by operations, and dashboard cards can
        display an intuitive categorical label.
        """
        try:
            g3 = int(self.data.get("G3", 0))
        except (ValueError, TypeError):
            return "F"
        for lo, hi, letter in self._GRADE_BANDS:
            if lo <= g3 <= hi:
                return letter
        return "F"

    @property
    def study_hours_label(self) -> str:
        """Convert the numeric ``studytime`` code to a human-readable label.

        Mapping
        -------
        * 1 → ``"<2 hours"``
        * 2 → ``"2-5 hours"``
        * 3 → ``"5-10 hours"``
        * 4 → ``">10 hours"``

        Returns
        -------
        str
            A descriptive string for the student's weekly study time.

        BL2 — Explain
        ^^^^^^^^^^^^^^
        The raw ``studytime`` column is an ordinal code (1–4).  Displaying
        ``1`` on a chart axis is meaningless to stakeholders; this property
        provides the semantically rich label that appears in tooltips,
        legends, and grouped tables.
        """
        try:
            code = int(self.data.get("studytime", 0))
        except (ValueError, TypeError):
            return "Unknown"
        return self._STUDYTIME_LABELS.get(code, "Unknown")

    @property
    def is_passing(self) -> bool:
        """Determine whether the student passed (G3 ≥ 10).

        Returns
        -------
        bool
            ``True`` if G3 ≥ 10, ``False`` otherwise.

        BL2 — Explain
        ^^^^^^^^^^^^^^
        In the Portuguese education system the minimum passing mark is 10
        out of 20.  This property encapsulates that rule so that every
        part of the codebase uses a single, consistent definition of
        "passing".
        """
        try:
            return int(self.data.get("G3", 0)) >= 10
        except (ValueError, TypeError):
            return False

    @property
    def improvement(self) -> int:
        """Calculate the grade improvement from the first to the final period.

        Returns
        -------
        int
            ``G3 − G1``.  Positive values indicate improvement; negative
            values indicate decline; zero indicates no change.

        BL2 — Explain
        ^^^^^^^^^^^^^^
        Tracking improvement across the three grading periods (G1 → G3)
        is a key analytical question: did interventions (tutoring, extra
        study) help?  This simple difference is the most straightforward
        measure of change.  More sophisticated metrics (e.g. percentage
        change, regression-adjusted gain) could be added as additional
        properties later.
        """
        try:
            g3 = int(self.data.get("G3", 0))
            g1 = int(self.data.get("G1", 0))
        except (ValueError, TypeError):
            return 0
        return g3 - g1


# ===========================================================================
#  StudentCohort container class (CO3 — sequence protocol)
# ===========================================================================

class StudentCohort:
    """Represents a collection/cohort of StudentRecord objects.

    Course Outcomes Addressed:
        CO3: Demonstrates Python's sequence/collection protocol via special
             methods (__init__, __len__, __getitem__, __iter__, __repr__).

    Bloom's Taxonomy Levels:
        BL2 (Explain): Explains how aggregate collection types allow slicing,
             iteration, and cohort-level domain filtering.
        BL5 (Evaluate): Evaluates container classes vs bare lists of dicts.
             A cohort object provides type-safe filtering (e.g. by subject,
             passing status, or letter grade) without requiring repetitive
             manual loops in downstream consumer code.
    """

    def __init__(
        self,
        records: list[StudentRecord] | None = None,
        name: str = "All Students",
    ) -> None:
        """Initialise the cohort with a list of StudentRecord instances."""
        self.records: list[StudentRecord] = list(records) if records else []
        self.name: str = name

    def __len__(self) -> int:
        """Return the number of student records in this cohort.

        BL2 — Explain
        ^^^^^^^^^^^^^^
        Enables len(cohort), standard in Python's sequence protocol.
        """
        return len(self.records)

    def __getitem__(self, index):
        """Enable indexing and slicing on the cohort.

        Parameters
        ----------
        index : int or slice
            Integer index or slice object.

        Returns
        -------
        StudentRecord or StudentCohort
            Single record if integer index; new StudentCohort if sliced.

        BL2 — Explain
        ^^^^^^^^^^^^^^
        Enables cohort[0] or cohort[0:10] syntax.
        """
        if isinstance(index, slice):
            return StudentCohort(self.records[index], name=f"{self.name} (slice)")
        return self.records[index]

    def __iter__(self):
        """Iterate directly over StudentRecord instances in this cohort.

        BL2 — Explain
        ^^^^^^^^^^^^^^
        Enables for student in cohort: loops.
        """
        return iter(self.records)

    def __repr__(self) -> str:
        """Human-readable representation of the cohort."""
        return f"StudentCohort(name='{self.name}', size={len(self.records)})"

    def filter_by_subject(self, subject: str) -> StudentCohort:
        """Filter cohort by subject name (e.g. 'Mathematics')."""
        matches = [
            r for r in self.records
            if str(r.data.get("subject", "")).lower() == subject.lower()
        ]
        return StudentCohort(matches, name=f"{subject} Cohort")

    def filter_by_grade(self, letter: str) -> StudentCohort:
        """Filter cohort by letter grade ('A', 'B', 'C', 'D', 'F')."""
        matches = [r for r in self.records if r.grade_letter == letter.upper()]
        return StudentCohort(matches, name=f"Grade {letter.upper()} Cohort")

    @property
    def passing_students(self) -> StudentCohort:
        """Return sub-cohort of students who passed (G3 >= 10)."""
        matches = [r for r in self.records if r.is_passing]
        return StudentCohort(matches, name=f"{self.name} - Passing")

    @property
    def pass_rate(self) -> float:
        """Calculate percentage of students in this cohort who passed."""
        if not self.records:
            return 0.0
        passed = sum(1 for r in self.records if r.is_passing)
        return round(100.0 * passed / len(self.records), 2)

    def to_list_of_dicts(self) -> list[dict]:
        """Convert all records back to a list of dictionaries."""
        return [r.data for r in self.records]

