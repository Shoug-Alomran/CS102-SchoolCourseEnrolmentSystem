# Reports and Statistics

The School Enrollment System includes built‑in reporting and statistical features that help administrators understand system activity, course popularity, and overall enrollment distribution.  
These features are implemented primarily through the `Helpers` class and rely on data stored in the `Course` and `Assessment` lists.

---

## Purpose

The reporting and statistics features are designed to:

- Provide administrators with insight into system usage
- Identify popular or under‑enrolled courses
- Summarize student enrollment across all courses
- Support academic planning and decision‑making
- Offer quick, console‑based summaries without external tools

These features help maintain visibility into the system’s academic structure.

---

## Enrollment Statistics

### Method: viewEnrollmentStatistics

This method summarizes enrollment across all courses.

It displays:

- Total number of enrolled students across the entire system  
- Whether any courses are currently open  
- A simple distribution of enrollment per course  

Workflow:

1. Iterate through all courses  
2. Count the number of enrolled students in each  
3. Add to a running total  
4. Check whether any course has `OPEN` status  
5. Print the results  

This provides administrators with a quick overview of system activity.

---

## Popular Course Report

### Method: generateReports

This method identifies the most popular course based on enrollment count.

Workflow:

1. Iterate through all courses  
2. Track the course with the highest number of enrolled students  
3. Print:
   - Course name  
   - Course code  
   - Number of enrolled students  

If no students are enrolled in any course, the system prints a message indicating that no popularity ranking can be generated.

This report helps administrators understand which courses attract the most students.

---

## Data Sources

The reporting features rely on:

- `listOfCourses` from `dataManager`  
- `enrolledStudents` list inside each `Course` object  
- Enrollment status (`OPEN` or `CLOSED`)  
- Assessment data (for grade‑related reporting, if needed)  

These data structures ensure that reports are always based on the most current system state.

---

## Limitations

The reporting system is intentionally simple:

- No graphical charts  
- No external file export  
- No historical tracking  
- No multi‑semester comparison  

It is designed for console‑based academic simulations rather than full institutional analytics.

---

## Summary

The reports and statistics features provide administrators with essential insights into course enrollment and system activity.  
By summarizing enrollment totals and identifying popular courses, the system supports informed decision‑making and academic planning.

These features complete the administrative toolkit of the School Enrollment System.
