---
title: "Full Java Source Code (per class)"
description: "Complete Java source code for every class in the CS102 School Course Enrolment System - main driver, users, courses, assessments, helpers and data manager."
---

# Full Source Code (per class)

The complete Java source for each class in the School Course Enrolment System, taken from the [CS102 project report](project-report.md). All classes are in the `schoolcourseenrolmentsystem` package.

| Class | Role in the system |
| --- | --- |
| [SchoolCourseEnrolmentSystem](source-code/main.md) | Driver class: loads data, creates the default admin, and runs the role selection loop and menus |
| [User&lt;T&gt;](source-code/user.md) | Abstract generic base class with shared profile fields and the abstract `login` / `logout` methods |
| [Student](source-code/student.md) | Enrollment, dropping courses, credit limits, grades and profile updates |
| [Instructor](source-code/instructor.md) | Viewing enrolled students, grading, and updating course information |
| [Administrator](source-code/administrator.md) | Managing students, instructors and courses, assigning instructors, closing courses |
| [Assessment](source-code/assessment.md) | `ExamType` enum, assigning grades, viewing grades, averages and exam scores |
| [Course](source-code/course.md) | Course details, capacity, enrollment status, credit hours and enrolled students |
| [Helpers](source-code/helpers.md) | Generic login, validation, safe input, menus, and role-specific operation helpers |
| [dataManager](source-code/data-manager.md) | Singleton for text-file persistence and CRUD operations |

!!! note
    The listings were extracted from the PDF report and re-indented, so line wrapping and spacing may differ a little from the original files.
