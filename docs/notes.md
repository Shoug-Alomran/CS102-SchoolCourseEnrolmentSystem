---
title: "Notes & Known Issues"
description: "Known issues and improvement ideas for the CS102 School Course Enrolment System Java project."
---

# Notes & Issues

## Known issues from the report

- **Administrator login message:** In `Administrator.login`, the "No admin record" message prints inside the search loop instead of after it ends, so a failed search can print it more than once.
- **Unused instructor parameter:** The `Instructor` constructor accepts `enrolledStudents` but never uses it in the body. This may be intentional or an oversight.
- **Validation lives outside setters:** `User` setters do no validation. Input is checked by the `Helpers` validators (`ValidatePassword`, `ValidateEmail`, `ValidatePhoneNumber`, and others) before the setters are called.

## Improvement ideas

- Consolidate repetitive console I/O logic.
- Validate phone numbers using regex.
- Avoid printing "not found" messages repeatedly inside loops.
- Consider separating I/O from business logic for maintainability.
