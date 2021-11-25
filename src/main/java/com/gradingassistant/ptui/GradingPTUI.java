package com.gradingassistant.ptui;

import com.gradingassistant.model.*;

public class GradingPTUI implements Observer<GradingModel, Object>{
    public static Adjustment late_pss = new Adjustment("Late PSS Submission", -5);

    @Override
    public void update(GradingModel model, Object args) {

    }

    public static void main(String[] args) {

    }
}
