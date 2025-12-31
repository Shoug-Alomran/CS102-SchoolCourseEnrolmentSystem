# Exceptions and Validation

The School Enrollment System relies heavily on input validation and defensive programming to ensure data integrity and prevent runtime crashes.  
Validation is centralized primarily in the `Helpers` class, while entity classes enforce basic structural rules through setters.

---

## Purpose

The validation and exception‑handling system is designed to:

- Prevent invalid data from entering the system  
- Protect the application from crashes caused by user input  
- Ensure consistent formatting of user information  
- Provide clear feedback when errors occur  
- Maintain clean separation between validation logic and business logic  

This approach keeps the system stable and predictable.

---

## Centralized Validation in Helpers

Most validation is performed through dedicated methods in the `Helpers` class.

### Key validation methods

- `ValidatePassword`  
- `ValidateEmail`  
- `ValidatePhoneNumber`  
- `ValidateAddress`  
- `ValidateName`  

Each method checks for:

- Non‑empty input  
- Minimum length requirements  
- Basic formatting rules  
- Logical correctness (e.g., phone number must be 10 digits)  

These methods return `true` or `false`, allowing workflows to loop until valid input is provided.

---

## Safe Integer Input

### Method: getSafeIntInput

This method prevents crashes caused by invalid numeric input.

Behavior:

1. Prompts the user for an integer  
2. Catches invalid input using exception handling  
3. Clears the scanner buffer  
4. Repeats until a valid integer is entered  

This ensures that menus and numeric fields never break the program.

---

## Role Validation

### Method: checkValidityOfRole

Ensures that the user selects a valid role:

- Student  
- Instructor  
- Admin  

Invalid selections trigger a retry loop.

---

## Field Updating with Predicates

### Method: updateFieldWithPrompt

This method uses a `Predicate<String>` to validate new field values.

Advantages:

- Reusable for any field  
- Clean separation between validation and updating  
- Eliminates repetitive code  

Example fields validated through this method:

- Email  
- Password  
- Phone number  
- Address  

---

## User Creation Validation

### Method: createUserWithPrompt

Used when creating new students or instructors.

Behavior:

- Prompts for a required field  
- Validates using a predicate  
- Repeats until valid input is provided  

This ensures that all new users are created with valid data.

---

## Entity‑Level Validation

Some validation is also performed inside entity classes such as `Course`.

Examples:

- Course name and code must not be empty  
- Capacity must be positive  
- Credit hours must be greater than zero  

Invalid values trigger error messages and do not update the field.

This prevents corrupted course data.

---

## Exception Handling Philosophy

The system uses exceptions primarily for:

- Input mismatch errors  
- File handling errors  
- Unexpected runtime issues  

Design principles:

- Never allow the program to crash due to user input  
- Always provide clear, user‑friendly error messages  
- Keep exception handling localized to the point of failure  
- Avoid exposing stack traces to the user  

This ensures a smooth and predictable user experience.

---

## Summary

The validation and exception‑handling system is a critical part of the School Enrollment System.  
By centralizing validation in the `Helpers` class, enforcing structural rules in entity classes, and using safe input techniques, the system maintains data integrity and prevents crashes.

This design ensures that all workflows operate reliably and consistently.
