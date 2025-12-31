# Student Class

The `Student` class represents a student user within the School Enrollment System.  
It extends the generic `User<Student>` class and adds academic‑specific attributes and behaviors such as course enrollment, grade viewing, and credit limit management.

---

## Purpose

The purpose of the `Student` class is to:

- Model a student in the system
- Manage course enrollment and dropping
- Track credit limits and enrolled hours
- Provide access to grades and assessments
- Allow students to update their personal information
- Support authentication through the inherited login system

The class simulates the core functionality of a student portal in a university environment.

---

## Structure and key components

### 1. Inheritance

The class is defined as:

    public class Student extends User<Student>

This allows the student to inherit:

- ID, name, password, email, phone number, address
- Role handling
- Abstract login and logout methods

The student class then implements its own role‑specific logic.

---

### 2. Attributes

The `Student` class introduces two additional fields:

- `creditLimit`  
  The maximum number of credit hours the student is allowed to enroll in.

- `enrolledCourses`  
  A list of `Course` objects representing the courses the student is currently enrolled in.

The list is initialized in the constructor to avoid `NullPointerException`.

---

### 3. Constructors

#### Default constructor

Creates an empty student object, typically used during file loading or temporary object creation.

#### Parameterized constructor

Initializes:

- All inherited user fields (via `super`)
- The student's credit limit
- The list of enrolled courses (or creates a new list if none is provided)

This ensures that every student object is fully initialized.

---

### 4. Methods

The `Student` class implements several categories of methods.

---

## Authentication

### login

Searches the list of students for a matching ID and password.

Behavior:

- Iterates through the student list
- Compares credentials
- Prints success or failure messages
- Returns the authenticated student or `null`

### logout

Returns a simple confirmation message indicating that the student has logged out.

---

## Enrollment management

### totalCreditLimit

Calculates the total number of credit hours the student is currently enrolled in.

### enroll_In_Course

Attempts to enroll the student in a course.

Enrollment is allowed only if:

- The student is not already enrolled
- The course is not full
- Enrollment is open
- The student has enough remaining credit hours

If successful:

- The course is added to the student's `enrolledCourses`
- The student is added to the course's `enrolledStudents`

### dropCourse

Allows the student to drop a course.

Dropping is only allowed if:

- The student is enrolled in the course
- The course is still open for enrollment

This prevents dropping after the course has been closed.

---

## Credit management

### viewCreditLimit

Displays:

- The student's total credit limit
- The number of credit hours currently enrolled
- The remaining available credit hours

### enrolledInHours

Calculates the total number of credit hours across all enrolled courses.

---

## Grades management

### viewGrades

Provides a menu‑driven interface for viewing grades.

Students can:

- View specific exam scores
- View all grades for a course
- View average grades for a course

This method uses a temporary `Assessment` object to access grade‑related functionality.

---

## Course exploration

### viewEnrolledCourses

Displays all courses the student is currently enrolled in, including:

- Course name
- Course code
- Credit hours
- Schedule

### viewAvailableCourses

Lists all courses that are:

- Open
- Not full
- Not already enrolled by the student

This helps students explore enrollment options.

---

## Personal information management

### updateStudentPersonalInfo

Allows the student to update:

- Password
- Email
- Phone number
- Address

Validation is handled through the `Helpers` class.

---

## Utility

### toString

Overrides `toString()` to return a concise representation of the student:

- ID
- Name

This is useful for administrative listings and debugging.

---

## Summary

The `Student` class models the academic and personal responsibilities of a student within the system.  
By extending the `User` class and adding enrollment, grade, and credit management features, it provides a complete and realistic representation of student functionality in a course enrollment environment.
