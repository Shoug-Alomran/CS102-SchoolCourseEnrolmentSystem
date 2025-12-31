# Main Application Class

The `SchoolCourseEnrolmentSystem` class serves as the main entry point of the School Enrollment System.  
It coordinates authentication, role selection, workflow execution, and data persistence.

---

## Purpose

The purpose of the main application class is to:

- Initialize the system and load all saved data
- Create and register a default administrator
- Provide the main role selection loop
- Authenticate users based on their selected role
- Direct users to their respective workflows
- Save data before exiting the program

This class acts as the central controller of the entire application.

---

## Structure and key components

### 1. Default administrator instance

The system creates a default administrator at startup:

- Ensures that administrative tasks are always possible
- Prevents the system from starting without an admin
- Allows immediate access to user and course management features

This administrator is added to the system even if data is loaded from files.

---

### 2. Main method flow

The `main` method performs the following steps:

1. Initializes the singleton `dataManager` instance  
2. Loads all previously saved data using `loadAllData()`  
3. Adds the default administrator to the system  
4. Enters the main role selection loop  
5. Saves all data before exiting  

This ensures that the system state is preserved across sessions.

---

### 3. Role selection loop

The program repeatedly prompts the user to select a role:

- Student  
- Instructor  
- Administrator  
- Exit  

Based on the selected role, the system:

- Authenticates the user using the generic login system in `Helpers`
- Directs the user to the appropriate workflow
- Handles logout and returns to the main menu

This loop continues until the user chooses to exit.

---

## Student workflow

After successful login, students can:

1. View available courses  
2. Enroll in a course  
3. View enrolled courses  
4. View credit limit  
5. Drop a course  
6. View grades  
7. Update personal profile  
8. Logout  

Certain actions (such as updating personal information) trigger immediate data saving.

---

## Instructor workflow

After successful login, instructors can:

1. View enrolled students in their assigned courses  
2. Grade students  
3. Update course information  
4. Update personal profile  
5. Logout  

These actions allow instructors to manage academic responsibilities.

---

## Administrator workflow

After successful login, administrators can:

1. Add students  
2. Remove students  
3. View student list  
4. Add instructors  
5. Remove instructors  
6. View instructor list  
7. Add courses  
8. Close courses  
9. Update student information  
10. Update instructor information  
11. Assign instructors to courses  
12. View enrollment statistics  
13. Generate reports  
14. Logout  

Administrators have full control over system data and structure.

---

## Exit flow

When the user selects "exit":

- The system saves all data using `dataManager`
- A final message is displayed
- The program terminates cleanly

This ensures that no data is lost between sessions.

---

## Exception handling

The main class includes basic exception handling to:

- Prevent crashes from invalid input
- Ensure the main loop continues running
- Provide clear feedback to the user

Most validation and safety checks are delegated to the `Helpers` class.

---

## Summary

The `SchoolCourseEnrolmentSystem` class orchestrates the entire application.  
By managing initialization, authentication, workflows, and data persistence, it ensures that the system operates smoothly and consistently.

This class ties together all components of the School Enrollment System.
