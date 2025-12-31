# Project Structure

This page provides a high‑level overview of the architecture of the School Enrollment System.  
It summarizes the major components, their responsibilities, and how they interact within the application.

---

## Overall Project Structure

The system is organized into four main layers:

1. Core Entity Classes  
2. Utility Classes  
3. Data Management  
4. Main Application Flow

Each layer contributes to a modular, maintainable, and object‑oriented design.

---

## 1. Core Entity Classes

These classes represent the main actors and data structures in the system.

### User<T> (Abstract Base Class)

Defines shared attributes and behaviors for all user types.

Common fields include:

- name  
- ID  
- password  
- email  
- phoneNumber  
- role  
- address  

Subclasses:

- Student  
- Instructor  
- Administrator  

The class enforces a contract through abstract methods:

- `login()`  
- `logout()`

---

## Student

Represents a student in the system.

Responsibilities:

- Enroll in courses  
- Drop courses  
- View grades  
- Track credit limits  
- Update personal information  

---

## Instructor

Represents an instructor in the system.

Responsibilities:

- View enrolled students  
- Grade assessments  
- Update course information  
- Update personal profile  

---

## Administrator

Represents a system administrator.

Responsibilities:

- Add, remove, and update students and instructors  
- Add and manage courses  
- Assign instructors to courses  
- Close courses  
- View system statistics  

---

## Course

Represents a university course.

Key attributes:

- courseName  
- courseCode  
- schedule  
- description  
- creditHours  
- capacity  
- enrollmentStatus  
- instructor  
- enrolledStudents  
- assessments  

Includes validation logic and helper methods such as `isFull()`.

---

## Assessment

Represents a single evaluation event (quiz, midterm, final, project).

Attributes:

- studentId  
- courseCode  
- examType  
- score  
- assessmentName  

Methods support assigning grades, viewing grades, and calculating averages.

---

## 2. Utility Classes

### Helpers

Provides reusable logic used across the entire system.

Includes:

- Input validation  
- Safe integer input  
- Login workflows  
- Role selection  
- Profile updating  
- Course enrollment and dropping  
- Instructor and admin operations  
- Statistics and reporting  
- Menu display functions  

This class centralizes repeated logic and improves maintainability.

---

## 3. Data Management Class

### dataManager

Handles all file‑based persistence.

Responsibilities:

- Load and save data for:
  - Students  
  - Instructors  
  - Administrators  
  - Courses  
  - Assessments  

- CRUD operations for all entities  
- Assigning instructors  
- Enrolling and 3. Data Management Class

### dataManager

Handles all file‑based persistence.

Responsibilities:

- Load and save data for:
  - Students  
  - Instructors  
  - Administrators  
  - Courses  
  - Assessments  

- CRUD operations for all entities  
- Assigning instructors  
- Enrolling and dropping students  
- Generating reports dropping students  
- Generating reports  

This class ensures  

This class ensures that system data persists across that system data persists across program sessions program sessions.

---

## 4. Main Application Class

### SchoolCourse.

---

## 4. Main Application Class

### SchoolCourseEnrolmentSystem

The entry point of the application.

ResponsibilitiesEnrolmentSystem

The entry point of the application.

Responsibilities:

- Initialize the data manager  
:

- Initialize the data manager  
- Load all saved data  
- Create- Load all saved data  
- Create a default administrator  
- Provide the main role selection a default administrator  
- Provide the main role selection loop  
- Direct loop  
- Direct users to:
  - Student workflow  
  - Instructor workflow  
  - Administrator users to:
  - Student workflow  
  - Instructor workflow  
  - Administrator workflow  

- Save data before exiting workflow  

- Save data before exiting  

This class coordinates  

This class coordinates the entire system and manages user the entire system and manages user interaction.

---

 interaction.

---

## Summary

The project is structured to## Summary

The project is structured to separate concerns separate concerns clearly:

- Entity classes model the clearly:

- Entity classes model the system’s data  
- Helpers provide system’s data  
- Helpers provide reusable logic  
- dataManager handles persistence  
- reusable logic  
- dataManager handles persistence  
- The main class manages application flow The main class manages application flow  

This modular design supports  

This modular design supports readability, maintainability, and scalability readability, maintainability, and scalability.
