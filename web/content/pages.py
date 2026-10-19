"""Prose and tables for the non-class pages."""

SITE = {
    "title": "School Course Enrolment System",
    "short": "enrolment",
    "course": "CS102",
    "course_name": "Programming II",
    "institution": "Prince Sultan University",
    "author": "Shoug Alomran",
    "author_full": "Shoug Fawaz Alomran",
    "email": "2234103192@psu.edu.sa",
    "url": "https://school-course-enrolment-system.shoug-tech.com/",
    "repo": "https://github.com/Shoug-Alomran/CS102-SchoolCourseEnrolmentSystem",
    "main_site": "https://shoug-tech.com/",
    "blueprint": "https://blueprint.shoug-tech.com/",
    "pdf": "files/cs102-school-course-enrolment-system-project-report.pdf",
    "description": "CS102 School Course Enrolment System: a Java console app for students, instructors and administrators. Explore every class, each role's menu, the text-file data model, and run the program in your browser.",
}

# Known issues. source: "report" = listed in the project report,
# "listing" = observed when reading the report's source listings.
ISSUES = [
    {"id": "credit-limit-first-student", "kind": "bug", "source": "listing",
     "title": "View credit limit shows the first student, not you",
     "where": ("student", "viewCreditLimit"),
     "body": "The method loops over the whole student list and breaks after the first iteration, so it always prints the first student's limit and remaining hours.",
     "fix": "Use this.getCreditLimit() and this.enrolledInHours() instead of looping."},
    {"id": "drop-keeps-seat", "kind": "bug", "source": "listing",
     "title": "Dropping a course does not free the seat",
     "where": ("student", "dropCourse"),
     "body": "dropCourse removes the course from the student's list but never removes the student from the course's enrolledStudents. The roster, isFull() and the statistics still count the student.",
     "fix": "Also call course.getEnrolledStudents().remove(this)."},
    {"id": "load-order", "kind": "bug", "source": "listing",
     "title": "Saved enrolments are lost when students load",
     "where": ("data-manager", "loadAllData"),
     "body": "loadStudents runs before loadCourses, so getCourseByCode finds nothing and every student starts with no enrolled courses. Course rosters still list them, and enrolling again adds a duplicate roster entry.",
     "fix": "Load courses first, then resolve student course codes in a second pass."},
    {"id": "save-on-exit", "kind": "design", "source": "listing",
     "title": "Most changes are only written on exit",
     "where": ("main", "main"),
     "body": "Enrolments, drops, grades, new or removed accounts, new or closed courses and instructor assignments stay in memory until someone types exit. Closing the window or an unexpected error loses them.",
     "fix": "Use the dataManager methods that already save (enrollStudentInCourse, closeCourse…) or save after each change."},
    {"id": "close-open-course", "kind": "bug", "source": "listing",
     "title": "An open course with space cannot be closed",
     "where": ("administrator", "closeCourse"),
     "body": "Administrator.closeCourse only closes full courses. For an open course that still has space, the “still has available capacity” branch can never be reached, so nothing is printed and the course stays open.",
     "fix": "Add an else branch that sets the status to Closed."},
    {"id": "add-course-unknown-instructor", "kind": "bug", "source": "listing",
     "title": "Unknown instructor ID aborts course creation",
     "where": ("helpers", "addCourse"),
     "body": "If the ID does not match anyone, assignInstructor is called with null and calls getName() on it. The NullPointerException is caught, the message (null in Java 8) is printed, and the course is never added.",
     "fix": "Check selectedInstructor before calling assignInstructor."},
    {"id": "remove-student-invalid", "kind": "quirk", "source": "listing",
     "title": "Removing a student always ends with “Invalid option.”",
     "where": ("helpers", "removeStudent"),
     "body": "The println sits after the try/catch instead of inside the catch, so it runs every time.",
     "fix": "Move it into the catch block."},
    {"id": "logout-silent", "kind": "quirk", "source": "listing",
     "title": "Logout messages are never shown",
     "where": ("main", "main"),
     "body": "Each logout() returns a string such as “Student Sara Khalid logged out.”, but main() ignores the return value.",
     "fix": "Print the returned message."},
    {"id": "admin-login-loop", "kind": "quirk", "source": "report",
     "title": "Admin login prints “No admin record” inside the loop",
     "where": ("administrator", "login"),
     "body": "The failure message prints once for every administrator checked before the match, so a successful login can still show it.",
     "fix": "Print it once, after the loop."},
    {"id": "instructor-unused-param", "kind": "design", "source": "report",
     "title": "Instructor constructor ignores enrolledStudents",
     "where": ("instructor", None),
     "body": "The constructor takes a List<Student> but never uses it. This may be intentional or an oversight.",
     "fix": "Remove the parameter."},
    {"id": "validation-outside-setters", "kind": "design", "source": "report",
     "title": "User setters do not validate",
     "where": ("user", None),
     "body": "Input is checked by the Helpers validators before setters are called, which keeps User small but means code that calls a setter directly can store anything.",
     "fix": None},
    {"id": "stats-format", "kind": "quirk", "source": "listing",
     "title": "Helpers.viewEnrollmentStatistics would throw",
     "where": ("helpers", "viewEnrollmentStatistics"),
     "body": "Its printf has three placeholders but two arguments, which throws MissingFormatArgumentException. main() calls the dataManager version instead, so it never runs.",
     "fix": "Pass the course code, or delete the unused copy."},
    {"id": "double-message", "kind": "quirk", "source": "listing",
     "title": "Instructor profile update prints its message twice",
     "where": ("helpers", "updateInstructorProfile"),
     "body": "Both Instructor.updateInstructorPersonalInfo and the helper print “Instructor <name>'s information updated.”",
     "fix": None},
    {"id": "second-scanner", "kind": "design", "source": "listing",
     "title": "gradeStudent opens its own Scanner",
     "where": ("instructor", "gradeStudent"),
     "body": "It creates new Scanner(System.in) for the score, while the rest of the program shares Helpers.input. Two Scanners on one stream can swallow buffered input.",
     "fix": "Use Helpers.input or Helpers.getSafeIntInput."},
]

IMPROVEMENTS = [
    "Consolidate repetitive console input and output logic.",
    "Validate phone numbers with a regular expression (digits only, not just 10 characters).",
    "Avoid printing “not found” messages repeatedly inside loops.",
    "Separate input and output from business logic so the classes can be tested.",
]

DESIGN = [
    {"title": "Singleton storage", "code": "dataManager.getInstance()", "cls": "data-manager",
     "body": "One synchronized factory method means every part of the program shares the same five lists."},
    {"title": "Self-typed generics", "code": "User<T> / <T extends User<T>> T login(...)", "cls": "user",
     "body": "Each subclass passes itself as T, so one login flow in Helpers returns a Student, Instructor or Administrator with no casts."},
    {"title": "Predicate validators", "code": "updateFieldWithPrompt(\"email\", value, Helpers::ValidateEmail)", "cls": "helpers",
     "body": "Validators are passed as method references, so one prompt method handles every field."},
    {"title": "Enums for fixed choices", "code": "Role · EnrollmentStatusEnum · ExamType", "cls": "course",
     "body": "Roles, Open/Closed and exam types can only take valid values, and valueOf() parses them from the files."},
    {"title": "Safe removal", "code": "Iterator<Student> it = list.iterator(); it.remove();", "cls": "administrator",
     "body": "Removing through an Iterator avoids a ConcurrentModificationException while looping."},
    {"title": "Plain-text persistence", "code": "String.join(\"|\", ...) / line.split(\"\\\\|\")", "cls": "data-manager",
     "body": "Human-readable files with no database dependency, at the cost of indexing, concurrency and integrity checks."},
]

STARTUP = [
    ("dataManager.getInstance()", "Creates the five empty lists", "Testing Constructor"),
    ("loadAllData()", "Reads the five files in order: students, instructors, administrators, courses, assessments", "Loading student: …"),
    ("addAdministrator(DefaultAdmin)", "Registers the built-in admin and saves administrators.txt", "Administrator added: Shoug with ID: 1122334455"),
    ("Role prompt", "Loops until exit", "Enter your role from the current options: (Student/Instructor/Admin) or exit to finish."),
    ("Helpers.login<T>()", "ID, then up to three password attempts", "Please enter your ID:"),
    ("Role menu loop", "Runs until the user picks Logout", "---------Student Menu---------"),
    ("exit", "saveAllData() writes all five files", "Goodbye."),
]

REPORT_SECTIONS = [
    ("Project structure", "3–4", "architecture/"),
    ("Helpers class", "5–8", "helpers/"),
    ("User class", "9–10", "user/"),
    ("Student class", "11–13", "student/"),
    ("Administrator class", "14–16", "administrator/"),
    ("Instructor class", "17–19", "instructor/"),
    ("Course class", "20–21", "course/"),
    ("Assessment class", "22–23", "assessment/"),
    ("Main class and workflows", "24–27", "main/"),
    ("Full source code", "28–101", "architecture/#classes"),
]

POLICIES = [
    {
        "slug": "policys/privacy-notice",
        "title": "Privacy Notice",
        "updated": "Last updated: 2026",
        "html": """
<p>Welcome to Shoug's Digital Garden. This website is a personal academic and professional documentation platform hosted using GitHub Pages and delivered through Cloudflare. This notice explains what information may be collected when you visit and how it is handled.</p>
<h2 id="hosting">Hosting &amp; infrastructure</h2>
<div class="cards two">
  <div class="card"><h3>GitHub Pages</h3><p>This website is hosted on GitHub Pages as a static site. GitHub may process technical data as part of standard hosting operations.</p></div>
  <div class="card"><h3>Cloudflare</h3><p>Content is delivered and secured via Cloudflare, which provides CDN, DNS, and security services. Cloudflare may process technical data for performance and protection.</p></div>
</div>
<h2 id="collected">Information collected automatically</h2>
<p>When you visit this site, the following technical data may be automatically processed by infrastructure providers for content delivery, security monitoring, performance optimization, and abuse prevention.</p>
<div class="table-wrap"><table class="grid">
<thead><tr><th>Data type</th><th>Examples</th></tr></thead>
<tbody>
<tr><td>Network</td><td>IP address</td></tr>
<tr><td>Browser</td><td>Type, version</td></tr>
<tr><td>Device</td><td>Device type, operating system</td></tr>
<tr><td>Navigation</td><td>Referring pages, requested URLs</td></tr>
<tr><td>Timing</td><td>Date and time of access</td></tr>
</tbody></table></div>
<p>I do not personally track individual visitors or build user profiles.</p>
<h2 id="cookies">Cookies</h2>
<p>Cloudflare may use essential cookies for security and bot protection, load balancing, and performance optimization. This website may also use local storage or cookies for language selection (English / Arabic) and theme preference (Light / Dark mode).</p>
<p>No advertising or behavioral tracking cookies are intentionally deployed.</p>
<h2 id="contact-info">Contact information</h2>
<p>If you choose to contact me directly via email or linked platforms, you voluntarily provide your name, email address, and any information included in your message. This information is used only to respond to you and is not shared for commercial purposes.</p>
<h2 id="third-party">Third-party links</h2>
<p>This website may link to external platforms such as GitHub, LinkedIn, or other websites. Those platforms operate under their own privacy policies.</p>
<h2 id="sharing">Data sharing</h2>
<p>I do not sell, rent, or trade personal information. Any technical data processed occurs through GitHub and Cloudflare as infrastructure providers only.</p>
<h2 id="security">Data security</h2>
<p>Cloudflare provides security and traffic filtering. GitHub Pages provides hosting infrastructure. While reasonable measures are taken to protect the site, no online system can guarantee absolute security.</p>
<h2 id="rights">Your rights</h2>
<p>If you have contacted me and would like your message or personal information removed, you may request deletion via email at any time.</p>
<h2 id="contact">Contact</h2>
<p>For privacy-related inquiries, please reach out directly: <a href="mailto:inquiry@shoug-tech.com">inquiry@shoug-tech.com</a></p>
""",
    },
    {
        "slug": "policys/academic-disclaimer",
        "title": "Academic Disclaimer",
        "updated": "Last updated: 2026",
        "html": """
<p>Shoug's Digital Garden is a personal academic documentation platform. The materials published here are created as part of my personal learning process and knowledge organization, intended for educational and reference purposes only.</p>
<h2 id="purpose">Purpose of this website</h2>
<p>The content in the Academics section, including notes, summaries, diagrams, quizzes, cheat sheets, and reflections, reflects my personal understanding and interpretation of course material. It may simplify, reorganize, or rephrase official material for clarity, and should not be considered a substitute for lectures, textbooks, or official course documentation.</p>
<p>While care is taken to ensure accuracy, errors or omissions may exist.</p>
<h2 id="affiliation">University affiliation</h2>
<p>This website is not formally affiliated with any academic institution. Course names and structures are referenced for documentation purposes only. All rights to official course materials remain with their respective institutions and instructors.</p>
<h2 id="ip">Intellectual property</h2>
<p>Some materials may reference standard textbooks, academic frameworks, or publicly available educational resources. Where applicable, proper attribution is provided.</p>
<p>All original notes, summaries, and structured documentation on this website are my own intellectual work unless otherwise stated.</p>
<h2 id="use">Permitted use</h2>
<div class="cards two">
  <div class="card ok"><h3>You may</h3><ul><li>Use materials for personal study</li><li>Reference concepts with proper attribution</li></ul></div>
  <div class="card no"><h3>You may not</h3><ul><li>Reproduce content commercially</li><li>Redistribute materials without appropriate credit</li><li>Present the work as official institutional documentation</li></ul></div>
</div>
<h2 id="liability">No academic liability</h2>
<p>This website does not guarantee academic outcomes, grades, or examination performance. Users are responsible for verifying information against official academic sources.</p>
<h2 id="contact">Contact</h2>
<p>If you believe any content requires correction, clarification, or attribution adjustment, please reach out directly: <a href="mailto:inquiry@shoug-tech.com">inquiry@shoug-tech.com</a></p>
""",
    },
    {
        "slug": "policys/copyright",
        "title": "Copyright & Usage Policy",
        "updated": "© 2026 Shoug Fawaz Alomran. All rights reserved.",
        "html": """
<p>All content published under this domain and its subdomains is protected by international copyright laws. This includes software projects, source code, documentation, designs, research, and written content.</p>
<h2 id="use">Permitted &amp; prohibited use</h2>
<div class="cards two">
  <div class="card ok"><h3>You may</h3><ul><li>View and reference content for personal, educational, and non-commercial purposes</li><li>Quote small portions with proper attribution</li></ul></div>
  <div class="card no"><h3>You may not</h3><ul><li>Reproduce or redistribute full projects</li><li>Use content commercially without written permission</li><li>Claim authorship of this work</li></ul></div>
</div>
<h2 id="licensing">Licensing</h2>
<p>Specific projects may include their own separate licenses. In the event of any conflict between a project-level license and this policy, the project-level license takes precedence.</p>
<h2 id="contact">Contact</h2>
<p>For permissions or licensing inquiries, please reach out directly: <a href="mailto:Shoug.Alomran@Shoug-Tech.com">Shoug.Alomran@Shoug-Tech.com</a></p>
""",
    },
]
