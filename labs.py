import json
import os
import re

import classes
import utils
from classes import Class


def grade_new(process: Class, f_dir: str):
    students = process.students
    with open(f_dir, 'w+') as fp:
        print("\n...GRADING THE GITHUB PORTION...\n")
        if input("Was there a GitHub portion to this assignment? ([y]es or [n]o) > ").lower()[0] == "y":
            while True:
                try:
                    utils.set_github_value(int(input("How much is this item worth? > ")))
                    break
                except ValueError:
                    print('\tERROR: Invalid input, please try again')
                    continue
            utils.process_stus("MISSING GitHub submissions", process, utils.no_github)
        with open(f_dir[:-3] + "json", 'w+') as fp2:
            fp2.write(process.to_json())

        print("\n...GRADING THE PSS SUBMISSION PORTION...\n")
        utils.process_stus("ABSENCES during the PSS", process, utils.absent_pss)
        with open(f_dir[:-3] + "json", 'w+') as fp2:
            fp2.write(process.to_json())

        print("\n...GRADING THE IN-LAB PORTION...\n")
        utils.process_stus("MISSING submissions to the IN_LAB", process, utils.absent_pss)
        with open(f_dir[:-3] + "json", 'w+') as fp2:
            fp2.write(process.to_json())

        print("\n...GRADING THE LAB SUBMISSION PORTION...\n")
        utils.process_stus("LATE submissions to the LAB", process, utils.stu_late)
        with open(f_dir[:-3] + "json", 'w+') as fp2:
            fp2.write(process.to_json())

        utils.process_stus("MISSING submissions to the LAB", process, utils.stu_missing)
        with open(f_dir[:-3] + "json", 'w+') as fp2:
            fp2.write(process.to_json())

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
        stu_dict = process.students[student_id]
        assign_dict = stu_dict['assignment']
        assign = classes.Assignment()
        stu = classes.Student(stu_dict['first_name'],
                              stu_dict['last_name'],
                              stu_dict['id'],
                              assign)
        assign.setup(submitted=assign_dict['submitted'],
                     grade=assign_dict['grade'],
                     late_flag=assign_dict['late_flag'])
        for adj in assign_dict['adjustments']:
            stu.assignment.__add_adjustment__(adj['value'], adj['message'])
        for note in assign_dict['notes']:
            stu.assignment.__add_note__(note['message'])

        if not process.students[student_id]['finalized']:
            students[student_id] = stu
    process.students = students

    with open(f_dir, 'a') as fp:

        print("\n...CONTINUING GRADING THE STUDENTS...\n")
        for student in process.students.values():
            if not student.finalized: # "Sanity" check
                utils.grade(student, f_dir, process, fp)
        print("\n...FINISHED GRADING...\n...CLEANING UP...\n")
        os.remove(f_dir[:-3] + 'json')
