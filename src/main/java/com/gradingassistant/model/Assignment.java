package com.gradingassistant.model;

import com.gradingassistant.ptui.GradingPTUI;

import java.util.List;

public class Assignment {

    private final int GRADE_MAX_DEFAULT = 100;

    private boolean submitted;
    private boolean pss_submitted;
    private int grade;
    private int grade_max;
    private List<Adjustment> adjustments;
    private List<Note> notes;

    public Assignment() {
        submitted = false;
        pss_submitted = false;
        grade = GRADE_MAX_DEFAULT;
        grade_max = GRADE_MAX_DEFAULT;
    }

    public void setExtraCredit(int value) {
        grade_max += value;
    }

    public void submit(String late) {
        switch (late.toLowerCase().charAt(0)) {
            case 'l' -> grade_max = GRADE_MAX_DEFAULT - 10;
            case 'r' -> grade_max = GRADE_MAX_DEFAULT - 20;
        }
        submitted = true;
    }

    public void submit_pss(String late) {
        if (late.toLowerCase().charAt(0) == 'l') {
            adjustments.add(GradingPTUI.late_pss);
        }
        submitted = true;
    }

    public void complete() {

        boolean m_late = false;
        boolean late = false;

        for (Adjustment adjustment : adjustments) {
            grade += adjustment.getValue();
        }

        if (grade > grade_max && grade_max != GRADE_MAX_DEFAULT) {
            grade = grade_max;
        } else if (grade > grade_max) {
            //TODO prompt the user asking them if they want to set an extra credit thing
        }
    }
}
