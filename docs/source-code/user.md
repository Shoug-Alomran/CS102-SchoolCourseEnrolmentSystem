---
title: "User Class - Java Source Code"
description: "Full Java source of the abstract generic User<T> base class shared by students, instructors and administrators."
---

# User Class - Source Code

Full Java source of the abstract generic User<T> base class shared by students, instructors and administrators.

For an explanation of how this class works, see the [User class guide](../user.md). This listing comes from the [CS102 project report](../project-report.md).

```java title="User.java" linenums="1"
package schoolcourseenrolmentsystem;

import java.util.List;

public abstract class User<T> {
    // Attributes
    // enum is short for enumeration
    public enum Role {
        STUDENT,
        INSTRUCTOR,
        ADMIN;
    }

    private String name, ID, password, email, phoneNumber;
    private Role role;
    private String address;

    public User() { }

    // Constructor
    public User(String name, String id, String password, String email, String phoneNumber, Role role, String address) {
        setName(name);
        setId(id);
        setPassword(password);
        setEmail(email);
        setPhoneNumber(phoneNumber);
        setRole(role);
        setAddress(address);

    }
    //======================= Setters and Getters =======================
    // we do validation in prior to calling this method to avoid bloating it
    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getId() {
        return ID;
    }

    public void setId(String ID) {
        this.ID = ID;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getEmail() {
        return email;
    }
    public void setEmail(String email) {
        this.email = email;
    }

    public String getPhoneNumber() {
        return phoneNumber;
    }

    public void setPhoneNumber(String phoneNumber) {
        // research on how to ensure that phone numbers follow the KSA pattern
        this.phoneNumber = phoneNumber;
    }
    public String getAddress() {
        return address;
    }
    public void setAddress(String address) {
        this.address = address;
    }

    public Role getRole() {
        return role;
    }

    public void setRole(Role role) {
        this.role = role;
    }
    //======================= Methods =======================
    // Abstract Methods
    public abstract T login(List<T> list, String id, String password);

    public abstract String logout(T user);
}
```
