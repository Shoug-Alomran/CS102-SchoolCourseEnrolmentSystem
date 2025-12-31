# Assessment Class

The `Assessment` class represents an individual evaluation event within a course, such as quizzes, midterms, finals, or projects.  
It links a student, a course, an assessment type, and a score into a single structured record.

---

## Purpose

The purpose of the `Assessment` class is to:

- Store grade information for a specific student in a specific course
- Represent different types of assessments using an enumeration
- Support assigning and updating grades
- Provide methods for viewing grades and calculating averages
- Serve as the academic record component of the system

This class is essential for tracking student performance.

---

## Structure and key components

### 1. Enumerations

The class defines an enumeration for assessment types, such as:

- Quiz
- Midterm
- Final
- Project

Using an enum ensures that only valid assessment types can be assigned.

---

### 2. Attributes (private fields)

The `Assessment` class includes the following fields:

- `studentId`  
- `courseCode`  
- `examType`  
- `score`  
- `assessmentName`

These fields uniquely identify the assessment and store the student’s performance.

---

### 3. Constructor

The class provides a single constructor that initializes all fields.

This ensures that every `Assessment` object is complete and valid at creation time.

---

### 4. Setters and getters

Standard getter and setter methods are provided for all fields.

No complex validation is performed inside the setters; values are assigned directly.

---

### 5. Methods

The `Assessment` class includes several methods for managing and viewing grades.

---

## assignGrade

This method assigns or updates a grade for a student.

Behavior:

- Searches the list of assessments for an existing record matching:
  - student ID
  - course code
  - exam type
- If found, updates the score
- If not found, creates a new assessment entry
- Prints feedback indicating whether the grade was updated or newly recorded

---

## viewAllGradesForCourse

Allows a student to view all their grades for a selected course.

Behavior:

- Displays a list of courses the student is enrolled in
- Prompts the student to select a course
- Prints all assessments and scores for that course
- Handles cases where no grades exist

---

## viewTotalAverageGrade

Calculates the average score for a student in a selected course.

Behavior:

- Filters assessments by student ID and course code
- Computes the average score
- Prints the result
- Handles cases where no assessments exist

---

## viewSpecificExamScore

Allows a student to view the score for a specific exam type.

Behavior:

- Prompts the student to select a course
- Prompts the student to select an exam type
- Searches for a matching assessment
- Prints the score if found
- Prints a message if no score exists

---

## Summary

The `Assessment` class provides the foundation for grade tracking within the School Enrollment System.  
By linking students, courses, assessment types, and scores, it enables accurate academic reporting and supports all grade‑related functionality in the system.

This class is essential for representing student performance and supporting instructor grading workflows.
