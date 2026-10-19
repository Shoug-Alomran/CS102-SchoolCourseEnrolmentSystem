---
title: "Administrator Class - Java Source Code"
description: "Full Java source of the Administrator class: managing students, instructors and courses, assigning instructors and closing courses."
---

# Administrator Class - Source Code

Full Java source of the Administrator class: managing students, instructors and courses, assigning instructors and closing courses.

For an explanation of how this class works, see the [Administrator class guide](../administrator.md). This listing comes from the [CS102 project report](../project-report.md).

```java title="Administrator.java" linenums="1"
package schoolcourseenrolmentsystem;

import java.util.*;
import schoolcourseenrolmentsystem.Course.EnrollmentStatusEnum;

public class Administrator extends User<Administrator> {
    // Constructors
    // We must define the default constructor in case we define any other custom
    // constructors
    public Administrator() {
    }

    public Administrator(String name, String id, String password, String email, String phoneNumber, String address) {
        super(name, id, password, email, phoneNumber, User.Role.ADMIN, address);
    }

    // Methods

    // Login/logout & role
    @Override
    public Administrator login(List<Administrator> listOfAdministrators, String id, String password) {
        Administrator returnAdmin = null;
        for (Administrator administrator : listOfAdministrators) {
            if (administrator.getId().equals(id) && administrator.getPassword().equals(password)) {
                System.out.println("Administrator " + administrator.getName() + " logged in.");
                returnAdmin = administrator;
                break;
            }
            System.out.println("No admin record was found with the ID and password provided.");
        }
        return returnAdmin;
    }

    @Override
    public String logout(Administrator administrators) {
        return ("Administrator " + administrators.getName() + " logged out.");
    }

    // Add and remove users

    /// Loop used to iterate over all the students/instructors.
    /// An Iterator keeps track of the current position safely, and when you call
    /// remove(), it tells the collection to safely remove the current element
    /// without invalidating the loop.
    public boolean removeStudent(List<Student> listOfStudents, String targetId) {
        Iterator<Student> iterator = listOfStudents.iterator();
        while (iterator.hasNext()) {
            Student specificStudent = iterator.next();
            if (specificStudent.getId().equals(targetId)) {
                iterator.remove();
                System.out.println(specificStudent.getName() + " with the ID: " + specificStudent.getId() + " has been
                        successfully removed");
                return true;
            }
        }
        System.out.println(targetId + " is not found.");
        return false;
    }

    public boolean removeInstructor(List<Instructor> listOfInstructors, String targetId) {
        // Loop used to iterate over all the instructors
        Iterator<Instructor> iterator = listOfInstructors.iterator();
        while (iterator.hasNext()) {
            Instructor specificInstructor = iterator.next();
            if (specificInstructor.getId().equals(targetId)) {
                iterator.remove();
                System.out.println(specificInstructor.getName() + " with the ID: " + specificInstructor.getId() + " removed
                        successfully.");
                return true;
            }
        }
        System.out.println("Instructor with the ID: " + targetId + " not found.");
        return false;
    }

    public void addInstructor(Instructor specificInstructor, List<Instructor> listOfInstructors) {

        listOfInstructors.add(specificInstructor);
        System.out.printf("Instructor added: %s with the ID: %s", specificInstructor.getName(), specificInstructor.getId());
    }

    public void addStudent(Student specificStudent, List<Student> listOfStudents) {
        listOfStudents.add(specificStudent);
        System.out.printf("Student added: %s with the ID: %s", specificStudent.getName(), specificStudent.getId());
    }

    // Update user info.

    public void updateStudent(String targetId, List<Student> listOfStudents, String newName, String newId, String
            newPassword, String newEmail, String newPhoneNumber, User.Role newRole, String newAddress) {

        Student updateStudentInfo = null;
        for (Student student : listOfStudents) {
            if (student.getId().equals(targetId)) {
                updateStudentInfo = student;
                break;
            }
        }
        if (updateStudentInfo != null) {
            updateStudentInfo.setName(newName);
            updateStudentInfo.setPassword(newPassword);
            updateStudentInfo.setEmail(newEmail);
            updateStudentInfo.setPhoneNumber(newPhoneNumber);
            updateStudentInfo.setRole(newRole);
            updateStudentInfo.setAddress(newAddress);
        } else {
            System.out.println("Student with the ID " + targetId + " not found.");
        }
    }

    public void updateInstructor(String instructorTargetId, List<Instructor> listOfInstructors, String newName, String
            newPassword, String newEmail, String newPhoneNumber, User.Role newRole, String newAddress) {

        Instructor updateInstructorInfo = null;

        for (Instructor instructor : listOfInstructors) {
            if (instructor.getId().equals(instructorTargetId)) {
                updateInstructorInfo = instructor;
                break;
            }
        }
        if (updateInstructorInfo != null) {
            updateInstructorInfo.setName(newName);
            updateInstructorInfo.setPassword(newPassword);
            updateInstructorInfo.setEmail(newEmail);
            updateInstructorInfo.setPhoneNumber(newPhoneNumber);
            updateInstructorInfo.setRole(newRole);
            updateInstructorInfo.setAddress(newAddress);
        } else {
            System.out.println("Instructor with the ID " + instructorTargetId + " not found.");
        }
    }
    // Course related.
    public void addCourse(List<Course> listOfCourses, Course specificCourse) {
        if (listOfCourses.add(specificCourse)) {
            System.out.printf("Course added: (%s) (%s) succesfully.", specificCourse.getCourseName(),
                    specificCourse.getCourseCode());
        } else {
            System.out.println("Course already exists: " + specificCourse.getCourseName());
        }
    }

    public void assignInstructor(Course specificCourse, Instructor specificInstructor) {
        if (specificCourse.getInstructor() == null) {
            specificCourse.setInstructor(specificInstructor);
            System.out.printf("Instructor %s is assigned to %s", specificInstructor.getName(),
                    specificCourse.getCourseName());
        } else if (specificCourse.getInstructor().equals(specificInstructor)) {
            System.out.printf("Instructor %s is already assigned to %s", specificInstructor.getName(),
                    specificCourse.getCourseName());
        } else {
            System.out.println("Course already has a different instructor assigned.");

        }
    }

    public void closeCourse(Course specificCourse, List<Course> listOfCourses) {
        if (listOfCourses.contains(specificCourse)) {
            if (specificCourse.getEnrolledStudents().size() >= specificCourse.getCapacity()) {
                System.out.println(specificCourse.getCourseName() + " is at full capacity.");
                specificCourse.setEnrollmentStatus(EnrollmentStatusEnum.Closed);
            } else if (specificCourse.getEnrollmentStatus() == Course.EnrollmentStatusEnum.Closed) {
                System.out.println(specificCourse.getCourseName() + " enrollment status is closed.");
            }
        } else if (!listOfCourses.contains(specificCourse)) {
            System.out.println(specificCourse.getCourseName() + " not found.");
        } else {
            System.out.println(specificCourse.getCourseName() + " still has available capacity.");
        }
    }

    public void viewStudentList(List<Student> listOfStudents) {
        if (listOfStudents == null || listOfStudents.isEmpty()) {
            System.out.println("\nNo students are on record.");
        } else {
            for (Student student : listOfStudents) {
                System.out.println(student.toString());
            }
        }
    }

    public void viewInstructorList(List<Instructor> instructors) {
        if (instructors == null || instructors.isEmpty()) {
            System.out.println("\nNo instructors are on record.");
        } else {
            for (Instructor instructor : instructors) {
                System.out.println(instructor.toString());
            }
        }
    }

}
```
