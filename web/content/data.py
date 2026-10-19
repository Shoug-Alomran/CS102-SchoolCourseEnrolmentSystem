"""Sample data, file schemas, validation rules and exception handling.

SAMPLE is fictional demo data. It is written into the pages as example file
contents and also shipped to the browser for the interactive console, so the
console, the data-file viewer and the report examples always agree.
Field order matches dataManager's load/save methods.
"""

DEFAULT_ADMIN = {
    "name": "Shoug", "id": "1122334455", "password": "Default12345",
    "email": "S.Alomran@gmail.com", "phone": "0531110904", "address": "Qirawan district",
}

SAMPLE = {
    "students": [
        {"name": "Sara Khalid", "id": "2200000001", "password": "Student1234", "email": "sara.k@uni.example",
         "phone": "0500000101", "address": "North Residence", "creditLimit": 15, "courses": ["CS102", "MATH201"]},
        {"name": "Noura Saleh", "id": "2200000002", "password": "Noura12345", "email": "noura.s@uni.example",
         "phone": "0500000102", "address": "West Campus", "creditLimit": 12, "courses": ["CS102", "PHYS101"]},
        {"name": "Faisal Omar", "id": "2200000003", "password": "Faisal1234", "email": "faisal.o@uni.example",
         "phone": "0500000103", "address": "East Gate", "creditLimit": 18, "courses": ["ENG101", "PHYS101"]},
    ],
    "instructors": [
        {"name": "Lina Haddad", "id": "4000000001", "password": "Teacher1234", "email": "lina.h@uni.example",
         "phone": "0500000201", "address": "Faculty Block A"},
        {"name": "Omar Faris", "id": "4000000002", "password": "Teacher5678", "email": "omar.f@uni.example",
         "phone": "0500000202", "address": "Faculty Block B"},
    ],
    "administrators": [
        {"name": "Registrar Office", "id": "1000000001", "password": "Registrar2026", "email": "registrar@uni.example",
         "phone": "0500000301", "address": "Admin Building"},
    ],
    "courses": [
        {"name": "Programming II", "code": "CS102", "schedule": "Sun/Tue 10:00", "description": "Object-oriented programming in Java",
         "status": "Open", "instructor": "4000000001", "capacity": 30, "creditHours": 3, "students": ["2200000001", "2200000002"]},
        {"name": "Discrete Mathematics", "code": "MATH201", "schedule": "Mon/Wed 12:00", "description": "Logic, sets and proofs",
         "status": "Open", "instructor": "4000000002", "capacity": 25, "creditHours": 3, "students": ["2200000001"]},
        {"name": "Data Structures", "code": "CS210", "schedule": "Sun/Tue 13:00", "description": "Lists, trees and graphs",
         "status": "Open", "instructor": "4000000001", "capacity": 20, "creditHours": 4, "students": []},
        {"name": "Technical Writing", "code": "ENG101", "schedule": "Thu 09:00", "description": "Reports, memos and presentations",
         "status": "Closed", "instructor": "4000000002", "capacity": 20, "creditHours": 2, "students": ["2200000003"]},
        {"name": "Physics I", "code": "PHYS101", "schedule": "Mon/Wed 08:00", "description": "",
         "status": "Open", "instructor": "", "capacity": 2, "creditHours": 4, "students": ["2200000002", "2200000003"]},
    ],
    "assessments": [
        {"student": "2200000001", "course": "CS102", "type": "Quiz_1", "score": 88.0},
        {"student": "2200000001", "course": "CS102", "type": "Midterm_1", "score": 91.5},
        {"student": "2200000002", "course": "CS102", "type": "Quiz_1", "score": 76.0},
        {"student": "2200000001", "course": "MATH201", "type": "Quiz_1", "score": 69.0},
        {"student": "2200000003", "course": "ENG101", "type": "Project", "score": 94.0},
    ],
}

EXAM_TYPES = ["Quiz_1", "Quiz_2", "Quiz_3", "Quiz_4", "Midterm_1", "Midterm_2", "Final", "Project"]


def java_double(x):
    """String.valueOf(double) for the values we use."""
    return repr(float(x))


def lines_for(file_key):
    """Serialise SAMPLE the way dataManager's save methods do."""
    s = SAMPLE
    if file_key == "students":
        return ["|".join([r["name"], r["id"], r["password"], r["email"], r["phone"], r["address"],
                          str(r["creditLimit"]), ",".join(r["courses"])]) for r in s["students"]]
    if file_key in ("instructors", "administrators"):
        return ["|".join([r["name"], r["id"], r["password"], r["email"], r["phone"], r["address"]])
                for r in s[file_key]]
    if file_key == "courses":
        return ["|".join([r["name"], r["code"], r["schedule"], r["description"], r["status"], r["instructor"],
                          str(r["capacity"]), str(r["creditHours"]), ",".join(r["students"])]) for r in s["courses"]]
    if file_key == "assessments":
        return ["|".join([r["student"], r["course"], r["type"], java_double(r["score"]), r["type"]])
                for r in s["assessments"]]
    raise KeyError(file_key)


# Columns: (field, Java type, how the loader reads it)
FILES = [
    {
        "key": "students", "name": "students.txt", "cls": "student", "entity": "Student",
        "loader": "loadStudents", "saver": "saveStudents", "min": 7,
        "blurb": "One student per line. The last column lists enrolled course codes.",
        "columns": [
            ("name", "String", "parts[0]"),
            ("id", "String", "parts[1], must be unique"),
            ("password", "String", "parts[2], stored as plain text"),
            ("email", "String", "parts[3]"),
            ("phoneNumber", "String", "parts[4]"),
            ("address", "String", "parts[5]"),
            ("creditLimit", "int", "Integer.parseInt(parts[6])"),
            ("enrolledCourses", "List<Course>", "parts[7] split on commas → getCourseByCode()"),
        ],
        "refs": [("enrolledCourses", "courses", "code")],
    },
    {
        "key": "instructors", "name": "instructors.txt", "cls": "instructor", "entity": "Instructor",
        "loader": "loadInstructors", "saver": "saveInstructors", "min": 6,
        "blurb": "Profile fields only. Courses point at instructors, not the other way round.",
        "columns": [
            ("name", "String", "parts[0]"),
            ("id", "String", "parts[1], must be unique"),
            ("password", "String", "parts[2]"),
            ("email", "String", "parts[3]"),
            ("phoneNumber", "String", "parts[4]"),
            ("address", "String", "parts[5]"),
        ],
        "refs": [],
    },
    {
        "key": "administrators", "name": "administrators.txt", "cls": "administrator", "entity": "Administrator",
        "loader": "loadAdministrators", "saver": "saveAdministrators", "min": 6,
        "blurb": "Same layout as instructors. The default admin is added at start-up if its ID is not already here.",
        "columns": [
            ("name", "String", "parts[0]"),
            ("id", "String", "parts[1], must be unique"),
            ("password", "String", "parts[2]"),
            ("email", "String", "parts[3]"),
            ("phoneNumber", "String", "parts[4]"),
            ("address", "String", "parts[5]"),
        ],
        "refs": [],
    },
    {
        "key": "courses", "name": "courses.txt", "cls": "course", "entity": "Course",
        "loader": "loadCourses", "saver": "saveCourses", "min": 8,
        "blurb": "Empty schedule, description or instructor columns load as null.",
        "columns": [
            ("courseName", "String", "parts[0]"),
            ("courseCode", "String", "parts[1], must be unique"),
            ("schedule", "String", "parts[2], empty → null"),
            ("description", "String", "parts[3], empty → null"),
            ("enrollmentStatus", "EnrollmentStatusEnum", "valueOf(parts[4]): Open or Closed"),
            ("instructor", "Instructor", "parts[5] → getInstructorById(), empty → null"),
            ("capacity", "int", "Integer.parseInt(parts[6])"),
            ("creditHours", "int", "Integer.parseInt(parts[7])"),
            ("enrolledStudents", "List<Student>", "parts[8] split on commas → getStudentById()"),
        ],
        "refs": [("instructor", "instructors", "id"), ("enrolledStudents", "students", "id")],
    },
    {
        "key": "assessments", "name": "assessments.txt", "cls": "assessment", "entity": "Assessment",
        "loader": "loadAssessments", "saver": "saveAssessments", "min": 5,
        "blurb": "One grade per line, keyed by student, course and exam type.",
        "columns": [
            ("studentId", "String", "parts[0]"),
            ("courseCode", "String", "parts[1]"),
            ("examType", "ExamType", "valueOf(parts[2])"),
            ("score", "double", "Double.parseDouble(parts[3])"),
            ("assessmentName", "String", "parts[4], the exam type's name when graded in the app"),
        ],
        "refs": [("studentId", "students", "id"), ("courseCode", "courses", "code")],
    },
]

# Where each change is written. "exit" means only saveAllData() at exit.
PERSISTENCE = [
    ("Start-up", "Register the default admin", "administrators.txt", "now"),
    ("Student", "7 · Update personal information", "students.txt", "now"),
    ("Instructor", "3 · Update course information", "courses.txt", "now"),
    ("Instructor", "4 · Update personal information", "instructors.txt", "now"),
    ("Admin", "9 · Update Student Info", "students.txt", "now"),
    ("Admin", "10 · Update Instructor Info", "instructors.txt", "now"),
    ("Student", "2 · Enroll / 5 · Drop", "students.txt", "exit"),
    ("Instructor", "2 · Grade assignments", "assessments.txt", "exit"),
    ("Admin", "1, 2 · Add / remove students", "students.txt", "exit"),
    ("Admin", "4, 5 · Add / remove instructors", "instructors.txt", "exit"),
    ("Admin", "7, 8, 11 · Add / close course, assign instructor", "courses.txt", "exit"),
    ("Exit", "Type exit at the role prompt", "all five files", "now"),
]

VALIDATORS = [
    {"method": "ValidateName", "rule": "length() > 3", "ok": "Lina Haddad", "bad": "Bo",
     "used": "Adding students and instructors, admin profile updates",
     "message": "Invalid name. Please enter a valid name."},
    {"method": "ValidatePassword", "rule": "length() > 8", "ok": "Student1234", "bad": "secret12",
     "used": "Creating accounts and every profile update",
     "message": "Invalid password. Please try again."},
    {"method": "ValidateEmail", "rule": "contains(\"@\") && contains(\".\")", "ok": "sara.k@uni.example", "bad": "sara-at-uni",
     "used": "Creating accounts and every profile update",
     "message": "Invalid email. Please try again."},
    {"method": "ValidatePhoneNumber", "rule": "length() == 10", "ok": "0500000101", "bad": "05000001",
     "used": "Creating accounts and every profile update",
     "message": "Invalid phone number. Please try again."},
    {"method": "ValidateAddress", "rule": "length() > 3", "ok": "East Gate", "bad": "N/A",
     "used": "Creating accounts and every profile update",
     "message": "Invalid address. Please try again."},
]

GUARDS = [
    ("Course.setCourseName", "Not null or empty", "Course name cannot be null or empty."),
    ("Course.setCourseCode", "Not null or empty", "Course code cannot be null or empty."),
    ("Course.setCapacity", "Greater than 0", "Error: Capacity must be > 0."),
    ("Course.setCreditHours", "Greater than 0", "Credit hours can not be <= 0"),
    ("Student.setCreditLimit", "Not negative", "Must be greater than 0"),
    ("Helpers.getSafeIntInput", "An integer was typed", "Invalid input. Please enter a number."),
    ("Helpers.checkValidityOfRole", "1, 2 or 3", "Invalid selection. Please enter 1, 2, or 3."),
    ("Instructor.gradeStudent", "Score 0–100", "Score must be between 0 and 100."),
    ("Helpers.validatePasswordWithRetries", "At most 3 attempts", "Too many failed attempts. Returning to main menu."),
    ("main() menu switches", "A listed option", "Invalid option."),
    ("main() role prompt", "student, instructor, admin or exit", "Invalid role. Try again."),
]

EXCEPTIONS = [
    ("main()", "Exception, around the whole loop", "Prints “Error: <message>” and the program ends without saving."),
    ("load* methods", "FileNotFoundException", "“<Type> file not found. Starting with empty <type> list.”"),
    ("load* methods", "IOException", "“Error reading <type> file: <message>”"),
    ("loadStudents", "NumberFormatException", "“Error parsing student data: <message>”"),
    ("loadCourses, loadAssessments", "IllegalArgumentException (bad enum or number)", "“Error parsing course/assessment data: <message>”"),
    ("save* methods", "IOException", "“Error writing <type> file: <message>”"),
    ("Helpers.getSafeIntInput", "Any exception from nextInt()", "Clears the line and asks again."),
    ("Helpers flows (enrol, drop, add, update…)", "Exception", "Prints the exception's message and returns to the menu."),
    ("Instructor.gradeStudent", "InputMismatchException for the score", "“Invalid input. Please enter a number.” and asks again."),
]
