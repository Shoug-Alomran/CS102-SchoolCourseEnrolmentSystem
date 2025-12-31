# Data Files

The School Enrollment System uses simple text‑based storage to persist data across sessions.  
Each entity type—students, instructors, administrators, courses, and assessments—is stored in its own `.txt` file.  
These files are managed entirely by the `dataManager` class.

---

## Purpose

The data files serve to:

- Store all system data between program runs  
- Provide a human‑readable format for debugging  
- Keep the system lightweight without requiring a database  
- Allow easy serialization and deserialization of objects  

This approach is ideal for academic projects and console‑based systems.

---

## File List

The system uses the following files:

- `students.txt`  
- `instructors.txt`  
- `administrators.txt`  
- `courses.txt`  
- `assessments.txt`  

Each file contains one serialized object per line.

---

## File Format

### General Format

Each line in a data file represents a single object.  
Fields are separated using a delimiter such as a comma or semicolon, depending on implementation.

Example structure:


The `dataManager` class:

- Splits each line using the delimiter  
- Converts the fields into the appropriate object  
- Adds the object to the corresponding list  

---

## Students File

Stores:

- Name  
- ID  
- Password  
- Email  
- Phone number  
- Address  
- Role  
- Credit limit  
- Enrolled course codes (optional)  

Each student is stored on a single line.

---

## Instructors File

Stores:

- Name  
- ID  
- Password  
- Email  
- Phone number  
- Address  
- Role  

Instructors do not store course assignments directly; courses reference instructors instead.

---

## Administrators File

Stores:

- Name  
- ID  
- Password  
- Email  
- Phone number  
- Address  
- Role  

Administrators typically have fewer fields than students.

---

## Courses File

Stores:

- Course name  
- Course code  
- Schedule  
- Description  
- Capacity  
- Credit hours  
- Enrollment status  
- Instructor ID (optional)  
- List of enrolled student IDs  

This file represents the academic structure of the system.

---

## Assessments File

Stores:

- Student ID  
- Course code  
- Assessment type  
- Score  
- Assessment name  

Each line represents one grade entry.

---

## Loading Data

When the system starts:

1. `dataManager` checks if each file exists  
2. If not, it creates an empty file  
3. If it exists, it reads each line  
4. It reconstructs objects and populates the system lists  

This ensures the system always starts with valid data.

---

## Saving Data

Before the system exits:

1. Each list is serialized  
2. Each object is written as a single line  
3. Files are overwritten with the latest data  

This guarantees that all changes made during the session are preserved.

---

## Advantages of Text‑Based Storage

- Easy to inspect manually  
- Easy to debug  
- No external dependencies  
- Simple to implement  
- Works well for small to medium datasets  

---

## Limitations

- Not suitable for large‑scale systems  
- No indexing or query optimization  
- No concurrency control  
- No relational integrity enforcement  

For academic or console‑based projects, however, this approach is ideal.

---

## Summary

The data files form the persistence layer of the School Enrollment System.  
By storing each entity type in a simple text file and managing them through the `dataManager` class, the system remains lightweight, transparent, and easy to maintain.

This storage method supports all workflows while keeping the project accessible and easy to understand.
