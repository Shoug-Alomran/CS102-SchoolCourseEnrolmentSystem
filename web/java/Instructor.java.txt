package schoolcourseenrolmentsystem;

import java.util.*;

public class Instructor extends User<Instructor> {
    // Constructor
    public Instructor() {
    }

    public Instructor(String name, String id, String password, String email, String phoneNumber,
            String address, List<Student> enrolledStudents) {
        super(name, id, password, email, phoneNumber, Role.INSTRUCTOR, address);
    }

    // ======================= Methods =======================
    @Override
    public Instructor login(List<Instructor> listOfInstructors, String id, String password) {
        for (Instructor instructor : listOfInstructors) {
            if (instructor.getId().equals(id) && instructor.getPassword().equals(password)) {
                System.out.println("Instructor " + instructor.getName() + " logged in.\n");
                return instructor;
            }
        }
        System.out.println("No instructor record was found with the ID and password provided.");
        return null;

    }
    @Override
    public String logout(Instructor instructor) {
        return ("Instructor " + instructor.getName() + " logged out.");
    }

    public void viewEnrolledStudents(Instructor instructor, List<Course> listOfCourses) {
        boolean enrolledCourse = false;
        // Look through all the courses
        for (Course course : listOfCourses) {
            // Make sure that the instructor is actually assigned to the course
            if (course.getInstructor() != null && course.getInstructor().getId().equals(instructor.getId())) {
                enrolledCourse = true;
                // The instructor might teach multiple courses
                System.out.printf("\n(Course: %s) (Code: %s)", course.getCourseName(), course.getCourseCode());
                course.getEnrolledStudents();

                // Make sure there are actually students enrolled in the course.
                // Update the list.
                List<Student> courseStudents = course.getEnrolledStudents();
                if (courseStudents == null || courseStudents.isEmpty()) {
                    System.out.println("No students enrolled in this course.");
                } else {
                    for (Student student : courseStudents) {
                        System.out.printf("\n-Student: %s, ID: %s, Email: %s, Phone number: %s", student.getName(),
                                student.getId(), student.getEmail(), student.getPhoneNumber());
                    }
                }
            }
        }
        if (!enrolledCourse) {
            System.out.println("Instructor " + instructor.getName() + " is not assigned to any courses.");
        }
    }

    public void gradeStudent(List<Assessment> listOfGrades, List<Course> listOfCourses) {
        Scanner input = new Scanner(System.in);

        try {
            // Step 1: Show instructor's courses
            List<Course> instructorCourses = new ArrayList<>();
            System.out.println("\nCourses you're assigned to:");
            for (Course course : listOfCourses) {
                if (course.getInstructor() != null && course.getInstructor().getId().equals(this.getId())) {
                    instructorCourses.add(course);
                    System.out.println((instructorCourses.size()) + ". " + course.getCourseName() + " (" +
                            course.getCourseCode() + ")");
                }
            }
            if (instructorCourses.isEmpty()) {
                System.out.println("You're not assigned to any courses.");
                return;
            }
            int courseChoice = Helpers.getSafeIntInput("Select a course to grade: ");
            if (courseChoice < 1 || courseChoice > instructorCourses.size()) {
                System.out.println("Invalid selection.");
                return;
            }
            Course selectedCourse = instructorCourses.get(courseChoice - 1);

            // Step 2: Select student
            List<Student> enrolled = selectedCourse.getEnrolledStudents();
            if (enrolled.isEmpty()) {
                System.out.println("No students enrolled in this course.");
                return;
            }
            System.out.println("\nStudents in this course:");
            for (int i = 0; i < enrolled.size(); i++) {
                System.out.printf((i + 1) + ".%s (ID: %s)", enrolled.get(i).getName(), enrolled.get(i).getId());
            }

            int studentChoice = Helpers.getSafeIntInput("\nSelect a student to grade: ");
            if (studentChoice < 1 || studentChoice > enrolled.size()) {
                System.out.println("Invalid student selection.");
                return;

            }
            Student selectedStudent = enrolled.get(studentChoice - 1);

            // Step 3: Choose exam type
            Assessment.ExamType[] examTypes = Assessment.ExamType.values();
            System.out.println("\nSelect the assessment type to grade:");
            for (int i = 0; i < examTypes.length; i++) {
                System.out.println((i + 1) + ". " + examTypes[i]);
            }
            int examChoice = Helpers.getSafeIntInput("Choice: ");
            if (examChoice < 1 || examChoice > examTypes.length) {
                System.out.println("Invalid selection.");
                return;
            }
            Assessment.ExamType selectedExamType = examTypes[examChoice - 1];

            // Step 4: Enter score
            double score;
            while (true) {
                System.out.print("Enter score (0-100): ");
                try {
                    score = input.nextDouble();
                    input.nextLine(); // Buffer
                    if (score < 0 || score > 100) {
                        System.out.println("Score must be between 0 and 100.");
                    } else {
                        break;
                    }
                } catch (InputMismatchException e) {
                    System.out.println("Invalid input. Please enter a number.");
                    input.nextLine(); // Clear input
                }
            }

            // Step 5: Assign or update grade
            boolean updated = false;
            for (Assessment g : listOfGrades) {

                if (g.getStudentId().equals(selectedStudent.getId())
                        && g.getCourseCode().equals(selectedCourse.getCourseCode())
                        && g.getExamType().equals(selectedExamType)) {
                    g.setScore(score);
                    System.out.println("Grade updated successfully.");
                    updated = true;
                    break;
                }
            }
            if (!updated) {
                Assessment newAssessment = new Assessment(selectedStudent.getId(),
                        selectedCourse.getCourseCode(), selectedExamType, score, selectedExamType.toString());
                listOfGrades.add(newAssessment);
                System.out.println("Grade recorded successfully.");
            }
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }

    public void updateCourseInfo(String courseCode, List<Course> listOfCourses, String newSchedule, String
            newDescription) {

        // Now find the actual Course object
        Course courseToUpdate = null;
        for (Course course : listOfCourses) {
            if (course.getCourseCode().equals(courseCode)) {
                courseToUpdate = course;
                break;
            }
        }
        if (courseToUpdate == null) {
            System.out.println("Course with code " + courseCode + " not found.");
            return;
        }
        if (courseToUpdate != null) {
            Instructor assignedInstructor = courseToUpdate.getInstructor();

            if (assignedInstructor != null && assignedInstructor.getId().equals(this.getId())) {
                courseToUpdate.setSchedule(newSchedule);
                courseToUpdate.setDescription(newDescription);

                System.out.printf("Instructor %s's course information updated for %s", assignedInstructor.getName(),
                        courseToUpdate.getCourseName());
            } else if (assignedInstructor != null) {
                System.out.printf("%s with the ID number: %s is not assigned to %s.", assignedInstructor.getName(),
                        assignedInstructor.getId(), courseToUpdate.getCourseName());
            }
            // You don't see it but its basically (assignedInstructor == null);
            else {
                System.out.printf("No instructor assigned to %s.", courseToUpdate.getCourseName());
            }
        }
    }

    public void updateInstructorPersonalInfo(String newPassword, String newEmail, String newPhoneNumber, String
            newAddress) {
        // No need to check if they match because instructors are already logged in.
        setPassword(newPassword);
        setEmail(newEmail);
        setPhoneNumber(newPhoneNumber);
        setAddress(newAddress);
        System.out.println("Instructor " + getName() + "'s information updated.");
    }

    @Override
    public String toString() {
        return String.format("-ID: %s Name: %s", this.getId(), this.getName());
    }
}
