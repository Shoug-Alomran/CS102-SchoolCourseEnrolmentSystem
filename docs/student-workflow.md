# Student Workflow

The student workflow defines all actions available to a student after successfully logging into the School Enrollment System.  
This workflow is menu‑driven and allows students to manage their courses, view grades, and update personal information.

---

## Overview

After authentication, the system displays the student menu.  
Students may perform any of the following operations:

1. View available courses  
2. Enroll in a course  
3. View enrolled courses  
4. View credit limit  
5. Drop a course  
6. View grades  
7. Update personal profile  
8. Logout  

Each option is handled through the `Helpers` class and the `Student` class.

---

## 1. View available courses

This option displays all courses that the student is eligible to enroll in.

A course is considered available if:

- It is open for enrollment  
- It is not full  
- The student is not already enrolled  

Displayed information typically includes:

- Course name  
- Course code  
- Schedule  
- Credit hours  
- Capacity status  

This helps students explore their enrollment options.

---

## 2. Enroll in a course

The student may enroll in a course if:

- The course is open  
- The course is not full  
- The student has enough remaining credit hours  
- The student is not already enrolled  

The workflow:

1. The system lists all available courses  
2. The student selects a course  
3. The system validates the selection  
4. The course is added to the student's `enrolledCourses`  
5. The student is added to the course's `enrolledStudents`  

If enrollment fails, the system prints an appropriate message.

---

## 3. View enrolled courses

This option displays all courses the student is currently enrolled in.

Information shown includes:

- Course name  
- Course code  
- Credit hours  
- Schedule  

This helps students track their academic load.

---

## 4. View credit limit

The system displays:

- The student's total credit limit  
- The number of credit hours currently enrolled  
- The remaining available credit hours  

This prevents students from exceeding their credit capacity.

---

## 5. Drop a course

Students may drop a course only if:

- They are enrolled in the course  
- The course is still open for enrollment  

The workflow:

1. The system lists the student's enrolled courses  
2. The student selects a course to drop  
3. The system validates the selection  
4. The course is removed from the student's list  
5. The student is removed from the course's list  

If the course is closed, dropping is not allowed.

---

## 6. View grades

This option provides access to all grade‑related features.

Students may:

- View all grades for a course  
- View specific exam scores  
- View average grades for a course  

The workflow uses the `Assessment` class to retrieve and display grade information.

---

## 7. Update personal profile

Students may update:

- Password  
- Email  
- Phone number  
- Address  

Validation is handled through the `Helpers` class.  
After updating, the system saves the student's data immediately.

---

## 8. Logout

The student session ends, and the system returns to the main role selection menu.

---

## Summary

The student workflow provides all essential academic operations for students in the School Enrollment System.  
It allows students to manage their courses, monitor their academic progress, and maintain accurate personal information.

This workflow ensures a complete and functional student experience.
