package schoolcourseenrolmentsystem;

import java.io.*;
import java.util.*;

public class dataManager {

    private static dataManager instance = null;

    // Main data lists
    private List<Instructor> instructors;
    private List<Administrator> administrators;
    private List<Student> students;
    private List<Course> courses;
    private List<Assessment> grades;

    // File paths

    private static final String STUDENTS_FILE = "students.txt";
    private static final String INSTRUCTORS_FILE = "instructors.txt";
    private static final String ADMINISTRATORS_FILE = "administrators.txt";
    private static final String COURSES_FILE = "courses.txt";
    private static final String ASSESSMENTS_FILE = "assessments.txt";
    private static final String DELIMITER = "\\|";

    // Private constructor to prevent instantiation
    dataManager() {
        instructors = new ArrayList<>();
        administrators = new ArrayList<>();
        students = new ArrayList<>();
        courses = new ArrayList<>();
        grades = new ArrayList<>();
        System.out.println("Testing Constructor");
    }

    public static synchronized dataManager getInstance() {
        if (instance == null) {
            instance = new dataManager();
        }
        return instance;
    }

    // Load all data from files
    void loadAllData() {
        loadStudents();
        loadInstructors();
        loadAdministrators();
        loadCourses();
        loadAssessments();
    }

    // Save all data to files
    public void saveAllData() {
        saveStudents();
        saveInstructors();

        saveAdministrators();
        saveCourses();
        saveAssessments();
    }

    // Load Students from file
    private void loadStudents() {
        try (BufferedReader reader = new BufferedReader(new FileReader(STUDENTS_FILE))) {
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println("Loading student: " + line);
                String[] parts = line.split(DELIMITER);
                if (parts.length >= 7) {
                    String name = parts[0];
                    String id = parts[1];
                    String password = parts[2];
                    String email = parts[3];
                    String phoneNumber = parts[4];
                    String address = parts[5];
                    int creditLimit = Integer.parseInt(parts[6]);

                    List<Course> enrolledCourses = new ArrayList<>();

                    if (parts.length > 7 && !parts[7].isEmpty()) {
                        String[] courseCodes = parts[7].split(",");
                        for (String code : courseCodes) {
                            Course course = getCourseByCode(code.trim());
                            if (course != null) {
                                enrolledCourses.add(course);
                            }
                        }
                    }
                    Student student = new Student(name, id, password, email, phoneNumber, address,
                            creditLimit,enrolledCourses);
                    System.out.println(student);
                    if (isStudentIdUnique(id)) {
                        students.add(student);

                    }
                }
            }
        } catch (FileNotFoundException e) {
            System.out.println("Students file not found. Starting with empty student list.");
        } catch (IOException e) {
            System.out.println("Error reading students file: " + e.getMessage());
        } catch (NumberFormatException e) {
            System.out.println("Error parsing student data: " + e.getMessage());
        }
    }
    // Save Students to file
    void saveStudents() {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(STUDENTS_FILE))) {
            for (Student student : students) {
                StringBuilder courseCodes = new StringBuilder();
                for (Course course : student.getEnrolledCoursesList()) {
                    if (courseCodes.length() > 0) {
                        courseCodes.append(",");
                    }
                    courseCodes.append(course.getCourseCode());
                }
                String line = String.join("|",
                        student.getName(),
                        student.getId(),
                        student.getPassword(),
                        student.getEmail(),
                        student.getPhoneNumber(),
                        student.getAddress(),
                        String.valueOf(student.getCreditLimit()),
                        courseCodes.toString());
                writer.write(line);
                writer.newLine();
            }
        } catch (IOException e) {
            System.out.println("Error writing students file: " + e.getMessage());
        }

    }

    // Load Instructors from file
    private void loadInstructors() {
        try (BufferedReader reader = new BufferedReader(new FileReader(INSTRUCTORS_FILE))) {
            String line;
            while ((line = reader.readLine()) != null) {
                String[] parts = line.split(DELIMITER);
                if (parts.length >= 6) {
                    String name = parts[0];
                    String id = parts[1];
                    String password = parts[2];
                    String email = parts[3];
                    String phoneNumber = parts[4];
                    String address = parts[5];
                    Instructor instructor = new Instructor(name, id, password, email, phoneNumber, address, new
                            ArrayList<>());
                    if (isInstructorIdUnique(id)) {
                        instructors.add(instructor);
                    }
                }
            }
        } catch (FileNotFoundException e) {
            System.out.println("Instructors file not found. Starting with empty instructor list.");
        } catch (IOException e) {
            System.out.println("Error reading instructors file: " + e.getMessage());
        }
    }
    // Save Instructors to file
    void saveInstructors() {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(INSTRUCTORS_FILE))) {
            for (Instructor instructor : instructors) {
                String line = String.join("|",
                        instructor.getName(),
                        instructor.getId(),
                        instructor.getPassword(),
                        instructor.getEmail(),

                        instructor.getPhoneNumber(),
                        instructor.getAddress());
                writer.write(line);
                writer.newLine();
            }
        } catch (IOException e) {
            System.out.println("Error writing instructors file: " + e.getMessage());
        }
    }
    // Load Administrators from file
    private void loadAdministrators() {
        try (BufferedReader reader = new BufferedReader(new FileReader(ADMINISTRATORS_FILE))) {
            String line;
            while ((line = reader.readLine()) != null) {
                String[] parts = line.split(DELIMITER);
                if (parts.length >= 6) {
                    String name = parts[0];
                    String id = parts[1];
                    String password = parts[2];
                    String email = parts[3];
                    String phoneNumber = parts[4];
                    String address = parts[5];
                    Administrator admin = new Administrator(name, id, password, email, phoneNumber, address);
                    if (isAdminIdUnique(id)) {
                        administrators.add(admin);
                    }
                }
            }
        } catch (FileNotFoundException e) {
            System.out.println("Administrators file not found. Starting with default admin.");
        } catch (IOException e) {
            System.out.println("Error reading administrators file: " + e.getMessage());
        }
    }
    // Save Administrators to file
    private void saveAdministrators() {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(ADMINISTRATORS_FILE))) {

            for (Administrator admin : administrators) {
                String line = String.join("|",
                        admin.getName(),
                        admin.getId(),
                        admin.getPassword(),
                        admin.getEmail(),
                        admin.getPhoneNumber(),
                        admin.getAddress());
                writer.write(line);
                writer.newLine();
            }
        } catch (IOException e) {
            System.out.println("Error writing administrators file: " + e.getMessage());
        }
    }
    // Load Courses from file
    private void loadCourses() {
        try (BufferedReader reader = new BufferedReader(new FileReader(COURSES_FILE))) {
            String line;
            while ((line = reader.readLine()) != null) {
                String[] parts = line.split(DELIMITER);
                if (parts.length >= 8) {
                    String courseName = parts[0];
                    String courseCode = parts[1];
                    String schedule = parts[2].isEmpty() ? null : parts[2];
                    String description = parts[3].isEmpty() ? null : parts[3];
                    Course.EnrollmentStatusEnum status = Course.EnrollmentStatusEnum.valueOf(parts[4]);
                    Instructor instructor = parts[5].isEmpty() ? null : getInstructorById(parts[5]);
                    int capacity = Integer.parseInt(parts[6]);
                    int creditHours = Integer.parseInt(parts[7]);
                    List<Student> enrolledStudents = new ArrayList<>();
                    if (parts.length > 8 && !parts[8].isEmpty()) {
                        String[] studentIds = parts[8].split(",");
                        for (String id : studentIds) {
                            Student student = getStudentById(id.trim());
                            if (student != null) {
                                enrolledStudents.add(student);

                            }
                        }
                    }
                    Course course = new Course(courseName, courseCode, schedule, description, status, instructor,
                            capacity, new ArrayList<>(), creditHours);
                    course.setEnrolledStudents(enrolledStudents);
                    if (isCourseCodeUnique(courseCode)) {
                        courses.add(course);
                    }
                }
            }
        } catch (FileNotFoundException e) {
            System.out.println("Courses file not found. Starting with empty course list.");
        } catch (IOException e) {
            System.out.println("Error reading courses file: " + e.getMessage());
        } catch (IllegalArgumentException e) {
            System.out.println("Error parsing course data: " + e.getMessage());
        }
    }
    // Save Courses to file
    void saveCourses() {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(COURSES_FILE))) {
            for (Course course : courses) {
                StringBuilder studentIds = new StringBuilder();
                for (Student student : course.getEnrolledStudents()) {
                    if (studentIds.length() > 0) {
                        studentIds.append(",");
                    }
                    studentIds.append(student.getId());
                }
                String instructorId = course.getInstructor() != null ? course.getInstructor().getId() : "";
                String schedule = course.getSchedule() != null ? course.getSchedule() : "";
                String description = course.getDescription() != null ? course.getDescription() : "";
                String line = String.join("|",
                        course.getCourseName(),
                        course.getCourseCode(),
                        schedule,

                        description,
                        course.getEnrollmentStatus().toString(),
                        instructorId,
                        String.valueOf(course.getCapacity()),
                        String.valueOf(course.getCreditHours()),
                        studentIds.toString());
                writer.write(line);
                writer.newLine();
            }
        } catch (IOException e) {
            System.out.println("Error writing courses file: " + e.getMessage());
        }
    }
    // Load Assessments from file
    private void loadAssessments() {
        try (BufferedReader reader = new BufferedReader(new FileReader(ASSESSMENTS_FILE))) {
            String line;
            while ((line = reader.readLine()) != null) {
                String[] parts = line.split(DELIMITER);
                if (parts.length >= 5) {
                    String studentId = parts[0];
                    String courseCode = parts[1];
                    Assessment.ExamType examType = Assessment.ExamType.valueOf(parts[2]);
                    double score = Double.parseDouble(parts[3]);
                    String assessmentName = parts[4];
                    Assessment assessment = new Assessment(studentId, courseCode, examType, score,
                            assessmentName);
                    grades.add(assessment);
                }
            }
        } catch (FileNotFoundException e) {
            System.out.println("Assessments file not found. Starting with empty assessment list.");
        } catch (IOException e) {
            System.out.println("Error reading assessments file: " + e.getMessage());
        } catch (IllegalArgumentException e) {
            System.out.println("Error parsing assessment data: " + e.getMessage());
        }

    }
    // Save Assessments to file
    private void saveAssessments() {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(ASSESSMENTS_FILE))) {
            for (Assessment assessment : grades) {
                String line = String.join("|",
                        assessment.getStudentId(),
                        assessment.getCourseCode(),
                        assessment.getExamType().toString(),
                        String.valueOf(assessment.getScore()),
                        assessment.getAssessmentName());
                writer.write(line);
                writer.newLine();
            }
        } catch (IOException e) {
            System.out.println("Error writing assessments file: " + e.getMessage());
        }
    }
    // Methods for Students
    public void addStudent(Student student) {
        if (student == null) {
            System.out.println("Error: Student cannot be null.");
            return;
        }
        if (isStudentIdUnique(student.getId())) {
            students.add(student);
            saveStudents();
            System.out.printf("Student added: %s with ID: %s%n", student.getName(), student.getId());
        } else {
            System.out.println("Error: Student ID " + student.getId() + " already exists.");
        }
    }

    public boolean removeStudent(String studentId) {
        Iterator<Student> iterator = students.iterator();
        while (iterator.hasNext()) {
            Student student = iterator.next();

            if (student.getId().equals(studentId)) {
                iterator.remove();
                saveStudents();
                System.out.printf("Student %s with ID: %s removed successfully.%n", student.getName(), studentId);
                return true;
            }
        }
        System.out.println("Student with ID: " + studentId + " not found.");
        return false;
    }

    public Student getStudentById(String studentId) {
        for (Student student : students) {
            if (student.getId().equals(studentId)) {
                return student;
            }
        }
        return null;
    }

    public List<Student> getAllStudents() {
        return students;
    }

    // Methods for Instructors
    public void addInstructor(Instructor instructor) {
        if (instructor == null) {
            System.out.println("Error: Instructor cannot be null.");
            return;
        }
        if (isInstructorIdUnique(instructor.getId())) {
            instructors.add(instructor);
            saveInstructors();
            System.out.printf("Instructor added: %s with ID: %s%n", instructor.getName(), instructor.getId());
        } else {
            System.out.println("Error: Instructor ID " + instructor.getId() + " already exists.");
        }

    }

    public boolean removeInstructor(String instructorId) {
        Iterator<Instructor> iterator = instructors.iterator();
        while (iterator.hasNext()) {
            Instructor instructor = iterator.next();
            if (instructor.getId().equals(instructorId)) {
                for (Course course : courses) {
                    if (course.getInstructor() != null && course.getInstructor().getId().equals(instructorId)) {
                        course.setInstructor(null);
                    }
                }
                iterator.remove();
                saveInstructors();
                saveCourses();
                System.out.printf("Instructor %s with ID: %s removed successfully.%n", instructor.getName(),instructorId);
                return true;
            }
        }
        System.out.println("Instructor with ID: " + instructorId + " not found.");
        return false;
    }

    public Instructor getInstructorById(String instructorId) {
        for (Instructor instructor : instructors) {
            if (instructor.getId().equals(instructorId)) {
                return instructor;
            }
        }
        return null;
    }

    public List<Instructor> getAllInstructors() {
        return instructors;
    }

    // Methods for Administrators

    public void addAdministrator(Administrator admin) {
        if (admin == null) {
            System.out.println("Error: Administrator cannot be null.");
            return;
        }
        if (isAdminIdUnique(admin.getId())) {
            administrators.add(admin);
            saveAdministrators();
            System.out.printf("Administrator added: %s with ID: %s%n", admin.getName(), admin.getId());
        } else {
            System.out.println("Error: Administrator ID " + admin.getId() + " already exists.");
        }
    }

    public Administrator getAdminById(String adminId) {
        for (Administrator admin : administrators) {
            if (admin.getId().equals(adminId)) {
                return admin;
            }
        }
        return null;
    }

    public List<Administrator> getAllAdministrators() {
        return administrators;
    }

    // Methods for Courses
    public void addCourse(Course course) {
        if (course == null) {
            System.out.println("Error: Course cannot be null.");
            return;
        }
        if (isCourseCodeUnique(course.getCourseCode())) {
            courses.add(course);
            saveCourses();

            System.out.printf("Course added: %s (%s) successfully.%n", course.getCourseName(),
                    course.getCourseCode());
        } else {
            System.out.println("Error: Course code " + course.getCourseCode() + " already exists.");
        }
    }

    public boolean removeCourse(String courseCode) {
        Iterator<Course> iterator = courses.iterator();
        while (iterator.hasNext()) {
            Course course = iterator.next();
            if (course.getCourseCode().equals(courseCode)) {
                for (Student student : course.getEnrolledStudents()) {
                    student.getEnrolledCoursesList().remove(course);
                }
                iterator.remove();
                saveCourses();
                saveStudents();
                System.out.printf("Course %s (%s) removed successfully.%n", course.getCourseName(), courseCode);
                return true;
            }
        }
        System.out.println("Course with code: " + courseCode + " not found.");
        return false;
    }

    public Course getCourseByCode(String courseCode) {
        for (Course course : courses) {
            if (course.getCourseCode().equals(courseCode)) {
                return course;
            }
        }
        return null;
    }

    public List<Course> getAllCourses() {
        return courses;

    }
    // =======================Methods for Assessments=======================
    public void addAssessment(Assessment assessment) {
        if (assessment == null) {
            System.out.println("Error: Assessment cannot be null.");
            return;
        }
        grades.add(assessment);
        saveAssessments();
        System.out.println("Assessment recorded successfully.");
    }

    public void updateAssessment(String studentId, String courseCode, Assessment.ExamType examType, double
            score) {
        for (Assessment assessment : grades) {
            if (assessment.getStudentId().equals(studentId) &&
                    assessment.getCourseCode().equals(courseCode) &&
                    assessment.getExamType() == examType) {
                assessment.setScore(score);
                saveAssessments();
                System.out.println("Assessment updated successfully.");
                return;
            }
        }
        Assessment newAssessment = new Assessment(studentId, courseCode, examType, score, examType.name());
        grades.add(newAssessment);
        saveAssessments();
        System.out.println("Assessment recorded successfully.");
    }

    public List<Assessment> getAssessmentsByStudentAndCourse(String studentId, String courseCode) {
        List<Assessment> studentAssessments = new ArrayList<>();
        for (Assessment assessment : grades) {
            if (assessment.getStudentId().equals(studentId) && assessment.getCourseCode().equals(courseCode)) {
                studentAssessments.add(assessment);
            }
        }

        return studentAssessments;
    }

    public List<Assessment> getAllAssessments() {
        return grades;
    }

    // Validation methods
    private boolean isStudentIdUnique(String studentId) {
        return students.stream().noneMatch(student -> student.getId().equals(studentId));
    }

    private boolean isInstructorIdUnique(String instructorId) {
        return instructors.stream().noneMatch(instructor -> instructor.getId().equals(instructorId));
    }
    private boolean isAdminIdUnique(String adminId) {
        return administrators.stream().noneMatch(admin -> admin.getId().equals(adminId));
    }

    private boolean isCourseCodeUnique(String courseCode) {
        return courses.stream().noneMatch(course -> course.getCourseCode().equals(courseCode));
    }

    //======================= Utility methods=======================
    public void assignInstructorToCourse(String courseCode, String instructorId) {
        Course course = getCourseByCode(courseCode);
        Instructor instructor = getInstructorById(instructorId);

        if (course == null) {
            System.out.println("Error: Course with code " + courseCode + " not found.");
            return;
        }
        if (instructor == null) {
            System.out.println("Error: Instructor with ID " + instructorId + " not found.");
            return;
        }

        if (course.getInstructor() == null) {
            course.setInstructor(instructor);
            saveCourses();
            System.out.printf("Instructor %s assigned to %s.%n", instructor.getName(), course.getCourseName());
        } else if (course.getInstructor().equals(instructor)) {
            System.out.printf("Instructor %s is already assigned to %s.%n", instructor.getName(),
                    course.getCourseName());
        } else {
            System.out.println("Course already has a different instructor assigned.");
        }
    }

    public void enrollStudentInCourse(String studentId, String courseCode) {
        Student student = getStudentById(studentId);
        Course course = getCourseByCode(courseCode);

        if (student == null) {
            System.out.println("Error: Student with ID " + studentId + " not found.");
            return;
        }
        if (course == null) {
            System.out.println("Error: Course with code " + courseCode + " not found.");
            return;
        }
        student.enroll_In_Course(course);
        if (course.getEnrolledStudents().contains(student)) {
            saveStudents();
            saveCourses();
        }
    }

    public void dropStudentFromCourse(String studentId, String courseCode) {
        Student student = getStudentById(studentId);
        Course course = getCourseByCode(courseCode);

        if (student == null) {
            System.out.println("Error: Student with ID " + studentId + " not found.");

            return;
        }
        if (course == null) {
            System.out.println("Error: Course with code " + courseCode + " not found.");
            return;
        }

        student.dropCourse(course);
        if (!course.getEnrolledStudents().contains(student)) {
            saveStudents();
            saveCourses();
        }
    }

    public void closeCourse(String courseCode) {
        Course course = getCourseByCode(courseCode);
        if (course == null) {
            System.out.println("Error: Course with code " + courseCode + " not found.");
            return;
        }

        if (course.getEnrolledStudents().size() >= course.getCapacity()) {
            System.out.println(course.getCourseName() + " is at full capacity.");
            course.setEnrollmentStatus(Course.EnrollmentStatusEnum.Closed);
        } else if (course.getEnrollmentStatus() == Course.EnrollmentStatusEnum.Closed) {
            System.out.println(course.getCourseName() + " enrollment status is already closed.");
        } else {
            System.out.println(course.getCourseName() + " still has available capacity.");
            course.setEnrollmentStatus(Course.EnrollmentStatusEnum.Closed);
        }
        saveCourses();
    }
    public void viewEnrollmentStatistics() {
        int totalEnrolled = 0;
        boolean openCoursesExist = false;

        System.out.println("\n---------Enrollment Statistics---------");

        for (Course course : courses) {
            int count = course.getEnrolledStudents() != null ? course.getEnrolledStudents().size() : 0;
            totalEnrolled += count;
            System.out.printf("Course: %s (%s) - Enrolled: %d%n", course.getCourseName(), course.getCourseCode(),
                    count);
            if (course.getEnrollmentStatus() == Course.EnrollmentStatusEnum.Open) {
                openCoursesExist = true;
            }
        }
        System.out.println("Total enrolled students across all courses: " + totalEnrolled);
        System.out.println("Open courses available: " + (openCoursesExist ? "Yes" : "No"));
    }

    public void generateReports() {
        System.out.println("\n---------Enrollment Report---------");

        Course mostPopular = null;
        int maxEnrolled = 0;

        for (Course course : courses) {
            int enrolled = course.getEnrolledStudents() != null ? course.getEnrolledStudents().size() : 0;
            if (enrolled > maxEnrolled) {
                mostPopular = course;
                maxEnrolled = enrolled;
            }
        }
        if (mostPopular != null) {
            System.out.printf("Most popular course: %s (%s) - Enrolled: %d.%n", mostPopular.getCourseName(),
                    mostPopular.getCourseCode(), maxEnrolled);
        } else {
            System.out.println("No enrollments found.");
        }
    }
}
