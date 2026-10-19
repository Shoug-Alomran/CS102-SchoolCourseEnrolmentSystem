---
title: "Main Class (SchoolCourseEnrolmentSystem) - Java Source Code"
description: "Full Java source of the SchoolCourseEnrolmentSystem driver class: data loading, default administrator, role selection loop and role-specific menus."
---

# Main Class (SchoolCourseEnrolmentSystem) - Source Code

Full Java source of the SchoolCourseEnrolmentSystem driver class: data loading, default administrator, role selection loop and role-specific menus.

For an explanation of how this class works, see the [Main Class reference](../code-main.md). This listing comes from the [CS102 project report](../project-report.md).

```java title="SchoolCourseEnrolmentSystem.java" linenums="1"
package schoolcourseenrolmentsystem;

import java.util.*;

public class SchoolCourseEnrolmentSystem {
    private static Administrator DefaultAdmin = new Administrator("Shoug", "1122334455", "Default12345",
            "S.Alomran@gmail.com",
            "0531110904", "Qirawan district");

    public static void main(String[] args) {
        dataManager dataManagerInstance = dataManager.getInstance();
        Scanner input = Helpers.input;

        dataManagerInstance.loadAllData();

        try {
            boolean exit = false;
            dataManagerInstance.addAdministrator(DefaultAdmin);
            System.out.println("\nWelcome to School Course Enrolment System!");
            while (!exit) {
                System.out.println(
                        "Enter your role from the current options: (Student/Instructor/Admin) or exit to finish.");
                String role = input.next();
                input.nextLine();

                switch (role.toLowerCase()) {
                    case "student":
                        Student tempStudent = new Student();
                        Student loggedInStudent = Helpers.login(dataManagerInstance.getAllStudents(), tempStudent);

                        if (loggedInStudent == null) {
                            continue;
                        }
                        boolean studentExit = false;

                        while (!studentExit) {
                            Helpers.showStudentMenu();
                            int studentChoice = Helpers.getSafeIntInput("Option: ");

                            switch (studentChoice) {
                                case 1:
                                    loggedInStudent.viewAvailableCourses(dataManagerInstance.getAllCourses());
                                    break;
                                case 2:
                                    Helpers.enroll_In_Course_Student(dataManagerInstance.getAllCourses(),
                                            loggedInStudent);
                                    break;
                                case 3:
                                    loggedInStudent.viewEnrolledCourses();
                                    break;
                                case 4:
                                    loggedInStudent.viewCreditLimit(dataManagerInstance.getAllStudents());
                                    break;
                                case 5:
                                    Helpers.dropCourse(dataManagerInstance.getAllCourses(), loggedInStudent);
                                    break;
                                case 6:
                                    loggedInStudent.viewGrades(dataManagerInstance.getAllAssessments());
                                    break;
                                case 7:
                                    Helpers.updateStudentProfile(loggedInStudent);
                                    dataManagerInstance.saveStudents(); // Save after profile update
                                    break;
                                case 8:
                                    loggedInStudent.logout(loggedInStudent);
                                    studentExit = true;
                                    break;
                                default:
                                    System.out.println("Invalid option.");
                            }
                        }
                        break;

                    case "instructor":
                        Instructor tempInstructor = new Instructor();
                        Instructor loggedInInstructor = Helpers.login(dataManagerInstance.getAllInstructors(),
                                tempInstructor);

                        if (loggedInInstructor == null) {
                            continue;
                        }
                        boolean exitInstructor = false;
                        while (!exitInstructor) {
                            Helpers.showInstructorMenu();
                            int instructorChoice = Helpers.getSafeIntInput("Option: ");

                            switch (instructorChoice) {
                                case 1:
                                    loggedInInstructor.viewEnrolledStudents(loggedInInstructor,
                                            dataManagerInstance.getAllCourses());
                                    break;
                                case 2:
                                    loggedInInstructor.gradeStudent(dataManagerInstance.getAllAssessments(),
                                            dataManagerInstance.getAllCourses());
                                    break;
                                case 3:
                                    Helpers.updateCourseInfo(loggedInInstructor, dataManagerInstance.getAllCourses());
                                    dataManagerInstance.saveCourses(); // Save after course update
                                    break;
                                case 4:
                                    Helpers.updateInstructorProfile(loggedInInstructor);
                                    dataManagerInstance.saveInstructors(); // Save after profile update
                                    break;
                                case 5:
                                    loggedInInstructor.logout(loggedInInstructor);
                                    exitInstructor = true;
                                    break;
                                default:
                                    System.out.println("Invalid option.");
                            }

                        }
                        break;
                    case "admin":
                        Administrator temp = new Administrator();
                        Administrator loggedInAdministrator = Helpers.login(dataManagerInstance.getAllAdministrators(),
                                temp);

                        if (loggedInAdministrator == null) {
                            continue;
                        }
                        boolean exitAdmin = false;
                        while (!exitAdmin) {
                            Helpers.showAdminMenu();
                            int adminChoice = Helpers.getSafeIntInput("Option: ");

                            switch (adminChoice) {
                                case 1:
                                    Helpers.addStudent(loggedInAdministrator, dataManagerInstance.getAllStudents());
                                    break;
                                case 2:
                                    Helpers.removeStudent(loggedInAdministrator, dataManagerInstance.getAllStudents());
                                    break;
                                case 3:
                                    loggedInAdministrator.viewStudentList(dataManagerInstance.getAllStudents());
                                    break;
                                case 4:
                                    Helpers.addInstructor(loggedInAdministrator,dataManagerInstance.getAllInstructors());
                                    break;
                                case 5:
                                    Helpers.removeInstructor(loggedInAdministrator, dataManagerInstance.getAllInstructors());
                                    break;
                                case 6:
                                    loggedInAdministrator.viewInstructorList(dataManagerInstance.getAllInstructors());
                                    break;
                                case 7:
                                    Helpers.addCourse(loggedInAdministrator, dataManagerInstance.getAllCourses(),
                                            dataManagerInstance.getAllInstructors());

                                    break;
                                case 8:
                                    Helpers.closeCourse(loggedInAdministrator, dataManagerInstance.getAllCourses());
                                    break;
                                case 9:
                                    Helpers.adminUpdateStudentProfile(loggedInAdministrator, dataManagerInstance.getAllStudents());
                                    dataManagerInstance.saveStudents(); // Save after profile update
                                    break;
                                case 10:
                                    Helpers.adminUpdateInstructorProfile(loggedInAdministrator,dataManagerInstance.getAllInstructors());
                                    dataManagerInstance.saveInstructors(); // Save after profile update
                                    break;
                                case 11:
                                    Helpers.assignInstructor(loggedInAdministrator, dataManagerInstance.getAllCourses(),
                                            dataManagerInstance.getAllInstructors());
                                    break;
                                case 12:
                                    dataManagerInstance.viewEnrollmentStatistics();
                                    break;
                                case 13:
                                    dataManagerInstance.generateReports();
                                    break;
                                case 14:
                                    loggedInAdministrator.logout(loggedInAdministrator);
                                    exitAdmin = true;
                                    break;
                                default:
                                    System.out.println("Invalid option.");
                            }
                        }
                        break;
                    case "exit":
                        exit = true;
                        dataManagerInstance.saveAllData(); // Save all data before exiting
                        System.out.println("Goodbye.");
                        break;
                    default:

                        System.out.println("Invalid role. Try again.");
                }
            }
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
```
