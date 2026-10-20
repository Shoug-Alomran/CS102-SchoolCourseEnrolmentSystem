package schoolcourseenrolmentsystem;

import java.util.*;

public class Student extends User<Student> {
    // Attributes
    private int creditLimit;
    private List<Course> enrolledCourses;

    public Student() { }
    // Constructor
    public Student(String name, String id, String password, String email, String phoneNumber, String address, int
            creditLimit, List<Course> enrolledCourses) {
        super(name, id, password, email, phoneNumber, Role.STUDENT, address);
        setCreditLimit(creditLimit);
        // If the list is null, create a new one. Fixes NullPointerException.
        if (enrolledCourses != null) {
            this.enrolledCourses = enrolledCourses;
        } else {
            this.enrolledCourses = new ArrayList<>();
        }
    }
    //======================= Setters and Getters =======================
    public List<Course> getEnrolledCoursesList() {
        return enrolledCourses;
    }

    public int getCreditLimit() {
        return creditLimit;
    }

    public void setCreditLimit(int creditLimit) {
        if (creditLimit < 0) {
            System.out.println("Must be greater than 0");
            return;
        }
        this.creditLimit = creditLimit;
    }

    //======================= Methods =======================

    @Override
    public Student login(List<Student> listOfStudents, String id, String password) {
        for (Student student : listOfStudents) {
            if (student.getId().equals(id) && student.getPassword().equals(password)) {
                System.out.println("Student " + student.getName() + " logged in.");

                return student;
            }
        }
        System.out.println("No student record was found with the ID and password provided.");
        return null;
    }

    @Override
    public String logout(Student student) {
        return ("Student " + student.getName() + " logged out.");
    }

    // Count the hours of the courses already enrolled
    public int totalCreditLimit() {
        int total = 0;
        // This loop is to count how many courses and their toal hours
        for (Course course : enrolledCourses) {
            total += course.getCreditHours();
        }
        return total;
    }

    public void enroll_In_Course(Course course) {
        // 1. make sure credit limit is not excited and that the capacity is avaliable
        if (enrolledCourses.contains(course)) {
            System.out.printf("\nYou are already enrolled in (%s) (%s).", course.getCourseName(),
                    course.getCourseCode());
        } else if (course.isFull()) {
            System.out.println("\nCannot enroll in " + course.getCourseName() + " - course is full.");
        } // Check if the enrollment status is open or not
        else if (course.getEnrollmentStatus() == Course.EnrollmentStatusEnum.Closed) {
            System.out.println("\nEnrollment status is closed.");
        } // Previously enrolled hours + new hours
        else if (totalCreditLimit() + course.getCreditHours() > creditLimit) {
            System.out.println("\nCannot enroll in " + course.getCourseName() + " - credit limit exceeded.");
        } else {
            /// Adding the current student to the course's list of enrolled students.

            course.getEnrolledStudents().add(this);
            /// Adding the course to the student's list of enrolled courses.
            this.enrolledCourses.add(course);
            System.out.println("\n" + getName() + " enrolled successfully");
        }
    }

    public void dropCourse(Course course) {
        if (!enrolledCourses.contains(course)) {
            System.out.printf("%s is not enrolled in (%s) (%s).", getName(), course.getCourseName(),
                    course.getCourseCode());
        } else if (enrolledCourses.contains(course)
                && course.getEnrollmentStatus() == Course.EnrollmentStatusEnum.Closed) {
            System.out.println("Drop period is closed.");
        } else if (enrolledCourses.contains(course)
                && course.getEnrollmentStatus() == Course.EnrollmentStatusEnum.Open) {
            this.enrolledCourses.remove(course);
            System.out.printf("%s has successfully dropped (%s) (%s).", getName(), course.getCourseName(),
                    course.getCourseCode());
        }
    }

    public void viewCreditLimit(List<Student> listOfStudents) {
        for (Student student : listOfStudents) {
            System.out.println("Your credit limit is: " + student.getCreditLimit());

            // (condition) ? (value if true) : (value if false);
            int enrolledHours = (student.getEnrolledCoursesList() != null) ? student.enrolledInHours() : 0;
            System.out.println("Remaining credit limit is: " + (student.getCreditLimit() - enrolledHours) + " hours.");
            break;
        }
    }

    public int enrolledInHours() {
        int total = 0;
        if (enrolledCourses != null) {
            for (Course course : enrolledCourses) {

                total += course.getCreditHours();
            }
        }
        return total;
    }

    public void viewEnrolledCourses() {
        if (enrolledCourses.isEmpty()) {
            System.out.println(getName() + " is not enrolled in any courses.");
        } else {
            System.out.println(getName() + " is enrolled in: ");
            int index = 1;
            for (Course course : enrolledCourses) {
                System.out.printf(index + "- (%s) (%s) (%s). The schedule is: %s.", course.getCourseName(),
                        course.getCourseCode(), course.getCreditHours(), course.getSchedule());
                index++;
            }
        }
    }

    public void viewGrades(List<Assessment> listOfGrades) {
        System.out.println("\nWhat would you like to view?\n1. View a specific exam score.\n2. View all grades in a
                course.\n3. View total average in a course.");

        int choice = Helpers.getSafeIntInput("\nOption: ");
        Assessment temp = new Assessment(null, null, null, 0.0, null);

        if (choice == 1) {
            temp.viewSpecificExamScore(listOfGrades, this);
        } else if (choice == 2) {
            temp.viewAllGradesForCourse(listOfGrades, this);
        } else if (choice == 3) {
            List<Course> courses = this.getEnrolledCoursesList();

            if (courses.isEmpty()) {
                System.out.println("\nYou are not enrolled in any courses.");
                return;

            }
            System.out.println("\nSelect a course:");
            for (int i = 0; i < courses.size(); i++) {
                System.out.printf((i + 1) + ".%s ( %s )", courses.get(i).getCourseName(), courses.get(i).getCourseCode());
            }
            int courseChoice = Helpers.getSafeIntInput("\nOption: ");
            if (courseChoice < 1 || courseChoice > courses.size()) {
                System.out.println("Invalid course selection.");
                return;
            }
            String courseCode = courses.get(courseChoice - 1).getCourseCode();
            temp.viewTotalAverageGrade(listOfGrades, this.getId(), courseCode);
        } else {
            System.out.println("Invalid choice.");
        }
    }

    public void viewAvailableCourses(List<Course> listOfCourses) {
        boolean avaliableCourses = false;
        System.out.println("\nAvailable courses are: ");
        for (Course course : listOfCourses) {
            if (course.isFull() == false && course.getEnrollmentStatus() == Course.EnrollmentStatusEnum.Open) {
                avaliableCourses = true;
                System.out.println("- (Course name: " + course.getCourseName() + ") (Course code: " +
                        course.getCourseCode() + ") (Course schedule: " + course.getSchedule() + ") (Course instructor: " +
                        course.getInstructor()+ ") (Course capacity: " + course.getCapacity() + ").\n");
            }
        }
        if (!avaliableCourses) {
            System.out.println("No courses are avaliable.");
        }
    }

    public void updateStudentPersonalInfo(String newPassword, String newEmail, String newPhoneNumber,
            String newAddress) {
        setPassword(newPassword);
        setEmail(newEmail);

        setPhoneNumber(newPhoneNumber);
        setAddress(newAddress);
        System.out.println("\nStudent " + getName() + "'s information updated.");
    }

    @Override
    public String toString() {
        return String.format("-ID: %s Name: %s", this.getId(), this.getName());
    }
}
