---
title: School Course Enrolment System
template: home.html
hide:
  - navigation
  - toc
---

<section class="ce-section" markdown>
<p class="ce-kicker">// abstract</p>

## Three roles, one `User`

<p class="ce-section__lede">The School Enrollment System is a Java console application that simulates a simplified university course management environment. Each role signs in with an ID and password, then works through its own menu against a shared set of courses and assessments.</p>

<div class="ce-roles">
  <a class="ce-id ce-id--student" href="student-workflow/">
    <span class="ce-id__band"><span>Student card</span><span>CS102</span></span>
    <span class="ce-id__body">
      <span class="ce-id__photo">S</span>
      <span>
        <span class="ce-id__name">Student</span>
        <span class="ce-id__sig"><b>extends</b> User</span>
      </span>
    </span>
    <ul>
      <li>Browse and enrol in open courses</li>
      <li>View and drop enrolled courses</li>
      <li>Check grades per assessment</li>
      <li>Update personal information</li>
    </ul>
    <span class="ce-id__foot"><span>7 menu options</span><span>Workflow →</span></span>
  </a>
  <a class="ce-id ce-id--instructor" href="instructor-workflow/">
    <span class="ce-id__band"><span>Faculty card</span><span>CS102</span></span>
    <span class="ce-id__body">
      <span class="ce-id__photo">I</span>
      <span>
        <span class="ce-id__name">Instructor</span>
        <span class="ce-id__sig"><b>extends</b> User</span>
      </span>
    </span>
    <ul>
      <li>View students enrolled in a course</li>
      <li>Grade quizzes, midterms, homework, finals</li>
      <li>Update course information</li>
    </ul>
    <span class="ce-id__foot"><span>4 menu options</span><span>Workflow →</span></span>
  </a>
  <a class="ce-id ce-id--admin" href="admin-workflow/">
    <span class="ce-id__band"><span>Staff card</span><span>CS102</span></span>
    <span class="ce-id__body">
      <span class="ce-id__photo">A</span>
      <span>
        <span class="ce-id__name">Administrator</span>
        <span class="ce-id__sig"><b>extends</b> User</span>
      </span>
    </span>
    <ul>
      <li>Add or remove students and instructors</li>
      <li>Create courses and assign instructors</li>
      <li>Update user records</li>
      <li>Open or close courses</li>
    </ul>
    <span class="ce-id__foot"><span>8 menu options</span><span>Workflow →</span></span>
  </a>
</div>
</section>

<section class="ce-section" markdown>
<p class="ce-kicker">// system architecture</p>

## The class map

<p class="ce-section__lede">Core entities model the people and data, a singleton <code>dataManager</code> owns persistence, <code>Helpers</code> holds the shared input and menu logic, and <code>SchoolCourseEnrolmentSystem</code> drives the main role-selection loop.</p>

<div class="ce-uml" role="img" aria-label="Class diagram: Student, Instructor and Administrator extend the abstract User class. Supporting classes are Course, ExamType, dataManager, Helpers and the main SchoolCourseEnrolmentSystem class.">
  <div class="ce-uml__tier">
    <a class="ce-class ce-class--abstract" href="user/">
      <span class="ce-class__name"><i>«abstract»</i>User</span>
      <span class="ce-class__members">− id, password<br />− email, phoneNumber<br />+ <i>login()</i> · <i>logout()</i></span>
    </a>
  </div>
  <div class="ce-uml__link" aria-hidden="true"><span class="ce-uml__arrow"></span></div>
  <div class="ce-uml__tier">
    <a class="ce-class" href="student/">
      <span class="ce-class__name">Student</span>
      <span class="ce-class__members">+ enroll_In_Course()<br />+ dropCourse()</span>
    </a>
    <a class="ce-class" href="instructor/">
      <span class="ce-class__name">Instructor</span>
      <span class="ce-class__members">+ viewEnrolledStudents()<br />+ gradeAssignments()</span>
    </a>
    <a class="ce-class" href="administrator/">
      <span class="ce-class__name">Administrator</span>
      <span class="ce-class__members">+ addCourse()<br />+ closeCourse()</span>
    </a>
  </div>
  <div class="ce-uml__support">
    <span class="ce-uml__legend">course data · persistence · application flow</span>
    <div class="ce-uml__tier">
      <a class="ce-class" href="course/">
        <span class="ce-class__name">Course</span>
        <span class="ce-class__members">capacity · enrollmentStatus</span>
      </a>
      <a class="ce-class" href="assessment/">
        <span class="ce-class__name"><i>«assessment»</i>ExamType</span>
        <span class="ce-class__members">examType · grades</span>
      </a>
      <a class="ce-class" href="data-manager/">
        <span class="ce-class__name"><i>«singleton»</i>dataManager</span>
        <span class="ce-class__members">load · save · CRUD</span>
      </a>
      <a class="ce-class" href="helpers/">
        <span class="ce-class__name">Helpers</span>
        <span class="ce-class__members">input · menus</span>
      </a>
      <a class="ce-class" href="main/">
        <span class="ce-class__name"><i>«main»</i>SchoolCourseEnrolmentSystem</span>
        <span class="ce-class__members">role selection loop</span>
      </a>
    </div>
  </div>
</div>
</section>

<section class="ce-section" markdown>
<p class="ce-kicker">// how to use this documentation</p>

## Course catalogue

<p class="ce-section__lede">The documentation is organised like a semester timetable. Pick a module to enrol in, or use search (<kbd>/</kbd>) to jump straight to a class or method.</p>

<div class="ce-catalog">
  <div class="ce-catalog__head"><span>Code</span><span>Module</span><span>Pages</span><span></span></div>
  <a class="ce-catalog__row" href="structure/">
    <span class="ce-catalog__code">CS102-100</span>
    <span><span class="ce-catalog__title">Project Structure</span><span class="ce-catalog__desc">High-level breakdown of files, data, menus, validation and responsibilities.</span></span>
    <span class="ce-catalog__cr">9 pp.</span>
    <span class="ce-catalog__cta">Enrol →</span>
  </a>
  <a class="ce-catalog__row" href="user/">
    <span class="ce-catalog__code">CS102-200</span>
    <span><span class="ce-catalog__title">Core Classes</span><span class="ce-catalog__desc">User, Student, Instructor, Administrator, Course and Assessment in detail.</span></span>
    <span class="ce-catalog__cr">6 pp.</span>
    <span class="ce-catalog__cta">Enrol →</span>
  </a>
  <a class="ce-catalog__row" href="student-workflow/">
    <span class="ce-catalog__code">CS102-300</span>
    <span><span class="ce-catalog__title">Workflows</span><span class="ce-catalog__desc">Step-by-step student, instructor and administrator operations, plus exit and exception handling.</span></span>
    <span class="ce-catalog__cr">4 pp.</span>
    <span class="ce-catalog__cta">Enrol →</span>
  </a>
  <a class="ce-catalog__row" href="code-main/">
    <span class="ce-catalog__code">CS102-400</span>
    <span><span class="ce-catalog__title">Code Reference</span><span class="ce-catalog__desc">Annotated listings for the main, helpers and data manager classes, and the full source code.</span></span>
    <span class="ce-catalog__cr">13 pp.</span>
    <span class="ce-catalog__cta">Enrol →</span>
  </a>
  <a class="ce-catalog__row" href="reports-and-statistics/">
    <span class="ce-catalog__code">CS102-500</span>
    <span><span class="ce-catalog__title">Reports &amp; Statistics</span><span class="ce-catalog__desc">How enrolment statistics and reports are generated.</span></span>
    <span class="ce-catalog__cr">1 p.</span>
    <span class="ce-catalog__cta">Enrol →</span>
  </a>
  <a class="ce-catalog__row" href="project-report/">
    <span class="ce-catalog__code">CS102-600</span>
    <span><span class="ce-catalog__title">Project Report</span><span class="ce-catalog__desc">The full submitted report as a PDF, to read online or download.</span></span>
    <span class="ce-catalog__cr">PDF</span>
    <span class="ce-catalog__cta">Enrol →</span>
  </a>
</div>
</section>

<section class="ce-section" markdown>
<p class="ce-kicker">// project goals</p>

## What it set out to do

<ul class="ce-goals">
  <li>Simulate a basic university course enrolment system</li>
  <li>Implement role-based access and workflows</li>
  <li>Apply object-oriented design principles</li>
  <li>Use file-based persistence for storing system data</li>
  <li>Keep entities, helpers, data management and application flow clearly separated</li>
</ul>
</section>

<section class="ce-section" markdown>
<p class="ce-kicker">// persistence &amp; authorship</p>

## On file

<div class="ce-split">
  <div class="ce-panel">
    <h3>Plain-text data files</h3>
    <p>The <code>dataManager</code> class translates between these files and in-memory objects. Data is loaded at start-up and saved before the program exits.</p>
    <ul class="ce-files">
      <li>students.txt</li>
      <li>instructors.txt</li>
      <li>administrators.txt</li>
      <li>courses.txt</li>
      <li>assessments.txt</li>
    </ul>
  </div>
  <div class="ce-panel">
    <h3>Student record</h3>
    <p>Submitted as the CS102 course project.</p>
<dl class="ce-record">
<div><dt>Author</dt><dd>Shoug Alomran</dd></div>
<div><dt>Email</dt><dd><a href="mailto:2234103192@psu.edu.sa">2234103192@psu.edu.sa</a></dd></div>
<div><dt>Course</dt><dd>CS102 — Programming II</dd></div>
<div><dt>Institution</dt><dd>Prince Sultan University</dd></div>
</dl>
  </div>
</div>
</section>
