# School Enrollment System

CS102 Project — Documentation Website

---

## Abstract

The School Enrollment System is a Java-based console application designed to simulate a simplified university course management environment.

It enables three main roles:

- Students
- Instructors
- Administrators

Each role interacts with a shared set of courses and assessments through role-specific features such as enrollment, grading, user management, and reporting.

This documentation website presents the system design, class structure, workflows, and implementation details in a structured and accessible way.

Author: Shoug Alomran  
Email: 2234103192@psu.edu.sa  
Course: CS102 — Programming II  
Institution: Prince Sultan University  

---

## Project goals

- Simulate a basic university course enrollment system
- Implement role-based access and workflows
- Apply object-oriented design principles
- Use file-based persistence for storing system data
- Provide clear separation between entities, helpers, data management, and application flow

---

## System architecture overview

The system is organized into four main parts.

### Core entity classes

- `User<T>` (abstract, generic base class)
- `Student`
- `Instructor`
- `Administrator`
- `Course`
- `Assessment`

These classes model the main actors and data structures in the system, such as users, courses, and grades.

### Utility and support classes

- `Helpers`  
  Provides reusable logic for:
  - login and authentication workflows
  - input validation
  - safe integer input
  - role and profile updates
  - text-based menus and prompts

- `dataManager`  
  Handles:
  - loading and saving data from text files
  - CRUD operations on students, instructors, administrators, courses, and assessments
  - helper methods to enroll, drop, and assign users programmatically

### Main application class

- `SchoolCourseEnrolmentSystem`

Responsibilities:

- Initialize the data manager
- Load existing data from files
- Create and register a default administrator
- Provide the main role selection loop
- Direct users to the appropriate workflows:
  - Student workflow
  - Instructor workflow
  - Administrator workflow
- Save data before program exit

### Data files

Project data is persisted using simple text files:

- `students.txt`
- `instructors.txt`
- `administrators.txt`
- `courses.txt`
- `assessments.txt`

The `dataManager` class is responsible for translating between these files and in-memory objects.

---

## How to use this documentation

This site is organized into several sections:

- Project Structure  
  High-level breakdown of classes and responsibilities.

- Core Classes  
  Detailed documentation for each main class:
  User, Student, Instructor, Administrator, Course, Assessment.

- Workflows  
  Step-by-step explanation of:
  - Student operations
  - Instructor operations
  - Administrator operations
  - Exit and exception handling

- Code Reference  
  Selected source code listings with explanations for the main, helpers, and data manager classes.

- Reports and Statistics  
  Description of how enrollment statistics and reports are generated.

Use the navigation sidebar to move between these sections as needed.