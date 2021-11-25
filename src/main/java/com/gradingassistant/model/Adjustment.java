package com.gradingassistant.model;

public class Adjustment extends Note {

    private final int value;

    public Adjustment(String message, int value) {
        super(message);
        this.value = value;
    }

    public int getValue() {
        return value;
    }

    @Override
    public String toString() {
        return String.format("%s%% %s", value, message);
    }
}
