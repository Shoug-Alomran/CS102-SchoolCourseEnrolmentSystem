# Project File Structure

The School Enrollment System is organized into a clear, modular file structure that separates responsibilities across classes, workflows, and data management.  
This structure ensures maintainability, readability, and ease of navigation for developers and reviewers.

---

## Overview

The project is divided into the following major components:

- **Core entity classes**  
- **Workflow logic**  
- **Utility and helper classes**  
- **Data persistence layer**  
- **Main application entry point**  
- **Text‑based storage files**  

Each component plays a specific role in the system’s architecture.

---

## Directory Layout

A typical layout for the project is as follows:

SchoolCourseEnrolmentSystem/
│
├── src/
│   ├── User.java
│   ├── Student.java
│   ├── Instructor.java
│   ├── Administrator.java
│   ├── Course.java
│   ├── Assessment.java
│   │
│   ├── Helpers.java
│   ├── DataManager.java
│   │
│   └── SchoolCourseEnrolmentSystem.java    ← Main entry point
│
├── data/
│   ├── students.txt
│   ├── instructors.txt
│   ├── administrators.txt
│   ├── courses.txt
│   └── assessments.txt
│
└── docs/
├── index.md
├── structure.md
├── file-structure.md
├── data-files.md
├── helpers.md
├── data-manager.md
├── main.md
├── student.md
├── instructor.md
├── administrator.md
├── course.md
├── assessment.md
├── student-workflow.md
├── instructor-workflow.md
├── admin-workflow.md
├── exit-exception.md
├── code-main.md
├── code-helpers.md
├── code-data-manager.md
├── reports-and-statistics.md
└── CS102 PROJECT REPORT.pdf

---

## Folder Breakdown

### **src/** — Source Code

Contains all Java classes that implement the system’s logic.

- **Entity classes**  
  `User`, `Student`, `Instructor`, `Administrator`, `Course`, `Assessment`

- **Utility classes**  
  `Helpers`, `DataManager`

- **Main application**  
  `SchoolCourseEnrolmentSystem.java`

This folder represents the core of the application.

---

### **data/** — Text‑Based Storage

Contains all persistent storage files used by `DataManager`.

Files include:

- `students.txt`  
- `instructors.txt`  
- `administrators.txt`  
- `courses.txt`  
- `assessments.txt`  

Each file stores serialized objects, one per line, using a delimiter‑based format.

---

### **docs/** — Documentation (MkDocs)

Contains all Markdown files used to generate the project documentation website.

Includes:

- Project overview pages  
- Class documentation  
- Workflow descriptions  
- Code reference pages  
- Reports and statistics  
- PDF project report  

This folder powers the MkDocs site hosted on GitHub Pages.

---

## Purpose of the Structure

This file organization supports:

- **Separation of concerns**  
- **Easy navigation for developers and graders**  
- **Clear mapping between code, data, and documentation**  
- **Scalability** as the system grows  

Each folder has a single, well‑defined responsibility, making the project easier to understand and maintain.

---

## Summary

The project’s file structure is intentionally simple and modular:

- `src/` contains all Java logic  
- `data/` stores persistent text files  
- `docs/` powers the documentation site  

This structure ensures clarity, maintainability, and professional organization throughout the system.
