# Exit and Exception Flow

The School Enrollment System includes a clean exit flow and robust exception handling to ensure stability and data integrity.  
These mechanisms are implemented primarily in the `SchoolCourseEnrolmentSystem` main class and the `Helpers` utility class.

---

## Purpose

The exit and exception flow is designed to:

- Prevent crashes due to invalid input  
- Ensure all data is saved before termination  
- Provide clear feedback when errors occur  
- Maintain a smooth user experience  
- Support academic standards for safe and predictable system behavior  

These features protect both the user and the system.

---

## Exit Flow

### Trigger

The exit flow is triggered when:

- A user selects "Exit" from the main role selection menu  
- A critical error occurs that requires termination  

---

### Behavior

Upon exit:

1. The system calls `dataManager.saveAllData()`  
2. All lists (students, instructors, administrators, courses, assessments) are serialized and written to their respective files  
3. A final message is printed to confirm successful termination  
4. The program exits cleanly using `System.exit(0)`  

This ensures that no data is lost between sessions.

---

## Exception Handling

### Input validation

Handled through:

- `Helpers.getSafeIntInput()`  
- Validation loops for menu selections  
- Predicate-based field validation  

These prevent crashes from invalid user input.

---

### Try-catch blocks

Used in:

- Main method  
- File I/O operations  
- Numeric input parsing  
- Role selection and login  

Each block:

- Catches specific exceptions (e.g., `InputMismatchException`, `IOException`)  
- Prints a user-friendly error message  
- Clears the scanner buffer if needed  
- Allows the program to continue running  

---

### File errors

If a data file is missing:

- The system creates a new empty file  
- No crash occurs  
- A message may be printed for debugging  

This ensures that the system can recover from missing or corrupted files.

---

### Null checks

Used throughout the system to prevent:

- Null pointer exceptions  
- Invalid object access  
- Crashes during iteration  

Examples:

- Checking if a student or course exists before accessing fields  
- Verifying that lists are not null before looping  

---

## Defensive Programming

The system uses defensive programming techniques such as:

- Validating all user input  
- Avoiding assumptions about data state  
- Using helper methods to centralize validation  
- Catching and handling exceptions locally  

This keeps the system resilient and user-friendly.

---

## Summary

The exit and exception flow ensures that the School Enrollment System remains stable, predictable, and safe.  
By saving data on exit and handling errors gracefully, the system protects both users and academic integrity.

These features complete the foundation for a robust console-based application.
