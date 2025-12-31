# Data Manager Class

The `dataManager` class is responsible for loading, saving, and managing all persistent data in the School Enrollment System.  
It acts as the system’s storage layer, handling CRUD operations for students, instructors, administrators, courses, and assessments.

---

## Purpose

The purpose of the `dataManager` class is to:

- Load all system data from text files at startup
- Save all system data before the program exits
- Provide CRUD operations for all user types and courses
- Maintain lists of:
  - Students
  - Instructors
  - Administrators
  - Courses
  - Assessments
- Serve as the central data repository for the entire application

This class ensures that the system state persists across sessions.

---

## Structure and key components

### 1. Singleton pattern

The class uses a singleton design:

- Only one instance of `dataManager` exists
- Accessed through a static `getInstance()` method
- Ensures consistent data across all workflows

This prevents data duplication and synchronization issues.

---

### 2. Data lists

The class maintains the following lists:

- `List<Student> listOfStudents`
- `List<Instructor> listOfInstructors`
- `List<Administrator> listOfAdministrators`
- `List<Course> listOfCourses`
- `List<Assessment> listOfAssessments`

These lists represent the entire system’s data in memory.

---

### 3. File paths

The class reads and writes to text files such as:

- `students.txt`
- `instructors.txt`
- `administrators.txt`
- `courses.txt`
- `assessments.txt`

Each file stores serialized data for its corresponding entity type.

---

## Loading data

### loadAllData

This method loads all system data at startup by calling:

- `loadStudents()`
- `loadInstructors()`
- `loadAdministrators()`
- `loadCourses()`
- `loadAssessments()`

Each loader:

- Opens the corresponding file
- Reads each line
- Splits fields by delimiter
- Creates the appropriate object
- Adds it to the corresponding list

If a file does not exist, the system creates it automatically.

---

## Saving data

### saveAllData

This method saves all system data before program exit by calling:

- `saveStudents()`
- `saveInstructors()`
- `saveAdministrators()`
- `saveCourses()`
- `saveAssessments()`

Each saver:

- Opens the file for writing
- Serializes each object into a line of text
- Writes all lines to the file

This ensures that all changes made during the session are preserved.

---

## CRUD operations

The class provides CRUD operations for all entity types.

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

These operations are used throughout the system by the `Helpers` class and the main workflows.

---

## Utility methods

The class includes additional helper methods such as:

- Checking if a student or instructor exists  
- Checking if a course exists  
- Ensuring unique IDs  
- Ensuring unique course codes  
- Validating instructor assignments  

These methods help maintain data integrity.

---

## Summary

The `dataManager` class is the backbone of the School Enrollment System’s data layer.  
By handling all loading, saving, and CRUD operations, it ensures that the system remains consistent, persistent, and reliable across sessions.

This class enables the rest of the application to focus on workflows and logic without worrying about data storage.
