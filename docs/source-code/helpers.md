---
title: "Helpers Class - Java Source Code"
description: "Full Java source of the Helpers utility class: generic login, input validation, safe input, menus, admin helpers and reports."
---

# Helpers Class - Source Code

Full Java source of the Helpers utility class: generic login, input validation, safe input, menus, admin helpers and reports.

For an explanation of how this class works, see the [Helpers code reference](../code-helpers.md). This listing comes from the [CS102 project report](../project-report.md).

```java title="Helpers.java" linenums="1"
package schoolcourseenrolmentsystem;

import java.util.*;
import java.util.function.Predicate;

public class Helpers {
    public static final Scanner input = new Scanner(System.in);

    /// <T extends User<T>> This method works with any User (Admin, Instructor,
    /// Student). T inherits from User<T>.
    /// The single T will return a single object of type T.
    public static <T extends User<T>> T login(List<T> usersList, T tempUser) {
        T loggedInUser = null;
        try {
            System.out.print("\nPlease enter your ID: ");
            String id = input.next();
            input.nextLine(); // Buffer

            // Check if the ID exists
            boolean idExists = false;
            for (T user : usersList) {
                if (user.getId().equals(id)) {
                    idExists = true;
                    break;
                }
            }
            if (!idExists) {
                System.out.println("No user found with the entered ID.");
            }
            loggedInUser = validatePasswordWithRetries(usersList, tempUser, id);
            return loggedInUser;
        } catch (Exception e) {

            return loggedInUser;
        }
    }

    public static <T extends User<T>> T validatePasswordWithRetries(List<T> usersList, T tempUser, String tempID) {
        T loggedInUser = null;
        int attempts = 0;
        final int maxAttempts = 3;

        while (attempts < maxAttempts) {
            System.out.print("\nPlease enter your password: ");
            String password = input.nextLine();

            loggedInUser = tempUser.login(usersList, tempID, password);

            if (loggedInUser != null) {
                return loggedInUser;
            } else {
                attempts++;
                if (attempts < maxAttempts) {
                    System.out.println("Incorrect password. Try again (" + (maxAttempts - attempts) + " attempts left).");
                }
            }
        }
        System.out.println("Too many failed attempts. Returning to main menu.");
        return null;
    }

    public static boolean ValidatePassword(String password) {
        boolean isValid = false;
        try {
            if (password != null && password != "" && password.length() > 8) {
                isValid = true;
            }
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }

        return isValid;
    }

    public static boolean ValidateEmail(String email) {
        boolean isValid = false;
        try {
            if (email != null && email != "" && email.contains("@") && email.contains(".")) {
                isValid = true;
            }
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
        return isValid;
    }

    public static boolean ValidatePhoneNumber(String phoneNumber) {
        boolean isValid = false;
        try {
            if (phoneNumber != null && phoneNumber != "" && phoneNumber.length() == 10) {
                isValid = true;
            }
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
        return isValid;
    }

    public static boolean ValidateAddress(String address) {
        boolean isValid = false;
        try {
            if (null != address && address != "" && address.length() > 3) {
                isValid = true;
            }
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
        return isValid;

    }

    public static Boolean ValidateName(String name) {
        boolean isValid = false;
        try {
            if (null != name && name != "" && name.length() > 3) {
                isValid = true;
            }
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
        return isValid;
    }
    public static User.Role checkValidityOfRole() {
        while (true) {
            System.out.println("Select a role: \n1. STUDENT \n2. INSTRUCTOR \n3. ADMIN \nOption:");
            try {
                int Option = Helpers.getSafeIntInput("\nOption: ");

                switch (Option) {
                    case 1:
                        return User.Role.STUDENT;
                    case 2:
                        return User.Role.INSTRUCTOR;
                    case 3:
                        return User.Role.ADMIN;
                    default:
                        System.out.println("Invalid selection. Please enter 1, 2, or 3.");
                }
            } catch (InputMismatchException e) {
                System.out.println("Invalid input. Please enter a number.");
                input.nextLine(); // clear the invalid input
            }
        }
    }

    /// Method created to avoid InputMismatchException

    public static int getSafeIntInput(String prompt) {
        try {
            int number = -1; // -1 is typically related to false or not true. This is a default number.
            boolean valid = false;
            while (!valid) {
                System.out.print(prompt);
                //number = Integer.parseInt(input.nextLine());
                number= input.nextInt();
                input.nextLine();
                valid = true;
            }
            return number;
        } catch (Exception e) {
            System.out.println("Invalid input. Please enter a number.");
            input.nextLine(); // Clear the invalid input
            return getSafeIntInput(prompt); // Retry
        }
    }

    public static User.Role updateRolePrompt(User.Role currentRole) {
        System.out.println("\nDo you want to change the role? \n1.Yes \n2.No");
        int choice = getSafeIntInput("\nOption: ");
        input.nextLine();

        if (choice == 1) {
            return checkValidityOfRole(); // Assuming you already have this
        } else {
            System.out.println("Role remains unchanged.");
            return currentRole;
        }
    }

    // Predicate <> helps us use premade validators.
    public static String updateFieldWithPrompt(String fieldName, String currentValue, Predicate<String> validator) {
        System.out.println("\nDo you want to change your " + fieldName + "? \n1.Yes \n2.No");
        int choice = Helpers.getSafeIntInput("\nOption: ");

        if (choice == 1) {
            System.out.print("\nEnter new " + fieldName + ": ");
            String newValue = input.nextLine();
            while (!validator.test(newValue)) {
                System.out.println("Invalid " + fieldName + ". Please try again.");
                System.out.print("\nEnter new " + fieldName + ": ");
                newValue = input.nextLine();
            }
            return newValue;
        } else {
            System.out.println(fieldName + " remains unchanged.");
            return currentValue;
        }
    }

    public static String createUserWithPrompt(String fieldName, Predicate<String> validator) {
        String inputValue;
        while (true) {
            System.out.print("\nEnter " + fieldName + ": ");
            inputValue = input.nextLine();
            if (!validator.test(inputValue)) { // .test() method is just how you invoke the logic inside the Predicate<>
                System.out.println("Invalid " + fieldName + ". Please try again.");
            } else {
                break;
            }
        }
        return inputValue;
    }
    public static String GenerateRandomID() {
        String numbers = "0123456789";
        int ID_Length = 10;
        Random random = new Random();

        StringBuilder id = new StringBuilder(ID_Length);

        for (int i = 0; i < ID_Length; i++) {

            int randomIndex = random.nextInt(numbers.length());
            char randomChar = numbers.charAt(randomIndex);
            id.append(randomChar);
        }
        return id.toString();
    }

    // MENUS
    public static void showStudentMenu() {
        System.out.println("");
        System.out.println("\n---------Student Menu---------");
        System.out.println("1. View avaliable courses.");
        System.out.println("2. Enroll in course.");
        System.out.println("3. View enrolled courses.");
        System.out.println("4. View credit limit.");
        System.out.println("5. Drop course.");
        System.out.println("6. View grades.");
        System.out.println("7. Update personal information.");
        System.out.println("8. Logout.");
    }

    public static void showInstructorMenu() {
        System.out.println("");
        System.out.println("\n---------Instructor Menu---------");
        System.out.println("1. View enrolled students.");
        System.out.println("2. Grade assignments.");
        System.out.println("3. Update course information.");
        System.out.println("4. Update personal information.");
        System.out.println("5. Logout.");
    }

    public static void showAdminMenu() {
        System.out.println("");
        System.out.println("\n---------Administrator Menu---------");
        System.out.println("1. Add Students.");
        System.out.println("2. Remove Students.");
        System.out.println("3. View student list.");

        System.out.println("4. Add Instructors.");
        System.out.println("5. Remove Instructors.");
        System.out.println("6. View instructor list.");
        System.out.println("7. Add Course.");
        System.out.println("8. Close Course.");
        System.out.println("9. Update Student Info.");
        System.out.println("10. Update Instructor Info.");
        System.out.println("11. Assign Instructor to Course.");
        System.out.println("12. View Enrollment Statistics.");
        System.out.println("13. Generate Reports.");
        System.out.println("14. Logout.");
    }

    // CASES

    // INSTRUCTOR CASES
    public static void updateCourseInfo(Instructor instructor, List<Course> listOfCourses) {
        try {
            System.out.println("\n---------Update Course Information---------\nEnter the course code of the course you
                    would like to update: ");
            String courseCode = input.next();
            input.nextLine(); // Buffer

            System.out.print("\nEnter new schedule:");
            String newSchedule = input.nextLine();

            System.out.print("\nEnter new description: ");
            String newDescription = input.nextLine();

            instructor.updateCourseInfo(courseCode, listOfCourses, newSchedule, newDescription);
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }

    public static void updateInstructorProfile(Instructor instructor) {
        try {

            System.out.println("\n---------Update Personal Profile---------");
            System.out.println("\nPlease fill out the form to update your profile.");

            String updatedPassword = Helpers.updateFieldWithPrompt("password", instructor.getPassword(),
                    Helpers::ValidatePassword); // Helpers::ValidatePassword is like an inhanced for-each loop
            String updateEmail = Helpers.updateFieldWithPrompt("email", instructor.getEmail(), Helpers::ValidateEmail);
            String updatePhone = Helpers.updateFieldWithPrompt("phone number", instructor.getPhoneNumber(),
                    Helpers::ValidatePhoneNumber);
            String updateAddress = Helpers.updateFieldWithPrompt("address", instructor.getAddress(),
                    Helpers::ValidateAddress);
            instructor.updateInstructorPersonalInfo(updatedPassword, updateEmail, updatePhone, updateAddress);
            System.out.println("Instructor " + instructor.getName() + "'s information updated.");
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }

    // STUDENT CASES
    public static void enroll_In_Course_Student(List<Course> listOfCourses, Student student) {
        try {
            System.out.println("\n---------Enroll In Course---------");

            // Filter available courses
            List<Course> availableCourses = new ArrayList<>();
            for (Course course : listOfCourses) {
                if (!course.isFull() &&
                        course.getEnrollmentStatus() == Course.EnrollmentStatusEnum.Open &&
                        !student.getEnrolledCoursesList().contains(course)) {
                    availableCourses.add(course);
                }
            }

            // Display results
            if (availableCourses.isEmpty()) {
                System.out.println("No available courses to enroll in.");
            } else {
                System.out.println("Courses available to enroll in:");

                for (int i = 0; i < availableCourses.size(); i++) {
                    Course course = availableCourses.get(i);
                    System.out.printf("%d. %s (%s)\n", (i + 1), course.getCourseName(), course.getCourseCode());
                }
                System.out.print("\nEnter the number of the course you would like to enroll in: ");
                int selectedCourse = input.nextInt();
                input.nextLine(); // Consume newline

                if (selectedCourse >= 1 && selectedCourse <= availableCourses.size()) {
                    Course chosenCourse = availableCourses.get(selectedCourse - 1);
                    student.enroll_In_Course(chosenCourse);
                } else {
                    System.out.println("Invalid selection: " + selectedCourse);
                }
            }
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }

    public static void dropCourse(List<Course> listOfCourses, Student student) {
        try {
            System.out.println("\n---------Unenroll In Course---------");
            System.out.print("\nEnter course code of the course you would like to drop: ");
            String dropCourseCode = input.next();
            input.nextLine(); // Buffer

            Course courseCodeToDrop = null;

            for (Course course : listOfCourses) {
                if (course.getCourseCode().equalsIgnoreCase(dropCourseCode)) {
                    courseCodeToDrop = course;
                    break;
                }
            }
            if (courseCodeToDrop != null) {
                student.dropCourse(courseCodeToDrop);

            } else {
                System.out.println("No course found with the code" + dropCourseCode + "'.");
            }
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }

    public static void updateStudentProfile(Student specificStudent) {
        try {
            System.out.println("\n---------Update Personal Profile---------");
            System.out.println("\nPlease enter the needed information to update your profile.");
            String updatedPassword = Helpers.updateFieldWithPrompt("password", specificStudent.getPassword(),
                    Helpers::ValidatePassword); // Helpers::ValidatePassword is like an inhanced for-each loop
            String updateEmail = Helpers.updateFieldWithPrompt("email", specificStudent.getEmail(),
                    Helpers::ValidateEmail);
            String updatePhone = Helpers.updateFieldWithPrompt("phone number", specificStudent.getPhoneNumber(),
                    Helpers::ValidatePhoneNumber);
            String updateAddress = Helpers.updateFieldWithPrompt("address", specificStudent.getAddress(),
                    Helpers::ValidateAddress);

            specificStudent.updateStudentPersonalInfo(updatedPassword, updateEmail, updatePhone, updateAddress);
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }

    // ADMIN CASES
    public static void addStudent(Administrator administrator, List<Student> listOfStudents) {
        try {
            System.out.println("\n---------Create New Student---------");
            String studentName = "";
            while (true) {
                System.out.print("\nEnter student name: ");
                studentName = input.nextLine();

                if (!Helpers.ValidateName(studentName)) {

                    System.out.println("Invalid name. Please enter a valid name.");
                    continue;
                }
                break;
            }
            String studentID;
            while (true) {
                studentID = GenerateRandomID();
                boolean exists = false;
                for (Student student : listOfStudents) {
                    if (student.getId().equals(studentID)) {
                        exists = true;
                        break;
                    }
                }
                if (!exists) {
                    break; // We found a unique ID, exit the loop
                }
            }
            String createPassword = Helpers.createUserWithPrompt("password", Helpers::ValidatePassword);
            String createEmail = Helpers.createUserWithPrompt("email", Helpers::ValidateEmail);
            String createPhoneNumber = Helpers.createUserWithPrompt("phone number",
                    Helpers::ValidatePhoneNumber);
            String createAddress = Helpers.createUserWithPrompt("address", Helpers::ValidateAddress);

            System.out.print("\nEnter credit limit: ");
            int creditLimit = input.nextInt();
            input.nextLine(); // Buffer

            Student newStudent = new Student(studentName, studentID, createPassword, createEmail,
                    createPhoneNumber, createAddress, creditLimit, new ArrayList<>());

            administrator.addStudent(newStudent, listOfStudents);

        } catch (Exception e) {
            System.out.println(e.getMessage());
        }

    }

    public static void removeStudent(Administrator administrator, List<Student> listOfStudents) {
        try {
            System.out.println("\n---------Remove Student---------");
            System.out.print("\nEnter the ID of the student to remove: ");
            String targetId = input.next();
            input.nextLine(); // Buffer
            administrator.removeStudent(listOfStudents, targetId);

        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
        System.out.println("Invalid option.");
    }

    public static void removeInstructor(Administrator administrator, List<Instructor> listOfInstructors) {
        try {
            System.out.println("\n---------Remove Instructor---------");
            System.out.print("\nEnter the ID of the instructor to remove: ");
            String targetId = input.next();
            input.nextLine(); // Buffer
            administrator.removeInstructor(listOfInstructors, targetId);
        } catch (Exception e) {
            System.out.println("Invalid option.");
        }
    }

    public static void addInstructor(Administrator administrator, List<Instructor> listOfInstructors) {
        try {
            System.out.println("\n---------Create New Instructor---------");
            String instructorName = "";
            while (true) {
                System.out.print("\nEnter instructor name: ");
                instructorName = input.nextLine();
                if (!Helpers.ValidateName(instructorName)) {
                    System.out.println("Invalid name. Please enter a valid name.");

                    continue;
                }
                break;
            }
            String instructorID;
            while (true) {
                instructorID = GenerateRandomID();
                boolean exists = false;
                for (Instructor instructor : listOfInstructors) {
                    if (instructor.getId().equals(instructorID)) {
                        exists = true;
                        break;
                    }
                }
                if (!exists) {
                    break;
                }
            }
            String createPassword = Helpers.createUserWithPrompt("password", Helpers::ValidatePassword);
            String createEmail = Helpers.createUserWithPrompt("email", Helpers::ValidateEmail);
            String createPhoneNumber = Helpers.createUserWithPrompt("phone number",
                    Helpers::ValidatePhoneNumber);
            String createAddress = Helpers.createUserWithPrompt("address", Helpers::ValidateAddress);

            Instructor newInstructor = new Instructor(instructorName, instructorID, createPassword, createEmail,
                    createPhoneNumber, createAddress, new ArrayList<>());

            administrator.addInstructor(newInstructor, listOfInstructors);
        } catch (Exception e) {
            System.out.println("Invalid option.");
        }
    }

    public static void addCourse(Administrator administrator, List<Course> listOfCourses,
            List<Instructor> listOfInstructors) {
        try {
            System.out.println("\n---------Create Course---------");

            System.out.print("\nEnter the course's information that you would like to create.\n\nEnter course name: ");
            String courseName = input.nextLine();

            System.out.print("\nEnter course code: ");
            String courseCode = input.nextLine();

            System.out.print("\nEnter course capacity: ");
            int courseCapacity = input.nextInt();
            input.nextLine(); // Buffer

            System.out.print("\nEnter course credit hours: ");
            int courseCreditHours = input.nextInt();
            input.nextLine(); // Buffer

            Course newCourse = new Course(courseName, courseCode, null, null, null, null, courseCapacity, null,
                    courseCreditHours);

            System.out.println("\nWould you like to assign instructor now? \n1. Assign now. \n2. Assign later.");
            int assignChoice = Helpers.getSafeIntInput("\nOption: ");

            if (assignChoice == 1) {
                System.out.print("\nAssign instructor by ID: ");
                String assignInstructorID = input.nextLine();

                // Validate instructor list is not empty.
                if (listOfInstructors.isEmpty()) {
                    System.out.println("\nNo instructors available. Please add an instructor before creating a course.");
                    return; // Stop the method early
                }
                Instructor selectedInstructor = null;
                for (Instructor instructor : listOfInstructors) {
                    if (instructor.getId().equals(assignInstructorID)) {
                        selectedInstructor = instructor;
                        break;
                    }
                }
                administrator.assignInstructor(newCourse, selectedInstructor);

                if (selectedInstructor == null) {
                    System.out.println("\nInstructor with ID " + assignInstructorID + " not found.");
                }
            }
            if (assignChoice == 2) {
                System.out.println("To be assigned.");
            }

            // Assign course status
            System.out.println("\nEnter course status: \n1. Open \n2.Closed");
            int courseStatus = Helpers.getSafeIntInput("Option: ");

            if (courseStatus == 1) {
                newCourse.setEnrollmentStatus(Course.EnrollmentStatusEnum.Open);
            } else if (courseStatus == 2) {
                newCourse.setEnrollmentStatus(Course.EnrollmentStatusEnum.Closed);
            }
            administrator.addCourse(listOfCourses, newCourse);
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }

    public static void adminUpdateStudentProfile(Administrator administrator, List<Student> listOfStudents) {
        try {
            System.out.print("\n---------Update Student Profile---------\nPlease enter the requiered information
                    below.\nStudent's name: ");
            String name = input.nextLine();

            System.out.print("\nStudent ID: ");
            String ID = input.next();
            input.nextLine(); // Buffer

            Student studentToUpdate = null;

            for (Student student : listOfStudents) {

                if (student.getName().equals(name) && student.getId().equals(ID)) {
                    studentToUpdate = student;
                    break;
                }
            }
            if (studentToUpdate != null) {
                System.out.println("Update " + studentToUpdate.getName() + " details below: ");

                String updateName = Helpers.updateFieldWithPrompt("name", studentToUpdate.getName(),
                        Helpers::ValidateName);
                String updatePassword = Helpers.updateFieldWithPrompt("password", studentToUpdate.getPassword(),
                        Helpers::ValidatePassword);
                String updateEmail = Helpers.updateFieldWithPrompt("email",
                        studentToUpdate.getEmail(),Helpers::ValidateEmail);
                String updatePhoneNumber = Helpers.updateFieldWithPrompt("phone number",
                        studentToUpdate.getPhoneNumber(), Helpers::ValidatePhoneNumber);
                String updateAddress = Helpers.updateFieldWithPrompt("address", studentToUpdate.getAddress(),
                        Helpers::ValidateAddress);
                User.Role updateRole = Helpers.updateRolePrompt(studentToUpdate.getRole());

                // Option to update credit limit
                System.out.printf("\nDo you want to update %s's credit limit?\n1. Yes\n2. No",
                        studentToUpdate.getName());
                int creditLimitChoice = input.nextInt();

                if (creditLimitChoice == 1) {
                    System.out.print("\nEnter new credit limit: ");
                    int updatedStudentcreditLimit = input.nextInt();
                    studentToUpdate.setCreditLimit(updatedStudentcreditLimit);
                } else if (creditLimitChoice == 2) {
                    System.out.println("Credit limit number remains unchanged.");
                }
                // Apply updates
                studentToUpdate.setName(updateName);
                studentToUpdate.setPassword(updatePassword);
                studentToUpdate.setEmail(updateEmail);
                studentToUpdate.setPhoneNumber(updatePhoneNumber);

                studentToUpdate.setAddress(updateAddress);
                studentToUpdate.setRole(updateRole);

                System.out.println("Student " + updateName + "'s profile updated successfully.");
            }
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }

    public static void adminUpdateInstructorProfile(Administrator administrator, List<Instructor> listOfInstructors) {
        try {
            System.out.println("\n---------Update Instuctor Profile---------\nPlease enter the requiered information below.");

            System.out.print("\nEnter instructor name: ");
            String instructorName = input.nextLine();

            System.out.print("\nEnter instructor ID: ");
            String instructorId = input.next();
            input.nextLine(); // Buffer

            Instructor instructorToUpdate = null;

            for (Instructor instructor : listOfInstructors) {
                if (instructor.getName().equals(instructorName) && instructor.getId().equals(instructorId)) {
                    instructorToUpdate = instructor;
                    break;
                }
            }
            if (instructorToUpdate != null) {
                System.out.println("Update " + instructorToUpdate.getName() + "'s details below: ");

                String updateName = Helpers.updateFieldWithPrompt("name", instructorToUpdate.getName(),
                        Helpers::ValidateName);
                String updatePassword = Helpers.updateFieldWithPrompt("password", instructorToUpdate.getPassword(),
                        Helpers::ValidatePassword);

                String updateEmail = Helpers.updateFieldWithPrompt("email",
                        instructorToUpdate.getEmail(),Helpers::ValidateEmail);
                String updatePhoneNumber = Helpers.updateFieldWithPrompt("phone
                        number",instructorToUpdate.getPhoneNumber(), Helpers::ValidatePhoneNumber);
                String updateAddress = Helpers.updateFieldWithPrompt("address", instructorToUpdate.getAddress(),
                        Helpers::ValidateAddress);
                User.Role updateRole = Helpers.updateRolePrompt(instructorToUpdate.getRole());
                // Apply updates
                instructorToUpdate.setName(updateName);
                instructorToUpdate.setPassword(updatePassword);
                instructorToUpdate.setEmail(updateEmail);
                instructorToUpdate.setPhoneNumber(updatePhoneNumber);
                instructorToUpdate.setAddress(updateAddress);
                instructorToUpdate.setRole(updateRole);

                System.out.println("Instructor " + updateName + "'s profile updated successfully.");
            }
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }

    public static void assignInstructor(Administrator administrator, List<Course> listOfCourses,
            List<Instructor> listOfInstructors) {
        try {
            System.out.println("\n---------Available Courses---------");

            for (int i = 0; i < listOfCourses.size(); i++) {
                /// The i+1 is for the indext of which the admin will select. The i is for
                /// 'this' spesific course.
                System.out.printf("%d. %s (%s).\n", (i + 1), listOfCourses.get(i).getCourseName(),
                        listOfCourses.get(i).getCourseCode());
            }
            System.out.print("\nEnter the number of the course to assign the instructor to: ");
            int courseIndex = input.nextInt() - 1;
            input.nextLine(); // Buffer

            // Basic validation.
            if (courseIndex < 0 || courseIndex >= listOfCourses.size()) {
                System.out.println("Invalid course selection.");
                return;
            }
            System.out.print("\nEnter the ID of the instructor to assign: ");
            String instructorID2 = input.next();
            input.nextLine(); // Buffer

            Instructor assignInstructor = null;

            for (Instructor instructor : listOfInstructors) {
                if (instructor.getId().equals(instructorID2)) {
                    assignInstructor = instructor;
                    break;
                }
            }
            if (assignInstructor != null) {
                Course selectedCourse = listOfCourses.get(courseIndex);
                administrator.assignInstructor(selectedCourse, assignInstructor);
            } else {
                System.out.println("Instructor with ID " + instructorID2 + " not found.");
            }
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }

    public static void closeCourse(Administrator administrator, List<Course> listOfCourses) {
        try {
            System.out.println("\n---------Close Courses---------\nEnter the details requiered below.\nEnter course name: ");
            String closeCourseName = input.nextLine();
            System.out.print("\nEnter course code: ");
            String closeCourseCode = input.next();
            input.nextLine(); // Buffer

            Course courseToClose = null;

            for (Course course : listOfCourses) {
                if (course.getCourseName().equals(closeCourseName) &&
                        course.getCourseCode().equals(closeCourseCode)) {
                    courseToClose = course;
                    break;
                }
            }
            if (courseToClose != null) {
                administrator.closeCourse(courseToClose, listOfCourses);
            } else {
                System.out.println("Course not found.");
            }
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }
    // Statistics.
    public static void viewEnrollmentStatistics(List<Course> listOfCourses) {
        int totalEnrolled = 0;
        boolean openCoursesExist = false;

        System.out.println("\n---------Enrollment Statistics---------");
        for (Course course : listOfCourses) {
            int count = course.getEnrolledStudents() != null ? course.getEnrolledStudents().size() : 0;
            totalEnrolled += count;
            System.out.printf("Course: %s (%s) - Enrolled: %d", course.getCourseName(), count);
            if (course.getEnrollmentStatus() == Course.EnrollmentStatusEnum.Open) {
                openCoursesExist = true;
            }
        }
        System.out.println("Total enrolled students across all courses: " + totalEnrolled);
        System.out.println("Open courses available: " + (openCoursesExist ? "Yes" : "No"));
    }

    public static void generateReports(List<Course> listOfCourses) {
        System.out.println("\n---------Enrollment Report---------");

        // Most popular course
        Course mostPopular = null;
        int maxEnrolled = 0;

        for (Course course : listOfCourses) {
            int enrolled = course.getEnrolledStudents() != null ? course.getEnrolledStudents().size() : 0;
            if (enrolled > maxEnrolled) {
                mostPopular = course;
                maxEnrolled = enrolled;
            }
        }
        if (mostPopular != null) {
            System.out.printf("\nMost popular course: %s (%s) - Enrolled: %d.", mostPopular.getCourseName(),
                    mostPopular.getCourseCode(), maxEnrolled);
        } else {
            System.out.println("No enrollments found.");
        }
    }
}
```
