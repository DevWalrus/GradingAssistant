package com.gradingassistant.model;

public class Note {
    protected final String message;

    public Note(String message) {
        this.message = message;
    }

    @Override
    public String toString() {
        return String.format("NOTE: %s", message);
    }
}
