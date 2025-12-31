# Administrator Class

The `Administrator` class represents an administrative user within the School Enrollment System.  
It extends the generic `User<Administrator>` class and provides functionality for managing students, instructors, and courses.

---

## Purpose

The purpose of the `Administrator` class is to:

- Authenticate administrators through the inherited login system
- Add, remove, and update students and instructors
- Add and manage courses
- Assign instructors to courses
- Close courses when appropriate
- View system-wide statistics and reports
- Maintain overall system organization and data integrity

Administrators have the highest level of access and control in the system.

---

## Structure and key components

### 1. Inheritance

The class is defined as:

    public class Administrator extends User<Administrator>

This allows the administrator to inherit:

- ID, name, password, email, phone number, address
- Role handling
- Abstract login and logout methods

The administrator class then implements its own management-related functionality.

---

### 2. Constructors

#### Default constructor

Creates an empty administrator object, typically used during file loading or temporary object creation.

#### Parameterized constructor

Initializes:

- All inherited user fields (via `super`)
- Sets the role explicitly to `ADMIN`

This ensures that every administrator object is fully initialized with the correct role.

---

### 3. Methods

The `Administrator` class implements several categories of methods.

---

## Authentication

### login

Searches the list of administrators for a matching ID and password.

Behavior:

- Iterates through the administrator list
- Compares credentials
- Prints success or failure messages
- Returns the authenticated administrator or `null`

Note: A minor issue exists where the message "No admin record" may print inside the loop instead of after it.

### logout

Returns a simple confirmation message indicating that the administrator has logged out.

---

## User management

### removeStudent

Uses an iterator to safely remove a student by ID.

Behavior:

- Prompts for a student ID
- Searches the list
- Removes the student if found
- Prints success or failure messages

### removeInstructor

Similar to `removeStudent`, but for instructors.

### addInstructor and addStudent

Adds new instructors or students to their respective lists.

Behavior:

- Creates a new user object
- Sets all required fields
- Adds the user to the list
- Prints confirmation messages

### updateStudent and updateInstructor

Updates the profile of a student or instructor.

Behavior:

- Searches for the user by ID
- If found, updates:
  - Name
  - Email
  - Password
  - Phone number
  - Role
  - Address
- Prints success or failure messages

---

## Course management

### addCourse

Adds a new course to the system.

Behavior:

- Creates a new `Course` object
- Sets course name, code, schedule, description, capacity, credit hours
- Optionally assigns an instructor
- Prints confirmation messages

### assignInstructor

Assigns an instructor to a course.

Behavior:

- Ensures the course exists
- Ensures the course does not already have an instructor
- Assigns the instructor if valid

Prevents overwriting an existing instructor unless explicitly removed.

### closeCourse

Closes a course for enrollment.

A course may be closed if:

- It exists
- It is full
- It is already closed

The method prints appropriate feedback for each case.

---

## Viewing records

### viewStudentList and viewInstructorList

Displays all students or instructors.

Behavior:

- Iterates through the list
- Prints each user using their `toString()` method
- Handles empty or null lists gracefully

---

## Summary

The `Administrator` class provides the highest level of control in the School Enrollment System.  
By extending the `User` class and adding comprehensive management features, it enables administrators to maintain system integrity, manage users and courses, and oversee academic operations.

This class is essential for ensuring that the system remains organized, functional, and up to date.
