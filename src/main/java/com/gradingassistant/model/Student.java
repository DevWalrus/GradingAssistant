package com.gradingassistant.model;

import java.util.ArrayList;
import java.util.List;

public class Student {

    private final String firstName;
    private final String lastName;
    private final String id;
    private final List<Assignment> assignments;

    public Student (String firstName, String lastName, String id) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.id = id;
        assignments = new ArrayList<>();
    }


    @Override
    public String toString() {
        return String.format("%s\t\t%s\t\t%s", firstName, lastName, id);
    }
}
