# User Class

The `User` class is the abstract base class for all user types in the School Enrollment System.  
It defines the shared attributes, behaviors, and structure that Students, Instructors, and Administrators inherit.

---

## Purpose

The purpose of the `User` class is to:

- Provide a unified structure for all system users
- Define common fields such as ID, name, email, and password
- Enforce consistent behavior through abstract methods
- Reduce code duplication across subclasses
- Support generic login and logout workflows

All user types extend this class and implement their own role‑specific logic.

---

## Structure and key components

### 1. Attributes

The `User` class defines the following fields:

- `name`  
- `ID`  
- `password`  
- `email`  
- `phoneNumber`  
- `role`  
- `address`

These fields represent the essential profile information required for authentication, communication, and identification within the system.

---

### 2. Enum: Role

The `Role` enumeration defines the allowed user types:

- `STUDENT`
- `INSTRUCTOR`
- `ADMIN`

Using an enum ensures type safety and prevents invalid role assignments.

---

### 3. Constructors

The class provides two constructors:

#### Default constructor

Used when creating an empty user object, typically during file loading or temporary object creation.

#### Parameterized constructor

Initializes all user fields at the moment of object creation.  
It uses setter methods to ensure that any future validation logic is automatically applied.

---

### 4. Setters and getters

The class provides standard getter and setter methods for all fields.

Design notes:

- Validation is intentionally kept outside the setters to avoid overloading the class with input logic.
- The `Helpers` class is responsible for validating user input before setters are called.

This separation keeps the `User` class clean and focused on data representation.

---

### 5. Abstract methods

The `User` class defines two abstract methods that all subclasses must implement:

    public abstract T login(List<T> list, String id, String password);
    public abstract String logout(T user);

#### login

Each subclass implements its own login logic.  
This allows:

- Students to authenticate from the student list  
- Instructors to authenticate from the instructor list  
- Administrators to authenticate from the admin list  

The method returns the authenticated user or `null` if authentication fails.

#### logout

Returns a simple confirmation message indicating that the user has logged out.

---

## Summary

The `User` class provides the foundation for all user types in the system.  
By defining shared attributes and enforcing abstract login and logout methods, it ensures consistency across Students, Instructors, and Administrators while allowing each subclass to implement its own role‑specific behavior.

This design supports clean inheritance, reduces duplication, and maintains a clear separation of responsibilities.
