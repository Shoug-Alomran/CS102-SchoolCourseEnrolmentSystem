# Course Class

The `Course` class represents a university course within the School Enrollment System.  
It stores all course-related information, manages enrollment, and maintains academic data such as assessments and assigned instructors.

---

## Purpose

The purpose of the `Course` class is to:

- Model a course with all essential academic attributes
- Track enrolled students
- Store assessments and grades
- Manage enrollment status (open or closed)
- Support instructor assignment
- Provide validation and helper methods for safe course management

This class forms the core of the system’s academic structure.

---

## Structure and key components

### 1. Enumerations

The class defines an enumeration for enrollment status:

- `OPEN`
- `CLOSED`

Using an enum ensures type safety and prevents invalid status values.

---

### 2. Attributes (private fields)

The `Course` class includes the following fields:

#### Basic information

- `courseName`  
- `courseCode`  
- `schedule`  
- `description`

#### Enrollment management

- `enrollmentStatus`  
- `capacity`  
- `enrolledStudents` (a list of `Student` objects)

#### Academic details

- `grades` (a list of `Assessment` objects)  
- `creditHours`  

#### Instructor

- `instructor` (an `Instructor` object)

The `enrolledStudents` list is initialized during construction to avoid null references.

---

### 3. Constructors

#### Full constructor

Initializes all fields, ensuring the course object is fully populated.

#### Default constructor

Creates an empty course object, typically used during file loading or temporary object creation.

---

### 4. Setters and getters

Each field has corresponding getter and setter methods.

Validation rules include:

- `courseName` and `courseCode` must not be empty  
- `capacity` must be a positive integer  
- `creditHours` must be greater than zero  
- Invalid values trigger error messages and do not update the field  

This defensive design prevents invalid course data from entering the system.

---

### 5. Methods

#### isFull

Determines whether the course has reached maximum capacity.

Behavior:

- Compares the size of `enrolledStudents` with `capacity`
- Returns `true` if the course is full, otherwise `false`

This method is used during enrollment to prevent over-enrollment.

---

## Summary

The `Course` class models all essential aspects of a university course, including academic details, enrollment status, instructor assignment, and grade tracking.  
Its validation logic and helper methods ensure that course data remains consistent and reliable throughout the system.

This class is central to the functionality of the School Enrollment System.
