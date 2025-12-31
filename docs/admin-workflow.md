# Administrator Workflow

The administrator workflow defines all actions available to an administrator after successfully logging into the School Enrollment System.  
Administrators have the highest level of access and can manage users, courses, and system-wide academic data.

---

## Overview

After authentication, the system displays the administrator menu.  
Administrators may perform the following operations:

1. Add a student  
2. Remove a student  
3. View student list  
4. Add an instructor  
5. Remove an instructor  
6. View instructor list  
7. Add a course  
8. Close a course  
9. Update student information  
10. Update instructor information  
11. Assign instructor to a course  
12. View enrollment statistics  
13. Generate reports  
14. Logout  

Each option is handled through the `Helpers` class and the `Administrator` class.

---

## 1. Add a student

Administrators can create new student accounts.

Workflow:

1. Enter student name  
2. System generates a random 10‑digit ID  
3. Enter and validate:
   - Password  
   - Email  
   - Phone number  
   - Address  
4. Enter credit limit  
5. Student is added to the system  

Validation ensures all fields meet system requirements.

---

## 2. Remove a student

Administrators can remove a student by ID.

Workflow:

1. Enter student ID  
2. System searches the student list  
3. If found, the student is removed  
4. If not found, a message is displayed  

Removal uses an iterator to avoid errors during list modification.

---

## 3. View student list

Displays all students currently registered in the system.

Each student is printed using their `toString()` method.

---

## 4. Add an instructor

Similar to adding a student, but without credit limits.

Workflow:

1. Enter instructor name  
2. System generates a random ID  
3. Enter and validate:
   - Password  
   - Email  
   - Phone number  
   - Address  
4. Instructor is added to the system  

---

## 5. Remove an instructor

Administrators can remove an instructor by ID.

Workflow mirrors student removal.

---

## 6. View instructor list

Displays all instructors currently registered in the system.

---

## 7. Add a course

Administrators can create new courses.

Workflow:

1. Enter course name  
2. Enter course code  
3. Enter schedule  
4. Enter description  
5. Enter capacity  
6. Enter credit hours  
7. Optionally assign an instructor  
8. Set enrollment status (open or closed)  
9. Course is added to the system  

Validation ensures all fields are valid.

---

## 8. Close a course

Administrators can close a course for enrollment.

A course may be closed if:

- It exists  
- It is open  
- It is full or intentionally closed  

The system prints appropriate feedback.

---

## 9. Update student information

Administrators can update:

- Name  
- Password  
- Email  
- Phone number  
- Address  
- Role  
- Credit limit  

Workflow:

1. Enter student ID  
2. If found, update fields using validation  
3. Save changes  

---

## 10. Update instructor information

Similar to updating student information, but without credit limits.

---

## 11. Assign instructor to a course

Workflow:

1. Enter course code  
2. Enter instructor ID  
3. System verifies:
   - Course exists  
   - Instructor exists  
   - Course does not already have an instructor  
4. Instructor is assigned  

This ensures proper teaching assignments.

---

## 12. View enrollment statistics

Displays:

- Total number of enrolled students across all courses  
- Whether open courses exist  
- Basic enrollment distribution  

This provides administrators with a quick overview of system activity.

---

## 13. Generate reports

Identifies:

- The most popular course (highest enrollment)  

Useful for academic planning and analysis.

---

## 14. Logout

Ends the administrator session and returns to the main role selection menu.

---

## Summary

The administrator workflow provides full control over the School Enrollment System.  
Administrators manage users, courses, assignments, and system-wide academic data, ensuring that the system remains organized, functional, and up to date.

This workflow represents the highest level of access and responsibility within the system.
