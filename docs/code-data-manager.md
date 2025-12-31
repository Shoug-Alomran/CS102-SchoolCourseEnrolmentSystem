# Data Manager (Code Reference)

The `dataManager` class is the persistence backbone of the School Enrollment System.  
It handles loading, saving, and managing all system data using a simple text‑file storage approach.

This page provides a clean, structured reference to the class and its responsibilities.

---

## Class Overview

The `dataManager` class is responsible for:

- Maintaining lists of all system entities  
- Loading data from text files at startup  
- Saving data before program exit  
- Providing CRUD operations for:
  - Students  
  - Instructors  
  - Administrators  
  - Courses  
  - Assessments  

It ensures that the system state persists across sessions.

---

## Singleton Pattern

The class uses the singleton design pattern.

### Key characteristics

- Only one instance exists  
- Accessed through `getInstance()`  
- Ensures consistent data across all workflows  
- Prevents accidental duplication of data lists  

This pattern is ideal for global system storage.

---

## Data Lists

The class maintains the following in‑memory lists:

- `List<Student> listOfStudents`  
- `List<Instructor> listOfInstructors`  
- `List<Administrator> listOfAdministrators`  
- `List<Course> listOfCourses`  
- `List<Assessment> listOfAssessments`  

These lists represent the entire system’s data model.

---

## File Paths

The class reads and writes to text files such as:

- `students.txt`  
- `instructors.txt`  
- `administrators.txt`  
- `courses.txt`  
- `assessments.txt`  

Each file stores serialized objects, one per line.

---

## Loading Data

### Method: loadAllData

Calls:

- `loadStudents()`  
- `loadInstructors()`  
- `loadAdministrators()`  
- `loadCourses()`  
- `loadAssessments()`  

Each loader:

1. Opens the file  
2. Reads each line  
3. Splits fields using a delimiter  
4. Constructs the appropriate object  
5. Adds it to the corresponding list  

If a file does not exist, it is created automatically.

---

## Saving Data

### Method: saveAllData

Calls:

- `saveStudents()`  
- `saveInstructors()`  
- `saveAdministrators()`  
- `saveCourses()`  
- `saveAssessments()`  

Each saver:

1. Opens the file for writing  
2. Serializes each object into a delimited line  
3. Writes all lines to the file  

This ensures all changes are preserved.

---

## CRUD Operations

The class provides full CRUD support.

### Students

- Add student  
- Remove student  
- Update student  
- Retrieve student by ID  

### Instructors

- Add instructor  
- Remove instructor  
- Update instructor  
- Retrieve instructor by ID  

### Administrators

- Add administrator  
- Retrieve administrator by ID  

### Courses

- Add course  
- Remove course  
- Update course  
- Assign instructor  
- Close course  
- Retrieve course by code  

### Assessments

- Add assessment  
- Update assessment  
- Retrieve assessments for a student and course  

These operations are used throughout the system by workflows and helper methods.

---

## Utility Methods

Additional helper methods include:

- Checking if a student or instructor exists  
- Ensuring unique IDs  
- Ensuring unique course codes  
- Validating instructor assignments  
- Checking if a course is full or open  

These methods maintain data integrity.

---

## Error Handling

The class uses exception handling to manage:

- Missing files  
- Invalid data lines  
- I/O errors  

If a file is missing:

- A new empty file is created  
- The system continues without crashing  

This ensures robustness.

---

## Summary

The `dataManager` class is the core persistence layer of the School Enrollment System.  
By managing all data lists, handling file I/O, and providing CRUD operations, it ensures that the system remains consistent, reliable, and easy to maintain.

This class supports every workflow and ties the entire system together.
