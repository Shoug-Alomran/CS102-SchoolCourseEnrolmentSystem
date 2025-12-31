# Instructor Workflow

The instructor workflow defines all actions available to an instructor after successfully logging into the School Enrollment System.  
This workflow allows instructors to manage their courses, grade students, and update their personal information.

---

## Overview

After authentication, the system displays the instructor menu.  
Instructors may perform the following operations:

1. View enrolled students  
2. Grade students  
3. Update course information  
4. Update personal profile  
5. Logout  

Each option is handled through the `Helpers` class and the `Instructor` class.

---

## 1. View enrolled students

This option allows instructors to see which students are enrolled in the courses they teach.

The workflow:

1. The system iterates through all courses  
2. It identifies courses assigned to the instructor  
3. For each course, it prints:
   - Course name  
   - Course code  
   - List of enrolled students  

If:

- The instructor has no assigned courses, a message is displayed  
- A course has no enrolled students, the system indicates that the list is empty  

This ensures instructors only see students in their own courses.

---

## 2. Grade students

This option allows instructors to assign or update grades for students.

The workflow:

1. The system lists all courses taught by the instructor  
2. The instructor selects a course  
3. The system lists all students enrolled in that course  
4. The instructor selects a student  
5. The instructor selects an assessment type (Quiz, Midterm, Final, etc.)  
6. The instructor enters a score between 0 and 100  
7. The system:
   - Updates an existing assessment if it exists  
   - Creates a new assessment if none exists  

Validation ensures:

- The instructor can only grade students in their own courses  
- Scores must be within valid range  
- Assessment types must be valid  

---

## 3. Update course information

Instructors may update:

- Course schedule  
- Course description  

The workflow:

1. The instructor enters a course code  
2. The system verifies:
   - The course exists  
   - The instructor is assigned to the course  
3. If valid, the instructor may update:
   - Schedule  
   - Description  

This prevents instructors from modifying courses they do not teach.

---

## 4. Update personal profile

Instructors may update:

- Password  
- Email  
- Phone number  
- Address  

Validation is handled through the `Helpers` class.  
After updating, the system saves the instructor’s data immediately.

---

## 5. Logout

The instructor session ends, and the system returns to the main role selection menu.

---

## Summary

The instructor workflow provides all essential academic management operations for instructors in the School Enrollment System.  
It allows instructors to manage their courses, grade students, and maintain accurate personal information.

This workflow ensures a complete and functional instructor experience.
