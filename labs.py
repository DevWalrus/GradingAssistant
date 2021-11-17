import json
import os

from classes import Class

def grade_new(process:Class, f_dir:str):
    students = process.students
    with open(f_dir, 'w+') as fp:

        print("\n...GRADING THE PSS SUBMISSION PORTION...\n")
        for student in students.values():
            while True:
                try:
                    sub = input("Did {} submit the post-pss? > ".format(student.__get_name__())).lower()[0]
                    student.assignment.pss_submitted = sub == "y"
                    if sub == "l":
                        student.assignment.pss_submitted = True
                        student.assignment.__add_adjustment__(-5, "Late PostPSS Submission")
                    break
                except IndexError:
                    print('ERROR: Invalid input, please try again')
                    continue
        while True:
            edit = input("Did you want to edit any of those submissions? ([y]es, [p]rint class, [n]o) > ").lower()[0]
            if edit == "y":
                student_edit = input("Enter the user id of the user you want to edit > ")
                student = process.students[student_edit]
                while True:
                    try:
                        sub = input("Did {} submit the post-pss? > ".format(student.__get_name__())).lower()[0]
                        student.assignment.pss_submitted = sub == "y"
                        if sub == "l":
                            student.assignment.pss_submitted = True
                            student.assignment.__add_adjustment__(-5, "Late PostPSS Submission")
                        break
                    except IndexError:
                        print('ERROR: Invalid input, please try again')
                        continue
                continue
            if edit == "p":
                process.__print__()
                continue
            break

        print("\n...GRADING THE LABS SUBMISSION PORTION...\n")
        for student in students.values():
            while True:
                try:
                    sub = input("Did {} submit the post-pss? ([y]es, [l]ate, [r]eally late) > ".format(student.__get_name__())).lower()[0]
                    student.assignment.submitted = sub == "y"
                    if sub == "l":
                        student.assignment.submitted = True
                        student.assignment.__add_adjustment__(-10, "Late Lab Submission")
                    elif sub == "r":
                        student.assignment.submitted = True
                        student.assignment.__add_adjustment__(-20, "Late Lab Submission")
                    break
                except IndexError:
                    print('ERROR: Invalid input, please try again')
                    continue
        while True:
            edit = input("Did you want to edit any of those submissions? ([y]es, [p]rint class, [n]o) > ").lower()[0]
            if edit == "y":
                student_edit = input("Enter the user id of the user you want to edit > ")
                student = process.students[student_edit]
                while True:
                    try:
                        sub = input("Did {} submit the post-pss? ([y]es, [l]ate, [r]eally late) > ".format(
                            student.__get_name__())).lower()[0]
                        student.assignment.submitted = sub == "y"
                        if sub == "l":
                            student.assignment.submitted = True
                            student.assignment.__add_adjustment__(-10, "Late Lab Submission")
                        elif sub == "r":
                            student.assignment.submitted = True
                            student.assignment.__add_adjustment__(-20, "Late Lab Submission")
                        break
                    except IndexError:
                        print('ERROR: Invalid input, please try again')
                        continue
                continue
            if edit == "p":
                process.__print__()
                continue
            break

        print("\n...GRADING THE STUDENTS...\n")
        for student in students.values():
            str_stu = student.__get_name__()
            if not student.assignment.pss_submitted:
                student.assignment.__add_adjustment__(-15, "No Post-PSS Submission")

            if not student.assignment.submitted:
                print('Skipping {} (They have no lab submission)'.format(str_stu))
                student.assignment.__add_adjustment__(-75, "No Lab Submission")
            else:
                print('Grading {}'.format(str_stu))
                done = False
                while not done:
                    while True:
                        try:
                            add = input("\tWould you like to add an adjustment or note? ('a', 'n', 'p', or 'q') > ").lower()[0]
                            break
                        except IndexError:
                            print('\tERROR: Invalid input, please try again')
                            continue
                    if add == 'a':
                        student.__add_adjustment__()
                    elif add == 'n':
                        student.__add_note__()
                    elif add == 'p':
                        with open(f_dir[:-3]+'json', 'w+') as fp2:
                            fp2.write(process.to_json())
                        return
                    elif add == 'q':
                        done = True
                    else:
                        print("\tHelp Menu:",
                              "\t\t[a]djustment : add an adjustment to the current student (an item that adjusts their grade)",
                              "\t\t[n]ote : add an note to the current student (an item that doesn't adjust their grade)",
                              "\t\t[p]ause : output some temp data and quit so I can Pause my grading",
                              "\t\t[q]uit : move onto the next student for grading",
                              "\t\t[h]elp : print this help menu", sep='\n')
            student.__finalize__()
            fp.write(student.__to_string__())

def grade_resume(f_dir:str):
    with open(f_dir[:-3] + 'json', 'r') as fp2:
        for line in fp2:
            data_str = line
    process = Class.from_dict(json.loads(data_str))
    students = []
    for student_id in process.students:
        if not process.students[student_id].finalized:
            students.append(process.students[student_id])

    with open(f_dir, 'a') as fp:

        print("\n...CONTINUING GRADING THE STUDENTS...\n")
        for student in students:
            str_stu = student.__get_name__()
            if not student.assignment.pss_submitted:
                student.assignment.__add_adjustment__(-15, "No Post-PSS Submission")

            if not student.assignment.submitted:
                print('Skipping {} (They have no lab submission)'.format(str_stu))
                student.assignment.__add_adjustment__(-75, "No Lab Submission")
            else:
                print('Grading {}'.format(str_stu))
                done = False
                while not done:
                    while True:
                        try:
                            add = \
                            input("\tWould you like to add an adjustment or note? ('a', 'n', 'p', or 'q') > ").lower()[
                                0]
                            break
                        except IndexError:
                            print('\tERROR: Invalid input, please try again')
                            continue
                    if add == 'a':
                        student.__add_adjustment__()
                    elif add == 'n':
                        student.__add_note__()
                    elif add == 'p':
                        with open(f_dir[:-3] + 'json', 'w+') as fp2:
                            fp2.write(
                                "{" + '"last_processed": "{}", "data": {}'.format(student.id, process.to_json()) + "}")
                        return
                    elif add == 'q':
                        done = True
                    else:
                        print("\tHelp Menu:",
                              "\t\t[a]djustment : add an adjustment to the current student (an item that adjusts their grade)",
                              "\t\t[n]ote : add an note to the current student (an item that doesn't adjust their grade)",
                              "\t\t[p]ause : output some temp data and quit so I can Pause my grading",
                              "\t\t[q]uit : move onto the next student for grading",
                              "\t\t[h]elp : print this help menu", sep='\n')
            student.__finalize__()
            fp.write(student.__to_string__())
        print("\n...FINISHED GRADING...\n...CLEANING UP...\n")
        os.remove(f_dir[:-3] + 'json')