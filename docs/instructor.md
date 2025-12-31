# Instructor Class

The `Instructor` class represents an instructor within the School Enrollment System.  
It extends the generic `User<Instructor>` class and provides functionality related to teaching, grading, and managing course information.

---

## Purpose

The purpose of the `Instructor` class is to:

- Authenticate instructors through the inherited login system
- Allow instructors to view students enrolled in their assigned courses
- Enable grading of assessments
- Support updating course information such as schedule and description
- Allow instructors to update their personal information
- Provide a clear representation of instructor data for administrative use

The class models the responsibilities of an instructor in an academic environment.

---

## Structure and key components

### 1. Inheritance

The class is defined as:

    public class Instructor extends User<Instructor>

This allows the instructor to inherit:

- ID, name, password, email, phone number, address
- Role handling
- Abstract login and logout methods

The instructor class then implements its own role‑specific functionality.

---

### 2. Constructors

#### Default constructor

Creates an empty instructor object, typically used during file loading or temporary object creation.

#### Parameterized constructor

Initializes:

- All inherited user fields (via `super`)
- Any instructor‑specific fields (if provided)

Note: Although the constructor may accept a list of enrolled students, this parameter is not used internally, which may be intentional or an oversight.

---

### 3. Methods

The `Instructor` class implements several categories of methods.

---

## Authentication

### login

Searches the list of instructors for a matching ID and password.

Behavior:

- Iterates through the instructor list
- Compares credentials
- Prints success or failure messages
- Returns the authenticated instructor or `null`

### logout

Returns a simple confirmation message indicating that the instructor has logged out.

---

## Viewing enrolled students

### viewEnrolledStudents

Allows the instructor to view students enrolled in the courses they teach.

Behavior:

- Iterates through all courses
- Filters courses assigned to the instructor
- Displays enrolled students for each course
- Handles cases where:
  - No courses are assigned
  - Courses have no enrolled students

This method ensures instructors only see students in their own courses.

---

## Grading students

### gradeStudent

Provides a multi‑step process for assigning or updating a student's grade.

Workflow:

1. Instructor selects a course they teach  
2. Instructor selects a student enrolled in that course  
3. Instructor selects an assessment type (Quiz, Midterm, Final, etc.)  
4. Instructor enters a score between 0 and 100  
5. The system:
   - Updates an existing assessment if it exists  
   - Creates a new assessment if none exists  

The method includes validation and error handling for invalid inputs.

---

## Updating course information

### updateCourseInfo

Allows instructors to update the schedule and description of a course.

Behavior:

- Instructor enters a course code
- System verifies:
  - The course exists
  - The instructor is assigned to the course
- If valid, the instructor may update:
  - Schedule
  - Description

The method prevents instructors from modifying courses they do not teach.

---

## Updating personal information

### updateInstructorPersonalInfo

Allows instructors to update their own:

- Password
- Email
- Phone number
- Address

Validation is handled through the `Helpers` class.

---

## Utility

### toString

Overrides `toString()` to return a concise representation of the instructor:

- ID
- Name

This is useful for administrative listings and debugging.

---

## Summary

The `Instructor` class models the teaching and grading responsibilities of instructors within the system.  
By extending the `User` class and adding course‑specific and grading functionality, it provides a complete representation of instructor behavior in a course enrollment environment.
