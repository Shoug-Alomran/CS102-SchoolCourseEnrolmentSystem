# Project Structure

## Layers
- **Core Entities**: `User<T>` (abstract), `Student`, `Instructor`, `Administrator`, `Course`, `Assessment`
- **Utilities**: `Helpers` (validation, menus, login), `DataManager` (persistence)
- **Entry Point**: `SchoolCourseEnrolmentSystem` (main flow and role menus)

## Relations
- `Student` ↔ `Course`: enrol/drop with capacity and status checks  
- `Instructor` ↔ `Course`: assignment and grading  
- `Assessment`: `(student, course, examType) → score`

## Files (for persistence)
`students.txt`, `instructors.txt`, `administrators.txt`, `courses.txt`, `assessments.txt`