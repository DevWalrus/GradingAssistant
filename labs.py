import json
import os
import re

import classes
import utils
from classes import Class


def grade_new(process: Class, f_dir: str):
    students = process.students
    with open(f_dir, 'w+') as fp:
        print("\n...GRADING THE PSS SUBMISSION PORTION...\n")
        utils.process_stus("absences during the pss", process, utils.absent_pss)

        print("\n...GRADING THE LABS SUBMISSION PORTION...\n")
        utils.process_stus("LATE submissions to the lab", process, utils.stu_late)
        utils.process_stus("MISSING submissions to the lab", process, utils.stu_missing)

        print("\n...GRADING THE STUDENTS...\n")
        for student in students.values():
            if not student.finalized:
                utils.grade(student, f_dir, process, fp)
        print("\n...FINISHED GRADING...\n...CLEANING UP...\n")
        os.remove(f_dir[:-3] + 'json')


def grade_resume(f_dir: str):
    with open(f_dir[:-3] + 'json', 'r') as fp2:
        data_str = fp2.read()
    fp2.close()
    process = Class.from_dict(json.loads(data_str))
    students = {}

    for student_id in process.students:
        print(process.students[student_id])

        stu = classes.Student(process.students[student_id]['first_name'],
                              process.students[student_id]['last_name'],
                              process.students[student_id]['id'],
                              classes.Assignment())
        for adj in process.students[student_id]['assignment']['adjustments']:
            stu.assignment.__add_adjustment__(adj['value'], adj['message'])
        for note in process.students[student_id]['assignment']['notes']:
            stu.assignment.__add_note__(note['message'])
        print(stu)

        if not process.students[student_id]['finalized']:
            students[student_id] = stu
    process.students = students

    with open(f_dir, 'a') as fp:

        print("\n...CONTINUING GRADING THE STUDENTS...\n")
        for student in process.students.values():
            if not student.finalized:
                utils.grade(student, f_dir, process, fp)
        print("\n...FINISHED GRADING...\n...CLEANING UP...\n")
        os.remove(f_dir[:-3] + 'json')
