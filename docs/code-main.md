# Main Class (Code Reference)

This page provides a structured, readable reference for the `SchoolCourseEnrolmentSystem` main class.  
It focuses on the program flow, method responsibilities, and how the main class coordinates all system components.

---

## Class Overview

The `SchoolCourseEnrolmentSystem` class serves as the entry point of the entire application.

Responsibilities include:

- Initializing the system  
- Loading all saved data  
- Creating a default administrator  
- Handling the main role selection loop  
- Authenticating users  
- Directing users to their workflows  
- Saving all data before exit  

This class acts as the central controller of the system.

---

## Main Method Structure

The `main` method follows this sequence:

1. Retrieve the singleton `dataManager` instance  
2. Load all data using `loadAllData()`  
3. Create and register a default administrator  
4. Enter the main role selection loop  
5. Save all data before termination  

This ensures that the system always starts and ends in a consistent state.

---

## Default Administrator Creation

A default administrator is created at startup to guarantee:

- The system always has at least one admin  
- Administrative tasks are always accessible  
- No dependency on external files for initial admin creation  

The default admin is added even if data files already contain administrators.

---

## Role Selection Loop

The main loop repeatedly prompts the user to choose a role:

- Student  
- Instructor  
- Administrator  
- Exit  

For each role:

- The system calls the generic login method in `Helpers`  
- If authentication succeeds, the corresponding workflow is launched  
- If login fails, the user is returned to the main menu  

This loop continues until the user selects Exit.

---

## Workflow Dispatching

After login:

### Student
The system launches the student workflow, enabling:
- Course browsing  
- Enrollment  
- Dropping courses  
- Viewing grades  
- Updating profile  

### Instructor
The instructor workflow allows:
- Viewing enrolled students  
- Grading  
- Updating course info  
- Updating profile  

### Administrator
The admin workflow provides:
- User management  
- Course management  
- Instructor assignment  
- Reports and statistics  

Each workflow is implemented in the `Helpers` class and entity classes.

---

## Data Saving on Exit

When the user selects Exit:

- The system calls `saveAllData()`  
- All lists (students, instructors, administrators, courses, assessments) are serialized  
- Files are overwritten with the latest data  
- A final confirmation message is printed  
- The program terminates cleanly  

This ensures no data is lost.

---

## Exception Handling

The main class includes basic exception handling to:

- Prevent crashes from invalid input  
- Catch unexpected runtime errors  
- Keep the main loop running  
- Provide user‑friendly error messages  

Most validation is delegated to the `Helpers` class.

---

## Summary

The `SchoolCourseEnrolmentSystem` main class orchestrates the entire application.  
It initializes the system, manages authentication, dispatches workflows, and ensures data persistence.

This class ties together all components of the School Enrollment System and ensures smooth, predictable operation.
