---
title: "Assessment Class - Java Source Code"
description: "Full Java source of the Assessment class and ExamType enum: assigning grades, viewing course grades, averages and exam scores."
---

# Assessment Class - Source Code

Full Java source of the Assessment class and ExamType enum: assigning grades, viewing course grades, averages and exam scores.

For an explanation of how this class works, see the [Assessment class guide](../assessment.md). This listing comes from the [CS102 project report](../project-report.md).

```java title="Assessment.java" linenums="1"
package schoolcourseenrolmentsystem;

import java.util.*;

public class Assessment {
    // Defines the types of exams/assessments available (quizzes, midterms, final
    // exam, project).
    public enum ExamType {
        Quiz_1, Quiz_2, Quiz_3, Quiz_4, Midterm_1, Midterm_2, Final, Project

    }

    // Attributes
    private String studentId;
    private String courseCode;
    private ExamType examType;
    private double score;
    private String assessmentName;

    // Constructor
    public Assessment(String studentId, String courseCode, ExamType examType, double score, String
            assessmentName) {
        setStudentId(studentId);
        setCourseCode(courseCode);
        setExamType(examType);
        setScore(score);
        setAssessmentName(assessmentName);
    }
    //======================= Setters and Getters =======================
    public String getStudentId() {
        return studentId;
    }

    public void setStudentId(String studentId) {

        this.studentId = studentId;
    }

    public String getCourseCode() {
        return courseCode;
    }

    public void setCourseCode(String courseCode) {
        this.courseCode = courseCode;
    }

    public ExamType getExamType() {
        return examType;
    }

    public void setExamType(ExamType examType) {
        this.examType = examType;
    }

    public double getScore() {
        return score;
    }

    public void setScore(double score) {
        this.score = score;
    }

    public String getAssessmentName() {
        return assessmentName;
    }

    public void setAssessmentName(String assessmentName) {
        this.assessmentName = assessmentName;
    }

    //======================= Methods=======================

    public void assignGrade(List<Assessment> listOfGrades, String studentId, String courseCode,
            Assessment.ExamType examType, double score) {
        boolean gradeUpdated = false;

        for (Assessment grade : listOfGrades) {
            if (grade.getCourseCode().equals(courseCode)
                    && grade.getStudentId().equals(studentId)
                    && grade.getExamType() == examType) {
                grade.setScore(score); // Update existing score
                System.out.println("Grade updated successfully.");
                gradeUpdated = true;
                break;
            }
        }
        if (!gradeUpdated) {
            Assessment newGrade = new Assessment(studentId, courseCode, examType, score, examType.name());
            listOfGrades.add(newGrade);
            System.out.println("Grade recorded successfully.");
        }
    }

    public void viewAllGradesForCourse(List<Assessment> listOfGrades, Student student) {
        List<Course> courses = student.getEnrolledCoursesList();
        if (courses.isEmpty()) {
            System.out.println("You are not enrolled in any courses.");
            return;
        }
        System.out.println("Select a course to view all your grades:");
        for (int i = 0; i < courses.size(); i++) {
            System.out.printf((i + 1) + ".%s (%s).", courses.get(i).getCourseName(), courses.get(i).getCourseCode());
        }
        int courseChoice = Helpers.getSafeIntInput("Option: ");
        if (courseChoice < 1 || courseChoice > courses.size()) { //Option can't be less than 1 or more than listed courses.
            System.out.println("Invalid course selection.");
            return;
        }
        String courseCode = courses.get(courseChoice - 1).getCourseCode();

        boolean found = false;

        for (Assessment grade : listOfGrades) {
            if (grade.getStudentId().equals(student.getId()) && grade.getCourseCode().equals(courseCode)) {
                System.out.println(grade.getExamType() + ": " + grade.getScore());
                found = true;
            }
        }
        if (!found) {
            System.out.println("No grades found for this course.");
        }
    }

    public void viewTotalAverageGrade(List<Assessment> listOfGrades, String studentId, String courseCode) {
        double total = 0;
        int count = 0;

        for (Assessment grade : listOfGrades) {
            if (grade.getStudentId().equals(studentId) && grade.getCourseCode().equals(courseCode)) {
                total += grade.getScore();
                count++;
            }
        }
        if (count > 0) {
            double average = total / count;
            System.out.println("Your total average grade in " + courseCode + " is: " + average);
        } else {
            System.out.println("No grades found for this course.");
        }
    }

    public void viewSpecificExamScore(List<Assessment> listOfGrades, Student student) {
        List<Course> listOfCourses = student.getEnrolledCoursesList();
        if (listOfCourses.isEmpty()) {
            System.out.println("You are not enrolled in any courses.");
            return;
        }

        System.out.println("Select a course: ");
        for (int i = 0; i < listOfCourses.size(); i++) {
            System.out.printf((i + 1) + ".%s (%s).\n", listOfCourses.get(i).getCourseName(),
                    listOfCourses.get(i).getCourseCode());
        }
        int courseChoice = Helpers.getSafeIntInput("Choice: ");
        if (courseChoice < 1 || courseChoice > listOfCourses.size()) {
            System.out.println("Invalid selection.");
            return;
        }

        String courseCode = listOfCourses.get(courseChoice - 1).getCourseCode();

        // Choose exam type
        Assessment.ExamType[] types = Assessment.ExamType.values();
        System.out.println("Select an exam to view:");
        for (int i = 0; i < types.length; i++) {
            System.out.println((i + 1) + ". " + types[i]);
        }

        int examChoice = Helpers.getSafeIntInput("Choice: ");
        if (examChoice < 1 || examChoice > types.length) {
            System.out.println("Invalid exam type.");
            return;
        }

        Assessment.ExamType selected = types[examChoice - 1];
        boolean found = false;
        for (Assessment assessment : listOfGrades) {
            if (assessment.getStudentId().equals(student.getId()) &&
                    assessment.getCourseCode().equals(courseCode) &&
                    assessment.getExamType() == selected) {
                System.out.println("Your " + selected + " score: " + assessment.getScore());
                found = true;
            }
        }

        if (!found) {
            System.out.println("No " + selected + " score found for this course.");
        }
    }
}
```
