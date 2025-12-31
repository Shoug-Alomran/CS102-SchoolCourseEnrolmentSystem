# System Menus

The School Enrollment System uses a menu‑driven console interface to guide users through available actions.  
Each user role—Student, Instructor, and Administrator—has its own dedicated menu, displayed after successful login.

These menus are defined and printed through the `Helpers` class.

---

## Purpose

The menu system is designed to:

- Provide a clear, structured navigation flow  
- Prevent users from accessing actions outside their role  
- Ensure consistency across all workflows  
- Simplify user interaction in a console‑based environment  

Each menu option corresponds to a specific workflow or helper method.

---

## Student Menu

Displayed after a student logs in.

Options include:

1. View available courses  
2. Enroll in a course  
3. View enrolled courses  
4. View credit limit  
5. Drop a course  
6. View grades  
7. Update personal information  
8. Logout  

This menu provides all academic and profile‑related actions available to students.

---

## Instructor Menu

Displayed after an instructor logs in.

Options include:

1. View enrolled students  
2. Grade students  
3. Update course information  
4. Update personal information  
5. Logout  

This menu focuses on teaching responsibilities and profile management.

---

## Administrator Menu

Displayed after an administrator logs in.

Options include:

1. Add student  
2. Remove student  
3. View student list  
4. Add instructor  
5. Remove instructor  
6. View instructor list  
7. Add course  
8. Close course  
9. Update student information  
10. Update instructor information  
11. Assign instructor to course  
12. View enrollment statistics  
13. Generate reports  
14. Logout  

This menu provides full system control and management capabilities.

---

## Input Handling

All menus rely on:

- `Helpers.getSafeIntInput()` for safe numeric input  
- Validation loops to prevent invalid selections  
- Clear error messages for out‑of‑range choices  

This ensures the system never crashes due to invalid menu input.

---

## Summary

The menu system is the backbone of user interaction in the School Enrollment System.  
By providing structured, role‑specific options, it ensures that users can easily navigate the system and access all available features.

These menus tie together the workflows, helpers, and entity classes into a cohesive user experience.
