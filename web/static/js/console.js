/* CS102 enrolment: an in-browser port of SchoolCourseEnrolmentSystem.main().
 *
 * Each Java method used by the menus is mirrored below with the same prompts,
 * messages, load order and save points, including the quirks documented on
 * the Known issues page. Data starts from window.CE_SAMPLE (sample files).
 */
(function () {
  "use strict";

  var SAMPLE = window.CE_SAMPLE;
  if (!SAMPLE) return;
  var FILES = ["students", "instructors", "administrators", "courses", "assessments"];

  function Abort() {}
  function JavaException(message) { this.message = message === undefined ? null : message; }

  function jd(x) { return Number.isInteger(x) ? x.toFixed(1) : String(x); }
  function str(x) { return x === null || x === undefined ? "null" : String(x); }

  /* ---------------------------------------------------------------------
     Terminal widget
     --------------------------------------------------------------------- */
  function Terminal(host, opts) {
    this.host = host;
    this.opts = opts || {};
    this.gen = 0;
    this.pending = null;
    this.queue = [];
    this.build();
  }

  Terminal.prototype.build = function () {
    var self = this;
    var dock = !!this.opts.dock;
    this.host.innerHTML =
      '<div class="console">' +
      '<div class="con-bar">' +
      '<span class="con-title"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg><span>SchoolCourseEnrolmentSystem</span></span>' +
      '<div role="tablist" aria-label="Console views" style="display:flex;gap:2px">' +
      '<button type="button" class="con-tab" role="tab" aria-selected="true" data-tab="run">Console</button>' +
      '<button type="button" class="con-tab" role="tab" aria-selected="false" data-tab="files">Files</button></div>' +
      '<span class="con-grow"></span>' +
      '<button type="button" class="con-btn" data-act="reset" title="Restart the program with the sample files">↻ Rerun</button>' +
      (dock ? '<button type="button" class="con-btn" data-act="close" aria-label="Close console">×</button>' : "") +
      "</div>" +
      '<pre class="con-out" aria-live="polite" tabindex="0"></pre>' +
      '<form class="con-in" autocomplete="off"><label for="ci-' + (Terminal.n = (Terminal.n || 0) + 1) + '">&gt;</label>' +
      '<input id="ci-' + Terminal.n + '" spellcheck="false" autocapitalize="off" aria-label="Program input" disabled></form>' +
      '<div class="con-chips" aria-label="Suggested input"></div>' +
      '<div class="con-files" hidden></div>' +
      "</div>";
    this.out = this.host.querySelector(".con-out");
    var out = this.out;
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(function () { out.scrollTop = out.scrollHeight; });
    }
    this.input = this.host.querySelector("input");
    this.chips = this.host.querySelector(".con-chips");
    this.files = this.host.querySelector(".con-files");
    this.form = this.host.querySelector("form");
    this.form.addEventListener("submit", function (e) {
      e.preventDefault();
      self.submit(self.input.value);
    });
    this.chips.addEventListener("click", function (e) {
      var b = e.target.closest("[data-v]");
      if (b) self.submit(b.dataset.v);
    });
    this.host.querySelector(".con-bar").addEventListener("click", function (e) {
      var t = e.target.closest("[data-tab]");
      if (t) self.showTab(t.dataset.tab);
      var a = e.target.closest("[data-act]");
      if (a && a.dataset.act === "reset") self.restart();
      if (a && a.dataset.act === "close" && self.opts.onClose) self.opts.onClose();
    });
    this.out.addEventListener("click", function () {
      if (!self.input.disabled && !window.getSelection().toString()) self.input.focus({ preventScroll: true });
    });
  };

  Terminal.prototype.showTab = function (name) {
    this.host.querySelectorAll("[data-tab]").forEach(function (t) {
      t.setAttribute("aria-selected", String(t.dataset.tab === name));
    });
    var files = name === "files";
    this.files.hidden = !files;
    this.out.hidden = files;
    this.form.hidden = files;
    this.chips.hidden = files;
    if (files) this.renderFiles();
  };

  Terminal.prototype.write = function (text, cls) {
    if (!text) return;
    var span = document.createElement("span");
    if (cls) span.className = cls;
    span.textContent = text;
    this.out.appendChild(span);
    if (this.out.childNodes.length > 1500) this.out.removeChild(this.out.firstChild);
    this.out.scrollTop = this.out.scrollHeight;
  };

  Terminal.prototype.ask = function (chips) {
    var self = this;
    var gen = this.gen;
    this.setChips(chips || []);
    this.out.scrollTop = this.out.scrollHeight; // chips change the output's height
    this.input.disabled = false;
    if (this.opts.focus !== false && this.host.getBoundingClientRect().top < window.innerHeight) {
      this.input.focus({ preventScroll: true });
    }
    return new Promise(function (resolve, reject) {
      self.pending = { resolve: resolve, reject: reject, gen: gen };
      if (self.queue.length) {
        var next = self.queue.shift();
        setTimeout(function () { if (self.pending && self.pending.gen === gen) self.submit(next); }, 260);
      }
    });
  };

  Terminal.prototype.submit = function (value) {
    if (!this.pending) return;
    var p = this.pending;
    this.pending = null;
    if (p.rerun) { this.restart(); return; }
    this.input.value = "";
    this.input.disabled = true;
    this.setChips([]);
    this.write(value + "\n", "u");
    if (this.files && !this.files.hidden) this.renderFiles();
    p.resolve(value);
  };

  Terminal.prototype.setChips = function (chips) {
    this.chips.innerHTML = chips.map(function (c) {
      var v = Array.isArray(c) ? c[0] : c;
      var label = Array.isArray(c) ? c[1] : c;
      return '<button type="button" class="con-chip" data-v="' + window.CE.escapeHtml(v) + '">' + window.CE.escapeHtml(label) + "</button>";
    }).join("");
  };

  Terminal.prototype.restart = function (script) {
    this.gen++;
    if (this.pending) { this.pending.reject(new Abort()); this.pending = null; }
    this.queue = script ? script.slice() : [];
    this.out.textContent = "";
    this.showTab("run");
    var program = new Program(this);
    this.program = program;
    var self = this;
    var gen = this.gen;
    program.run().then(function () {
      if (gen !== self.gen) return;
      self.write("\nProcess finished with exit code 0\n", "sys");
      self.input.disabled = true;
      self.setChips([["__rerun", "↻ Run again"]]);
      self.pending = { gen: gen, rerun: true, reject: function () {}, resolve: function () {} };
    }, function (e) {
      if (!(e instanceof Abort)) { self.write("\n" + e + "\n", "err"); }
    });
  };

  Terminal.prototype.renderFiles = function () {
    var self = this;
    var prog = this.program;
    if (!prog) return;
    var current = this.fileKey || "students";
    var bar = '<div class="con-files-bar"><span>File</span>' + FILES.map(function (k) {
      return '<button type="button" data-file="' + k + '" aria-pressed="' + (k === current) + '">' + k + ".txt</button>";
    }).join("") + "</div>";
    var disk = prog.disk[current] || [];
    var mem;
    try { mem = prog.serialize(current); } catch (e) { mem = ["(saving now would throw NullPointerException)"]; }
    function col(title, lines, other) {
      return '<div class="con-files-col"><h4>' + title + "</h4><pre>" + (lines.length ? lines.map(function (l) {
        var changed = other.indexOf(l) < 0;
        return '<span class="' + (changed ? "chg" : "") + '">' + window.CE.escapeHtml(l) + "</span>";
      }).join("\n") : '<span style="color:#6f737a">(empty)</span>') + "</pre></div>";
    }
    this.files.innerHTML = bar + '<div class="con-files-grid">' +
      col("On disk", disk, mem) + col("In memory · written on save", mem, disk) + "</div>";
    this.files.querySelectorAll("[data-file]").forEach(function (b) {
      b.addEventListener("click", function () { self.fileKey = b.dataset.file; self.renderFiles(); });
    });
  };

  /* ---------------------------------------------------------------------
     The program
     --------------------------------------------------------------------- */
  function Program(term) {
    this.t = term;
    this.disk = JSON.parse(JSON.stringify(SAMPLE.disk));
    this.students = [];
    this.instructors = [];
    this.administrators = [];
    this.courses = [];
    this.grades = [];
  }

  var P = Program.prototype;

  P.print = function (s) { this.t.write(str(s)); };
  P.println = function (s) { this.t.write((s === undefined ? "" : str(s)) + "\n"); };
  P.header = function (s) { this.t.write(s + "\n", "hdr"); };

  P.nextLine = function (chips) { return this.t.ask(chips); };
  P.next = function (chips) {
    return this.t.ask(chips).then(function (v) { return v.trim().split(/\s+/)[0] || ""; });
  };
  P.nextInt = function (chips) {
    return this.next(chips).then(function (v) {
      if (!/^[+-]?\d+$/.test(v)) throw new JavaException(null);
      return parseInt(v, 10);
    });
  };
  P.getSafeIntInput = async function (prompt, chips) {
    for (;;) {
      this.print(prompt);
      var v = (await this.nextLine(chips)).trim().split(/\s+/)[0];
      if (/^[+-]?\d+$/.test(v)) return parseInt(v, 10);
      this.println("Invalid input. Please enter a number.");
    }
  };

  /* ----- toString / helpers ----- */
  function userStr(u) { return u ? "-ID: " + u.id + " Name: " + u.name : "null"; }
  function isFull(c) { return c.students !== null && c.students.length >= c.capacity; }

  var V = {
    ValidatePassword: function (s) { return s !== null && s.length > 8; },
    ValidateEmail: function (s) { return s.indexOf("@") >= 0 && s.indexOf(".") >= 0; },
    ValidatePhoneNumber: function (s) { return s.length === 10; },
    ValidateAddress: function (s) { return s.length > 3; },
    ValidateName: function (s) { return s.length > 3; }
  };

  function newStudent(name, id, password, email, phone, address, limit, courses, prog) {
    var s = { kind: "student", name: name, id: id, password: password, email: email, phone: phone, address: address,
      role: "STUDENT", creditLimit: 0, courses: courses || [] };
    setCreditLimit(s, limit, prog);
    return s;
  }
  function setCreditLimit(s, n, prog) {
    if (n < 0) { prog.println("Must be greater than 0"); return; }
    s.creditLimit = n;
  }
  function newUser(kind, role, name, id, password, email, phone, address) {
    return { kind: kind, name: name, id: id, password: password, email: email, phone: phone, address: address, role: role };
  }
  P.newCourse = function (name, code, schedule, description, status, instructor, capacity, hours) {
    var c = { name: null, code: null, schedule: null, description: null, status: status, instructor: instructor || null,
      capacity: 0, creditHours: 0, students: [] };
    if (!name) this.println("Course name cannot be null or empty."); else c.name = name;
    if (!code) this.println("Course code cannot be null or empty."); else c.code = code;
    c.schedule = schedule || null;
    c.description = description || null;
    if (capacity > 0) c.capacity = capacity; else this.println("Error: Capacity must be > 0.");
    if (hours > 0) c.creditHours = hours; else this.println("Credit hours can not be <= 0");
    return c;
  };

  /* ----- dataManager: load / save ----- */
  P.getCourseByCode = function (code) { return this.courses.filter(function (c) { return c.code === code; })[0] || null; };
  P.getStudentById = function (id) { return this.students.filter(function (s) { return s.id === id; })[0] || null; };
  P.getInstructorById = function (id) { return this.instructors.filter(function (s) { return s.id === id; })[0] || null; };

  P.loadAllData = function () {
    var self = this;
    // loadStudents runs first, so course codes cannot be resolved yet.
    this.disk.students.forEach(function (line) {
      self.println("Loading student: " + line);
      var p = line.split("|");
      if (p.length < 7) return;
      var enrolled = [];
      if (p.length > 7 && p[7]) {
        p[7].split(",").forEach(function (code) {
          var c = self.getCourseByCode(code.trim());
          if (c) enrolled.push(c);
        });
      }
      var s = newStudent(p[0], p[1], p[2], p[3], p[4], p[5], parseInt(p[6], 10), enrolled, self);
      self.println(userStr(s));
      if (!self.getStudentById(s.id)) self.students.push(s);
    });
    this.disk.instructors.forEach(function (line) {
      var p = line.split("|");
      if (p.length >= 6 && !self.getInstructorById(p[1])) self.instructors.push(newUser("instructor", "INSTRUCTOR", p[0], p[1], p[2], p[3], p[4], p[5]));
    });
    this.disk.administrators.forEach(function (line) {
      var p = line.split("|");
      if (p.length >= 6 && !self.administrators.some(function (a) { return a.id === p[1]; })) {
        self.administrators.push(newUser("admin", "ADMIN", p[0], p[1], p[2], p[3], p[4], p[5]));
      }
    });
    this.disk.courses.forEach(function (line) {
      var p = line.split("|");
      if (p.length < 8) return;
      var c = self.newCourse(p[0], p[1], p[2], p[3], p[4], p[5] ? self.getInstructorById(p[5]) : null, parseInt(p[6], 10), parseInt(p[7], 10));
      var roster = [];
      if (p.length > 8 && p[8]) {
        p[8].split(",").forEach(function (id) {
          var s = self.getStudentById(id.trim());
          if (s) roster.push(s);
        });
      }
      c.students = roster;
      if (!self.getCourseByCode(c.code)) self.courses.push(c);
    });
    this.disk.assessments.forEach(function (line) {
      var p = line.split("|");
      if (p.length >= 5) self.grades.push({ studentId: p[0], courseCode: p[1], examType: p[2], score: parseFloat(p[3]), name: p[4] });
    });
  };

  P.serialize = function (key) {
    if (key === "students") {
      return this.students.map(function (s) {
        return [s.name, s.id, s.password, s.email, s.phone, s.address, String(s.creditLimit),
          s.courses.map(function (c) { return c.code; }).join(",")].join("|");
      });
    }
    if (key === "instructors" || key === "administrators") {
      return this[key].map(function (u) { return [u.name, u.id, u.password, u.email, u.phone, u.address].join("|"); });
    }
    if (key === "courses") {
      return this.courses.map(function (c) {
        if (c.status === null || c.status === undefined) throw new JavaException(null);
        return [c.name, c.code, c.schedule || "", c.description || "", c.status, c.instructor ? c.instructor.id : "",
          String(c.capacity), String(c.creditHours), c.students.map(function (s) { return s.id; }).join(",")].join("|");
      });
    }
    return this.grades.map(function (g) { return [g.studentId, g.courseCode, g.examType, jd(g.score), g.name].join("|"); });
  };
  P.save = function (key) { this.disk[key] = this.serialize(key); };
  P.saveAllData = function () { var self = this; FILES.forEach(function (k) { self.save(k); }); };

  /* ----- main() ----- */
  P.run = async function () {
    this.println("Testing Constructor");
    this.loadAllData();
    try {
      var exit = false;
      var d = SAMPLE.defaultAdmin;
      var admin = newUser("admin", "ADMIN", d.name, d.id, d.password, d.email, d.phone, d.address);
      if (!this.administrators.some(function (a) { return a.id === admin.id; })) {
        this.administrators.push(admin);
        this.save("administrators");
        this.println("Administrator added: " + admin.name + " with ID: " + admin.id);
      } else {
        this.println("Error: Administrator ID " + admin.id + " already exists.");
      }
      this.println("\nWelcome to School Course Enrolment System!");
      while (!exit) {
        this.println("Enter your role from the current options: (Student/Instructor/Admin) or exit to finish.");
        var role = await this.next(["student", "instructor", "admin", "exit"]);
        switch (role.toLowerCase()) {
          case "student": await this.studentSession(); break;
          case "instructor": await this.instructorSession(); break;
          case "admin": await this.adminSession(); break;
          case "exit":
            exit = true;
            this.saveAllData();
            this.println("Goodbye.");
            break;
          default:
            this.println("Invalid role. Try again.");
        }
      }
    } catch (e) {
      if (e instanceof Abort) throw e;
      if (e instanceof JavaException) { this.println("Error: " + str(e.message)); return; }
      throw e;
    }
  };

  /* ----- Helpers.login<T> ----- */
  P.login = async function (list, kind) {
    var ids = list.slice(0, 3).map(function (u) { return u.id; });
    this.print("\nPlease enter your ID: ");
    var id = await this.next(ids);
    if (!list.some(function (u) { return u.id === id; })) this.println("No user found with the entered ID.");
    var known = list.filter(function (u) { return u.id === id; })[0];
    for (var attempts = 0; attempts < 3;) {
      this.print("\nPlease enter your password: ");
      var pw = await this.nextLine(known ? [known.password] : []);
      var user = this.subclassLogin(list, kind, id, pw);
      if (user) return user;
      attempts++;
      if (attempts < 3) this.println("Incorrect password. Try again (" + (3 - attempts) + " attempts left).");
    }
    this.println("Too many failed attempts. Returning to main menu.");
    return null;
  };

  P.subclassLogin = function (list, kind, id, pw) {
    var i;
    if (kind === "admin") {
      for (i = 0; i < list.length; i++) {
        if (list[i].id === id && list[i].password === pw) {
          this.println("Administrator " + list[i].name + " logged in.");
          return list[i];
        }
        this.println("No admin record was found with the ID and password provided.");
      }
      return null;
    }
    for (i = 0; i < list.length; i++) {
      if (list[i].id === id && list[i].password === pw) {
        this.println(kind === "student" ? "Student " + list[i].name + " logged in." : "Instructor " + list[i].name + " logged in.\n");
        return list[i];
      }
    }
    this.println("No " + kind + " record was found with the ID and password provided.");
    return null;
  };

  function menuChips(labels) {
    return labels.map(function (l, i) { return [String(i + 1), (i + 1) + " " + l]; });
  }
  var YES_NO = [["1", "1 Yes"], ["2", "2 No"]];

  /* ----- Student ----- */
  var STUDENT_MENU = ["View avaliable courses.", "Enroll in course.", "View enrolled courses.", "View credit limit.",
    "Drop course.", "View grades.", "Update personal information.", "Logout."];

  P.studentSession = async function () {
    var s = await this.login(this.students, "student");
    if (!s) return;
    for (;;) {
      this.println("");
      this.header("\n---------Student Menu---------");
      var self = this;
      STUDENT_MENU.forEach(function (l, i) { self.println((i + 1) + ". " + l); });
      var choice = await this.getSafeIntInput("Option: ", menuChips(["Available", "Enroll", "Enrolled", "Credit", "Drop", "Grades", "Profile", "Logout"]));
      switch (choice) {
        case 1: this.viewAvailableCourses(); break;
        case 2: await this.enrollHelper(s); break;
        case 3: this.viewEnrolledCourses(s); break;
        case 4: this.viewCreditLimit(); break;
        case 5: await this.dropHelper(s); break;
        case 6: await this.viewGrades(s); break;
        case 7: await this.updateProfile(s, "student"); this.save("students"); break;
        case 8: return; // logout() returns a message that main() never prints
        default: this.println("Invalid option.");
      }
    }
  };

  P.viewAvailableCourses = function () {
    var any = false, self = this;
    this.println("\nAvailable courses are: ");
    this.courses.forEach(function (c) {
      if (!isFull(c) && c.status === "Open") {
        any = true;
        self.println("- (Course name: " + c.name + ") (Course code: " + c.code + ") (Course schedule: " + str(c.schedule) +
          ") (Course instructor: " + userStr(c.instructor) + ") (Course capacity: " + c.capacity + ").\n");
      }
    });
    if (!any) this.println("No courses are avaliable.");
  };

  P.enrollHelper = async function (s) {
    try {
      this.println("\n---------Enroll In Course---------");
      var available = this.courses.filter(function (c) { return !isFull(c) && c.status === "Open" && s.courses.indexOf(c) < 0; });
      if (!available.length) { this.println("No available courses to enroll in."); return; }
      this.println("Courses available to enroll in:");
      var self = this;
      available.forEach(function (c, i) { self.print((i + 1) + ". " + c.name + " (" + c.code + ")\n"); });
      this.print("\nEnter the number of the course you would like to enroll in: ");
      var n = await this.nextInt(available.map(function (c, i) { return [String(i + 1), (i + 1) + " " + c.code]; }));
      if (n >= 1 && n <= available.length) this.enroll(s, available[n - 1]);
      else this.println("Invalid selection: " + n);
    } catch (e) {
      if (!(e instanceof JavaException)) throw e;
      this.println(str(e.message));
    }
  };

  P.enroll = function (s, c) {
    var hours = s.courses.reduce(function (a, x) { return a + x.creditHours; }, 0);
    if (s.courses.indexOf(c) >= 0) this.print("\nYou are already enrolled in (" + c.name + ") (" + c.code + ").");
    else if (isFull(c)) this.println("\nCannot enroll in " + c.name + " - course is full.");
    else if (c.status === "Closed") this.println("\nEnrollment status is closed.");
    else if (hours + c.creditHours > s.creditLimit) this.println("\nCannot enroll in " + c.name + " - credit limit exceeded.");
    else {
      c.students.push(s);
      s.courses.push(c);
      this.println("\n" + s.name + " enrolled successfully");
    }
  };

  P.viewEnrolledCourses = function (s) {
    if (!s.courses.length) { this.println(s.name + " is not enrolled in any courses."); return; }
    this.println(s.name + " is enrolled in: ");
    var self = this;
    s.courses.forEach(function (c, i) {
      self.print((i + 1) + "- (" + c.name + ") (" + c.code + ") (" + c.creditHours + "). The schedule is: " + str(c.schedule) + ".");
    });
  };

  P.viewCreditLimit = function () {
    // Loops over every student and breaks after the first: always the first student's numbers.
    for (var i = 0; i < this.students.length; i++) {
      var st = this.students[i];
      this.println("Your credit limit is: " + st.creditLimit);
      var used = st.courses.reduce(function (a, c) { return a + c.creditHours; }, 0);
      this.println("Remaining credit limit is: " + (st.creditLimit - used) + " hours.");
      break;
    }
  };

  P.dropHelper = async function (s) {
    this.println("\n---------Unenroll In Course---------");
    this.print("\nEnter course code of the course you would like to drop: ");
    var code = await this.next(s.courses.map(function (c) { return c.code; }));
    var c = this.courses.filter(function (x) { return x.code && x.code.toLowerCase() === code.toLowerCase(); })[0];
    if (!c) { this.println("No course found with the code" + code + "'."); return; }
    if (s.courses.indexOf(c) < 0) this.print(s.name + " is not enrolled in (" + c.name + ") (" + c.code + ").");
    else if (c.status === "Closed") this.println("Drop period is closed.");
    else if (c.status === "Open") {
      s.courses.splice(s.courses.indexOf(c), 1); // the course roster is left unchanged
      this.print(s.name + " has successfully dropped (" + c.name + ") (" + c.code + ").");
    }
  };

  P.viewGrades = async function (s) {
    this.println("\nWhat would you like to view?\n1. View a specific exam score.\n2. View all grades in a course.\n3. View total average in a course.");
    var choice = await this.getSafeIntInput("\nOption: ", [["1", "1 Exam score"], ["2", "2 All grades"], ["3", "3 Average"]]);
    var courses = s.courses, self = this, n;
    function courseChips() { return courses.map(function (c, i) { return [String(i + 1), (i + 1) + " " + c.code]; }); }
    if (choice === 1) {
      if (!courses.length) { this.println("You are not enrolled in any courses."); return; }
      this.println("Select a course: ");
      courses.forEach(function (c, i) { self.print((i + 1) + "." + c.name + " (" + c.code + ").\n"); });
      n = await this.getSafeIntInput("Choice: ", courseChips());
      if (n < 1 || n > courses.length) { this.println("Invalid selection."); return; }
      var code = courses[n - 1].code;
      var types = SAMPLE.examTypes;
      this.println("Select an exam to view:");
      types.forEach(function (t, i) { self.println((i + 1) + ". " + t); });
      var e = await this.getSafeIntInput("Choice: ", types.map(function (t, i) { return [String(i + 1), (i + 1) + " " + t]; }));
      if (e < 1 || e > types.length) { this.println("Invalid exam type."); return; }
      var found = false;
      this.grades.forEach(function (g) {
        if (g.studentId === s.id && g.courseCode === code && g.examType === types[e - 1]) {
          self.println("Your " + types[e - 1] + " score: " + jd(g.score));
          found = true;
        }
      });
      if (!found) this.println("No " + types[e - 1] + " score found for this course.");
    } else if (choice === 2) {
      if (!courses.length) { this.println("You are not enrolled in any courses."); return; }
      this.println("Select a course to view all your grades:");
      courses.forEach(function (c, i) { self.print((i + 1) + "." + c.name + " (" + c.code + ")."); });
      n = await this.getSafeIntInput("Option: ", courseChips());
      if (n < 1 || n > courses.length) { this.println("Invalid course selection."); return; }
      var code2 = courses[n - 1].code, any = false;
      this.grades.forEach(function (g) {
        if (g.studentId === s.id && g.courseCode === code2) { self.println(g.examType + ": " + jd(g.score)); any = true; }
      });
      if (!any) this.println("No grades found for this course.");
    } else if (choice === 3) {
      if (!courses.length) { this.println("\nYou are not enrolled in any courses."); return; }
      this.println("\nSelect a course:");
      courses.forEach(function (c, i) { self.print((i + 1) + "." + c.name + " ( " + c.code + " )"); });
      n = await this.getSafeIntInput("\nOption: ", courseChips());
      if (n < 1 || n > courses.length) { this.println("Invalid course selection."); return; }
      var code3 = courses[n - 1].code, total = 0, count = 0;
      this.grades.forEach(function (g) { if (g.studentId === s.id && g.courseCode === code3) { total += g.score; count++; } });
      if (count > 0) this.println("Your total average grade in " + code3 + " is: " + jd(total / count));
      else this.println("No grades found for this course.");
    } else {
      this.println("Invalid choice.");
    }
  };

  /* ----- Shared prompts ----- */
  P.updateField = async function (field, current, valid, sample) {
    this.println("\nDo you want to change your " + field + "? \n1.Yes \n2.No");
    var choice = await this.getSafeIntInput("\nOption: ", YES_NO);
    if (choice !== 1) { this.println(field + " remains unchanged."); return current; }
    this.print("\nEnter new " + field + ": ");
    var v = await this.nextLine(sample ? [sample] : []);
    while (!valid(v)) {
      this.println("Invalid " + field + ". Please try again.");
      this.print("\nEnter new " + field + ": ");
      v = await this.nextLine(sample ? [sample] : []);
    }
    return v;
  };

  P.createField = async function (field, valid, sample) {
    for (;;) {
      this.print("\nEnter " + field + ": ");
      var v = await this.nextLine(sample ? [sample] : []);
      if (!valid(v)) this.println("Invalid " + field + ". Please try again.");
      else return v;
    }
  };

  P.updateProfile = async function (u, kind) {
    this.println("\n---------Update Personal Profile---------");
    this.println(kind === "student" ? "\nPlease enter the needed information to update your profile." : "\nPlease fill out the form to update your profile.");
    var pw = await this.updateField("password", u.password, V.ValidatePassword, "NewPassword99");
    var em = await this.updateField("email", u.email, V.ValidateEmail, "new.mail@uni.example");
    var ph = await this.updateField("phone number", u.phone, V.ValidatePhoneNumber, "0555555555");
    var ad = await this.updateField("address", u.address, V.ValidateAddress, "South Campus");
    u.password = pw; u.email = em; u.phone = ph; u.address = ad;
    if (kind === "student") this.println("\nStudent " + u.name + "'s information updated.");
    else {
      this.println("Instructor " + u.name + "'s information updated.");
      this.println("Instructor " + u.name + "'s information updated.");
    }
  };

  P.checkValidityOfRole = async function () {
    for (;;) {
      this.println("Select a role: \n1. STUDENT \n2. INSTRUCTOR \n3. ADMIN \nOption:");
      var o = await this.getSafeIntInput("\nOption: ", [["1", "1 STUDENT"], ["2", "2 INSTRUCTOR"], ["3", "3 ADMIN"]]);
      if (o === 1) return "STUDENT";
      if (o === 2) return "INSTRUCTOR";
      if (o === 3) return "ADMIN";
      this.println("Invalid selection. Please enter 1, 2, or 3.");
    }
  };

  P.updateRolePrompt = async function (current) {
    this.println("\nDo you want to change the role? \n1.Yes \n2.No");
    var c = await this.getSafeIntInput("\nOption: ", YES_NO);
    if (c === 1) return this.checkValidityOfRole();
    this.println("Role remains unchanged.");
    return current;
  };

  /* ----- Instructor ----- */
  var INSTRUCTOR_MENU = ["View enrolled students.", "Grade assignments.", "Update course information.", "Update personal information.", "Logout."];

  P.instructorSession = async function () {
    var me = await this.login(this.instructors, "instructor");
    if (!me) return;
    for (;;) {
      this.println("");
      this.header("\n---------Instructor Menu---------");
      var self = this;
      INSTRUCTOR_MENU.forEach(function (l, i) { self.println((i + 1) + ". " + l); });
      var choice = await this.getSafeIntInput("Option: ", menuChips(["Rosters", "Grade", "Course info", "Profile", "Logout"]));
      switch (choice) {
        case 1: this.viewEnrolledStudents(me); break;
        case 2: await this.gradeStudent(me); break;
        case 3: await this.updateCourseInfo(me); this.save("courses"); break;
        case 4: await this.updateProfile(me, "instructor"); this.save("instructors"); break;
        case 5: return;
        default: this.println("Invalid option.");
      }
    }
  };

  P.viewEnrolledStudents = function (me) {
    var any = false, self = this;
    this.courses.forEach(function (c) {
      if (c.instructor && c.instructor.id === me.id) {
        any = true;
        self.print("\n(Course: " + c.name + ") (Code: " + c.code + ")");
        if (!c.students.length) self.println("No students enrolled in this course.");
        else c.students.forEach(function (s) {
          self.print("\n-Student: " + s.name + ", ID: " + s.id + ", Email: " + s.email + ", Phone number: " + s.phone);
        });
      }
    });
    if (!any) this.println("Instructor " + me.name + " is not assigned to any courses.");
  };

  P.gradeStudent = async function (me) {
    var self = this;
    this.println("\nCourses you're assigned to:");
    var mine = this.courses.filter(function (c) { return c.instructor && c.instructor.id === me.id; });
    mine.forEach(function (c, i) { self.println((i + 1) + ". " + c.name + " (" + c.code + ")"); });
    if (!mine.length) { this.println("You're not assigned to any courses."); return; }
    var ci = await this.getSafeIntInput("Select a course to grade: ", mine.map(function (c, i) { return [String(i + 1), (i + 1) + " " + c.code]; }));
    if (ci < 1 || ci > mine.length) { this.println("Invalid selection."); return; }
    var course = mine[ci - 1];
    if (!course.students.length) { this.println("No students enrolled in this course."); return; }
    this.println("\nStudents in this course:");
    course.students.forEach(function (s, i) { self.print((i + 1) + "." + s.name + " (ID: " + s.id + ")"); });
    var si = await this.getSafeIntInput("\nSelect a student to grade: ", course.students.map(function (s, i) { return [String(i + 1), (i + 1) + " " + s.name]; }));
    if (si < 1 || si > course.students.length) { this.println("Invalid student selection."); return; }
    var student = course.students[si - 1];
    var types = SAMPLE.examTypes;
    this.println("\nSelect the assessment type to grade:");
    types.forEach(function (t, i) { self.println((i + 1) + ". " + t); });
    var ti = await this.getSafeIntInput("Choice: ", types.map(function (t, i) { return [String(i + 1), (i + 1) + " " + t]; }));
    if (ti < 1 || ti > types.length) { this.println("Invalid selection."); return; }
    var type = types[ti - 1], score;
    for (;;) {
      this.print("Enter score (0-100): ");
      var raw = (await this.nextLine(["95", "72.5"])).trim();
      if (!/^[+-]?(\d+\.?\d*|\.\d+)$/.test(raw)) { this.println("Invalid input. Please enter a number."); continue; }
      score = parseFloat(raw);
      if (score < 0 || score > 100) this.println("Score must be between 0 and 100.");
      else break;
    }
    var existing = this.grades.filter(function (g) { return g.studentId === student.id && g.courseCode === course.code && g.examType === type; })[0];
    if (existing) { existing.score = score; this.println("Grade updated successfully."); }
    else { this.grades.push({ studentId: student.id, courseCode: course.code, examType: type, score: score, name: type }); this.println("Grade recorded successfully."); }
  };

  P.updateCourseInfo = async function (me) {
    this.println("\n---------Update Course Information---------\nEnter the course code of the course you would like to update: ");
    var mine = this.courses.filter(function (c) { return c.instructor && c.instructor.id === me.id; }).map(function (c) { return c.code; });
    var code = await this.next(mine);
    this.print("\nEnter new schedule:");
    var sched = await this.nextLine(["Mon/Wed 14:00"]);
    this.print("\nEnter new description: ");
    var desc = await this.nextLine(["Updated outline"]);
    var c = this.getCourseByCode(code);
    if (!c) { this.println("Course with code " + code + " not found."); return; }
    var assigned = c.instructor;
    if (assigned && assigned.id === me.id) {
      c.schedule = sched || null;
      c.description = desc || null;
      this.print("Instructor " + assigned.name + "'s course information updated for " + c.name);
    } else if (assigned) {
      this.print(assigned.name + " with the ID number: " + assigned.id + " is not assigned to " + c.name + ".");
    } else {
      this.print("No instructor assigned to " + c.name + ".");
    }
  };

  /* ----- Administrator ----- */
  var ADMIN_MENU = ["Add Students.", "Remove Students.", "View student list.", "Add Instructors.", "Remove Instructors.",
    "View instructor list.", "Add Course.", "Close Course.", "Update Student Info.", "Update Instructor Info.",
    "Assign Instructor to Course.", "View Enrollment Statistics.", "Generate Reports.", "Logout."];

  P.adminSession = async function () {
    var me = await this.login(this.administrators, "admin");
    if (!me) return;
    for (;;) {
      this.println("");
      this.header("\n---------Administrator Menu---------");
      var self = this;
      ADMIN_MENU.forEach(function (l, i) { self.println((i + 1) + ". " + l); });
      var choice = await this.getSafeIntInput("Option: ", menuChips(["Add student", "Remove student", "Students", "Add instructor",
        "Remove instructor", "Instructors", "Add course", "Close course", "Edit student", "Edit instructor", "Assign", "Statistics", "Report", "Logout"]));
      try {
        switch (choice) {
          case 1: await this.addUser("student"); break;
          case 2: await this.removeStudent(); break;
          case 3: this.listUsers(this.students, "students"); break;
          case 4: await this.addUser("instructor"); break;
          case 5: await this.removeInstructor(); break;
          case 6: this.listUsers(this.instructors, "instructors"); break;
          case 7: await this.addCourse(); break;
          case 8: await this.closeCourse(); break;
          case 9: await this.adminUpdate("student"); this.save("students"); break;
          case 10: await this.adminUpdate("instructor"); this.save("instructors"); break;
          case 11: await this.assignInstructor(); break;
          case 12: this.viewEnrollmentStatistics(); break;
          case 13: this.generateReports(); break;
          case 14: return;
          default: this.println("Invalid option.");
        }
      } catch (e) {
        if (!(e instanceof JavaException)) throw e;
        this.println(str(e.message)); // the Helpers flows catch and print e.getMessage()
      }
    }
  };

  function randomId(list) {
    for (;;) {
      var id = "";
      for (var i = 0; i < 10; i++) id += Math.floor(Math.random() * 10);
      if (!list.some(function (u) { return u.id === id; })) return id;
    }
  }

  P.addUser = async function (kind) {
    var list = kind === "student" ? this.students : this.instructors;
    this.println(kind === "student" ? "\n---------Create New Student---------" : "\n---------Create New Instructor---------");
    var name;
    for (;;) {
      this.print("\nEnter " + kind + " name: ");
      name = await this.nextLine([kind === "student" ? "Huda Nasser" : "Reem Aziz"]);
      if (!V.ValidateName(name)) { this.println("Invalid name. Please enter a valid name."); continue; }
      break;
    }
    var id = randomId(list);
    var pw = await this.createField("password", V.ValidatePassword, "Welcome2026");
    var em = await this.createField("email", V.ValidateEmail, kind === "student" ? "huda.n@uni.example" : "reem.a@uni.example");
    var ph = await this.createField("phone number", V.ValidatePhoneNumber, "0500000999");
    var ad = await this.createField("address", V.ValidateAddress, "Main Campus");
    if (kind === "student") {
      this.print("\nEnter credit limit: ");
      var limit = await this.nextInt(["15", "18"]);
      var s = newStudent(name, id, pw, em, ph, ad, limit, [], this);
      this.students.push(s);
      this.print("Student added: " + s.name + " with the ID: " + s.id);
    } else {
      var u = newUser("instructor", "INSTRUCTOR", name, id, pw, em, ph, ad);
      this.instructors.push(u);
      this.print("Instructor added: " + u.name + " with the ID: " + u.id);
    }
  };

  P.removeStudent = async function () {
    this.println("\n---------Remove Student---------");
    this.print("\nEnter the ID of the student to remove: ");
    var id = await this.next(this.students.slice(-2).map(function (s) { return s.id; }));
    var i = this.students.findIndex(function (s) { return s.id === id; });
    if (i >= 0) {
      var s = this.students.splice(i, 1)[0];
      this.println(s.name + " with the ID: " + s.id + " has been successfully removed");
    } else {
      this.println(id + " is not found.");
    }
    this.println("Invalid option."); // printed after the try/catch, every time
  };

  P.removeInstructor = async function () {
    this.println("\n---------Remove Instructor---------");
    this.print("\nEnter the ID of the instructor to remove: ");
    var id = await this.next(this.instructors.slice(-2).map(function (s) { return s.id; }));
    var i = this.instructors.findIndex(function (s) { return s.id === id; });
    if (i >= 0) {
      var u = this.instructors.splice(i, 1)[0];
      this.println(u.name + " with the ID: " + u.id + " removed successfully.");
    } else {
      this.println("Instructor with the ID: " + id + " not found.");
    }
  };

  P.listUsers = function (list, word) {
    var self = this;
    if (!list.length) { this.println("\nNo " + word + " are on record."); return; }
    list.forEach(function (u) { self.println(userStr(u)); });
  };

  P.assign = function (course, inst) {
    if (course.instructor === null) {
      course.instructor = inst;
      if (!inst) throw new JavaException(null); // specificInstructor.getName() on null
      this.print("Instructor " + inst.name + " is assigned to " + course.name);
    } else if (course.instructor === inst) {
      this.print("Instructor " + inst.name + " is already assigned to " + course.name);
    } else {
      this.println("Course already has a different instructor assigned.");
    }
  };

  P.addCourse = async function () {
    this.println("\n---------Create Course---------");
    this.print("\nEnter the course's information that you would like to create.\n\nEnter course name: ");
    var name = await this.nextLine(["Operating Systems"]);
    this.print("\nEnter course code: ");
    var code = await this.nextLine(["CS330"]);
    this.print("\nEnter course capacity: ");
    var cap = await this.nextInt(["25"]);
    this.print("\nEnter course credit hours: ");
    var hours = await this.nextInt(["3"]);
    var c = this.newCourse(name, code, null, null, null, null, cap, hours);
    this.println("\nWould you like to assign instructor now? \n1. Assign now. \n2. Assign later.");
    var a = await this.getSafeIntInput("\nOption: ", [["1", "1 Assign now"], ["2", "2 Later"]]);
    if (a === 1) {
      this.print("\nAssign instructor by ID: ");
      var iid = await this.nextLine(this.instructors.map(function (i) { return i.id; }).concat(["4999999999"]));
      if (!this.instructors.length) { this.println("\nNo instructors available. Please add an instructor before creating a course."); return; }
      var inst = this.instructors.filter(function (i) { return i.id === iid; })[0] || null;
      this.assign(c, inst);
    }
    if (a === 2) this.println("To be assigned.");
    this.println("\nEnter course status: \n1. Open \n2.Closed");
    var st = await this.getSafeIntInput("Option: ", [["1", "1 Open"], ["2", "2 Closed"]]);
    if (st === 1) c.status = "Open";
    else if (st === 2) c.status = "Closed";
    this.courses.push(c);
    this.print("Course added: (" + c.name + ") (" + c.code + ") succesfully.");
  };

  P.closeCourse = async function () {
    this.println("\n---------Close Courses---------\nEnter the details requiered below.\nEnter course name: ");
    var name = await this.nextLine(this.courses.slice(-2).map(function (c) { return c.name; }));
    this.print("\nEnter course code: ");
    var code = await this.next(this.courses.filter(function (c) { return c.name === name; }).map(function (c) { return c.code; }));
    var c = this.courses.filter(function (x) { return x.name === name && x.code === code; })[0];
    if (!c) { this.println("Course not found."); return; }
    if (c.students.length >= c.capacity) {
      this.println(c.name + " is at full capacity.");
      c.status = "Closed";
    } else if (c.status === "Closed") {
      this.println(c.name + " enrollment status is closed.");
    }
    // An open course with space falls through: nothing printed, nothing changed.
  };

  P.adminUpdate = async function (kind) {
    var list = kind === "student" ? this.students : this.instructors;
    var name, id;
    if (kind === "student") {
      this.print("\n---------Update Student Profile---------\nPlease enter the requiered information below.\nStudent's name: ");
      name = await this.nextLine(list.slice(0, 2).map(function (u) { return u.name; }));
      this.print("\nStudent ID: ");
    } else {
      this.println("\n---------Update Instuctor Profile---------\nPlease enter the requiered information below.");
      this.print("\nEnter instructor name: ");
      name = await this.nextLine(list.slice(0, 2).map(function (u) { return u.name; }));
      this.print("\nEnter instructor ID: ");
    }
    id = await this.next(list.filter(function (u) { return u.name === name; }).map(function (u) { return u.id; }));
    var u = list.filter(function (x) { return x.name === name && x.id === id; })[0];
    if (!u) return; // nothing is printed when no match is found
    this.println(kind === "student" ? "Update " + u.name + " details below: " : "Update " + u.name + "'s details below: ");
    var nm = await this.updateField("name", u.name, V.ValidateName, u.name + " Jr");
    var pw = await this.updateField("password", u.password, V.ValidatePassword, "NewPassword99");
    var em = await this.updateField("email", u.email, V.ValidateEmail, "new.mail@uni.example");
    var ph = await this.updateField("phone number", u.phone, V.ValidatePhoneNumber, "0555555555");
    var ad = await this.updateField("address", u.address, V.ValidateAddress, "South Campus");
    var role = await this.updateRolePrompt(u.role);
    if (kind === "student") {
      this.print("\nDo you want to update " + u.name + "'s credit limit?\n1. Yes\n2. No");
      var c = await this.nextInt(YES_NO);
      if (c === 1) {
        this.print("\nEnter new credit limit: ");
        setCreditLimit(u, await this.nextInt(["18"]), this);
      } else if (c === 2) {
        this.println("Credit limit number remains unchanged.");
      }
    }
    u.name = nm; u.password = pw; u.email = em; u.phone = ph; u.address = ad; u.role = role;
    this.println((kind === "student" ? "Student " : "Instructor ") + nm + "'s profile updated successfully.");
  };

  P.assignInstructor = async function () {
    var self = this;
    this.println("\n---------Available Courses---------");
    this.courses.forEach(function (c, i) { self.print((i + 1) + ". " + c.name + " (" + c.code + ").\n"); });
    this.print("\nEnter the number of the course to assign the instructor to: ");
    var idx = (await this.nextInt(this.courses.map(function (c, i) { return [String(i + 1), (i + 1) + " " + c.code]; }))) - 1;
    if (idx < 0 || idx >= this.courses.length) { this.println("Invalid course selection."); return; }
    this.print("\nEnter the ID of the instructor to assign: ");
    var iid = await this.next(this.instructors.map(function (i) { return i.id; }));
    var inst = this.instructors.filter(function (i) { return i.id === iid; })[0];
    if (inst) this.assign(this.courses[idx], inst);
    else this.println("Instructor with ID " + iid + " not found.");
  };

  P.viewEnrollmentStatistics = function () {
    var total = 0, open = false, self = this;
    this.println("\n---------Enrollment Statistics---------");
    this.courses.forEach(function (c) {
      var n = c.students ? c.students.length : 0;
      total += n;
      self.println("Course: " + c.name + " (" + c.code + ") - Enrolled: " + n);
      if (c.status === "Open") open = true;
    });
    this.println("Total enrolled students across all courses: " + total);
    this.println("Open courses available: " + (open ? "Yes" : "No"));
  };

  P.generateReports = function () {
    this.println("\n---------Enrollment Report---------");
    var best = null, max = 0;
    this.courses.forEach(function (c) {
      var n = c.students ? c.students.length : 0;
      if (n > max) { best = c; max = n; }
    });
    if (best) this.println("Most popular course: " + best.name + " (" + best.code + ") - Enrolled: " + max + ".");
    else this.println("No enrollments found.");
  };

  /* ---------------------------------------------------------------------
     Mounting: inline consoles and the bottom dock
     --------------------------------------------------------------------- */
  var LOGINS = {
    student: ["student", "2200000001", "Student1234"],
    instructor: ["instructor", "4000000001", "Teacher1234"],
    admin: ["admin", "1122334455", "Default12345"]
  };

  function startWhenVisible(term) {
    if (!("IntersectionObserver" in window)) { term.restart(); return; }
    var io = new IntersectionObserver(function (entries) {
      if (entries.some(function (e) { return e.isIntersecting; })) { io.disconnect(); term.restart(); }
    });
    io.observe(term.host);
  }

  document.querySelectorAll("[data-inline-console]").forEach(function (host) {
    var term = new Terminal(host, { focus: false });
    host._term = term;
    startWhenVisible(term);
  });

  var dockEl = document.getElementById("dock");
  var dockTerm = null;
  function openDock(role) {
    if (!dockEl) return;
    var inline = document.querySelector("[data-inline-console]");
    if (inline && !role) {
      inline.scrollIntoView({ behavior: "smooth", block: "center" });
      if (inline._term && inline._term.input && !inline._term.input.disabled) inline._term.input.focus({ preventScroll: true });
      return;
    }
    if (!dockTerm) {
      dockTerm = new Terminal(dockEl, { dock: true, onClose: closeDock });
    }
    dockEl.hidden = false;
    document.body.classList.add("dock-open");
    dockTerm.restart(role ? LOGINS[role] : null);
  }
  function closeDock() {
    if (!dockEl) return;
    dockEl.hidden = true;
    document.body.classList.remove("dock-open");
    if (dockTerm) { dockTerm.gen++; if (dockTerm.pending) { dockTerm.pending.reject(new Abort()); dockTerm.pending = null; } }
  }
  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-run]");
    if (!b) return;
    e.preventDefault();
    openDock(b.dataset.run || null);
  });
})();
