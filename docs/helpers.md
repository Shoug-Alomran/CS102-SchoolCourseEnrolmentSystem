# Helpers Class

The `Helpers` class provides a collection of reusable utility methods that support multiple parts of the School Enrollment System.  
It centralizes common logic such as input validation, login workflows, safe input handling, and menu display, reducing duplication across the project.

---

## Purpose

The primary goals of the `Helpers` class are:

- Ensure safe and consistent user input handling
- Validate user information (email, password, phone number, etc.)
- Provide a generic login system for all user types
- Display role-specific menus
- Support student, instructor, and administrator operations
- Generate system statistics and reports
- Reduce repeated code across the application

---

## Structure and key components

### 1. Global input scanner

A single shared `Scanner` instance is used throughout the system:

    public static final Scanner input = new Scanner(System.in);

Using one scanner for `System.in` helps avoid issues caused by multiple scanners reading from the same input stream.

---

### 2. Generic login system

The generic login method:

    public static <T extends User<T>> T login(List<T> usersList, T tempUser)

Key characteristics:

- Works with any user type (`Student`, `Instructor`, `Administrator`) via Java generics
- Authenticates by ID first, then delegates to `validatePasswordWithRetries`
- Supports up to three password attempts before failing
- Returns the authenticated user object or `null` if authentication fails

This design avoids writing separate login methods for every user subclass.

The helper method:

    public static <T extends User<T>> T validatePasswordWithRetries(List<T> usersList, T tempUser, String tempID)

- Prompts for the password
- Calls the subclass implementation of `login`
- Handles retry logic and failure messaging

---

### 3. Validation methods

The `Helpers` class provides several validation methods:

- `ValidatePassword`
- `ValidateEmail`
- `ValidatePhoneNumber`
- `ValidateAddress`
- `ValidateName`

General behavior:

- Check that values are non-null, non-empty, and meet simple format rules
- Use basic exception handling to avoid crashes
- Keep validation logic outside entity classes to maintain separation of concerns

Examples of enforced rules:

- Password length must be greater than 8 characters
- Email must contain `@` and `.`
- Phone number must be exactly 10 digits
- Name and address must exceed a minimum length

These methods are reused across creation and update flows for users.

---

### 4. Safe input collection

#### `getSafeIntInput(String prompt)`

This method safely collects integer input:

    public static int getSafeIntInput(String prompt)

Behavior:

- Continuously prompts the user until a valid integer is entered
- Catches invalid input and clears the scanner buffer
- Prevents `InputMismatchException` from crashing the program
- Centralizes integer parsing logic so that other methods can rely on it

This method is widely used in menus and workflows where numeric options are required.

---

### 5. Role management

#### `checkValidityOfRole()`

Prompts the user to select a valid role:

- Student
- Instructor
- Admin

It loops until a correct numeric option is provided and returns the corresponding `User.Role` value.

#### `updateRolePrompt(User.Role currentRole)`

Asks the user whether they want to change their role:

- If yes, it calls `checkValidityOfRole`
- If no, it leaves the role unchanged and returns the existing value

This is used primarily in administrator-driven profile update flows.

---

### 6. Field updating and creation

The class uses `Predicate<String>` to generalize validation logic for string fields.

#### `updateFieldWithPrompt`

    public static String updateFieldWithPrompt(String fieldName, String currentValue, Predicate<String> validator)

Behavior:

- Asks the user if they want to change a specific field (password, email, phone, etc.)
- If yes, prompts for a new value and validates it using the provided `Predicate<String>`
- Repeats until a valid value is entered
- Returns the updated or original value

This avoids the need for separate, hard-coded update methods such as:

- `updateEmail()`
- `updatePassword()`
- `updatePhoneNumber()`

#### `createUserWithPrompt`

    public static String createUserWithPrompt(String fieldName, Predicate<String> validator)

Behavior:

- Prompts the user to enter a required field (e.g., password, email, phone)
- Validates the input using the provided predicate
- Repeats until a valid value is supplied
- Returns the final validated value

Both methods take advantage of the `Predicate` interface to make validation logic reusable and configurable.

---

### 7. ID generation

#### `GenerateRandomID()`

    public static String GenerateRandomID()

Purpose:

- Generates a random 10-digit numeric ID for new students or instructors
- Reduces manual ID entry and potential duplication errors

Implementation details:

- Uses a `Random` instance and a `StringBuilder` to construct the ID
- Randomly selects characters from the string `"0123456789"`
- Ensures fixed length and numeric content

This method is used in administrator flows when creating new users.

---

### 8. User interface menus

The `Helpers` class defines text-based menus for each role.

#### `showStudentMenu()`

Prints the student menu options, such as:

- View available courses
- Enroll in a course
- View enrolled courses
- View credit limit
- Drop a course
- View grades
- Update personal information
- Logout

#### `showInstructorMenu()`

Displays instructor options, such as:

- View enrolled students
- Grade assignments
- Update course information
- Update personal information
- Logout

#### `showAdminMenu()`

Displays administrator options, such as:

- Add students
- Remove students
- View student list
- Add instructors
- Remove instructors
- View instructor list
- Add course
- Close course
- Update student information
- Update instructor information
- Assign instructor to course
- View enrollment statistics
- Generate reports
- Logout

These menu methods standardize the console interface for each user type.

---

### 9. Specific operational helpers

The `Helpers` class also contains methods that wrap multi-step operations. These methods combine input, validation, and calls to core classes.

#### Instructor-related helpers

- `updateCourseInfo(Instructor instructor, List<Course> listOfCourses)`  
  Prompts for a course code, new schedule, and new description, then calls the instructor’s `updateCourseInfo` method.

- `updateInstructorProfile(Instructor instructor)`  
  Uses `updateFieldWithPrompt` and validation methods to update password, email, phone number, and address, then applies the changes through `updateInstructorPersonalInfo`.

#### Student-related helpers

- `enroll_In_Course_Student(List<Course> listOfCourses, Student student)`  
  Filters available courses (open, not full, not already enrolled), displays them, and lets the student choose one to enroll in.

- `dropCourse(List<Course> listOfCourses, Student student)`  
  Prompts for a course code and attempts to drop the corresponding course using the student’s `dropCourse` method.

- `updateStudentProfile(Student specificStudent)`  
  Similar to instructor profile updates, but for students. Uses validators and update prompts to modify contact and login information.

#### Administrator-related helpers

- `addStudent(Administrator administrator, List<Student> listOfStudents)`  
  Guides the admin through creating a new student:
  - Validates name
  - Generates a unique random ID
  - Collects and validates password, email, phone number, address
  - Reads credit limit
  - Creates the `Student` object and adds it to the system

- `removeStudent(Administrator administrator, List<Student> listOfStudents)`  
  Prompts for a student ID and calls the admin’s `removeStudent` method.

- `removeInstructor(Administrator administrator, List<Instructor> listOfInstructors)`  
  Prompts for an instructor ID and calls the admin’s `removeInstructor` method.

- `addInstructor(Administrator administrator, List<Instructor> listOfInstructors)`  
  Similar to `addStudent`, but for instructors.

- `addCourse(Administrator administrator, List<Course> listOfCourses, List<Instructor> listOfInstructors)`  
  Guides the admin through creating a course:
  - Collects course name, code, capacity, credit hours
  - Optionally assigns an instructor by ID
  - Sets the course enrollment status (Open or Closed)
  - Adds the course to the system

- `adminUpdateStudentProfile(Administrator administrator, List<Student> listOfStudents)`  
  Allows an admin to locate a student and update their name, password, email, phone number, address, role, and optionally credit limit.

- `adminUpdateInstructorProfile(Administrator administrator, List<Instructor> listOfInstructors)`  
  Allows an admin to locate an instructor and update their details and role.

- `assignInstructor(Administrator administrator, List<Course> listOfCourses, List<Instructor> listOfInstructors)`  
  Lets an admin select a course and assign an instructor by ID.

- `closeCourse(Administrator administrator, List<Course> listOfCourses)`  
  Locates a course by name and code and calls `closeCourse` on the administrator.

These helpers simplify complex console workflows and ensure consistent validation and feedback.

---

### 10. Statistics and reports

The `Helpers` class also includes two high-level reporting utilities.

#### `viewEnrollmentStatistics(List<Course> listOfCourses)`

Behavior:

- Iterates over all courses
- Counts the number of enrolled students per course
- Sums total enrolled students across all courses
- Checks whether any courses are currently open
- Prints a simple summary report to the console

#### `generateReports(List<Course> listOfCourses)`

Behavior:

- Identifies the course with the highest number of enrolled students
- Prints the most popular course and its enrollment count
- Handles the case where there are no enrollments

These methods give administrators a quick overview of system usage and trends.

---

## Summary

The `Helpers` class is a central utility component used by all roles in the School Enrollment System.  
By consolidating input handling, validation, login workflows, menu printing, and multi-step operations, it keeps business logic inside the core classes while simplifying user interaction and orchestration.

This design improves clarity, reduces duplication, and makes the overall system easier to maintain and extend.
