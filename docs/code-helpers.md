# Helpers Class (Code Reference)

The `Helpers` class is the central utility component of the School Enrollment System.  
It provides shared logic for validation, login, menu handling, enrollment operations, reporting, and safe input handling.

This page documents the structure and responsibilities of the class in a clean, readable format.

---

## Class Overview

The `Helpers` class contains:

- Input validation methods  
- Login and authentication logic  
- Menu printing methods  
- Field‑updating utilities  
- Enrollment helpers  
- Reporting and statistics helpers  
- Safe integer input handling  

It acts as the backbone of all workflows.

---

## Login System

### Method: loginUser

A generic login method used by:

- Students  
- Instructors  
- Administrators  

Workflow:

1. Prompt for ID  
2. Prompt for password  
3. Search the appropriate list in `dataManager`  
4. Validate credentials  
5. Return the matching user object or null  

This method ensures consistent authentication across all roles.

---

## Menu Printing

The class includes methods to print:

- Student menu  
- Instructor menu  
- Administrator menu  

Each menu is displayed after successful login and drives the workflow logic.

---

## Safe Integer Input

### Method: getSafeIntInput

Prevents crashes caused by invalid numeric input.

Behavior:

- Wraps input in a try‑catch block  
- Catches `InputMismatchException`  
- Clears the scanner buffer  
- Repeats until a valid integer is entered  

This method is used throughout all workflows.

---

## Validation Methods

The class centralizes all validation logic.

### Password Validation

Checks:

- Minimum length  
- Non‑empty input  

### Email Validation

Checks:

- Contains `@`  
- Contains `.`  
- Reasonable length  

### Phone Number Validation

Checks:

- Exactly 10 digits  
- Numeric only  

### Address Validation

Checks:

- Non‑empty  
- Minimum length  

### Name Validation

Checks:

- Non‑empty  
- Alphabetic characters  

These methods return `true` or `false`, allowing workflows to loop until valid input is provided.

---

## Field Updating

### Method: updateFieldWithPrompt

A generic method that uses a `Predicate<String>` to validate new field values.

Workflow:

1. Prompt for new value  
2. Validate using predicate  
3. If valid, update the field  
4. If invalid, repeat  

This eliminates repetitive validation code.

---

## User Creation

### Method: createUserWithPrompt

Used when creating:

- Students  
- Instructors  

Behavior:

- Prompts for each required field  
- Validates using predicates  
- Returns the validated value  

This ensures all new users are created with valid data.

---

## Enrollment Helpers

The class includes methods to support student enrollment.

### Method: enrollStudentInCourse

Validates:

- Course is open  
- Course is not full  
- Student has enough credit hours  
- Student is not already enrolled  

If valid:

- Adds course to student  
- Adds student to course  

### Method: dropCourse

Validates:

- Student is enrolled  
- Course is open  

If valid:

- Removes course from student  
- Removes student from course  

These helpers ensure consistent enrollment logic.

---

## Grade Viewing Helpers

The class provides methods to support the `Assessment` class:

- View all grades for a course  
- View specific exam scores  
- View average grade  

These methods guide user interaction and input selection.

---

## Reporting Helpers

The class includes:

### viewEnrollmentStatistics

Displays:

- Total enrolled students  
- Whether open courses exist  
- Enrollment distribution  

### generateReports

Identifies:

- Most popular course  

These methods support administrative reporting.

---

## Summary

The `Helpers` class is the utility engine of the School Enrollment System.  
By centralizing validation, login, menu handling, enrollment logic, and reporting, it ensures consistency and reduces duplication across all workflows.

This class is essential for maintaining clean, organized, and reliable system behavior.
