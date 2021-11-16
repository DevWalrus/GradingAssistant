from classes import Class, adjust, note

def grade_new(process:Class, f_dir:str):
    students = process.students
    with open(f_dir, 'w+') as fp:

        print("\n...GRADING THE PSS...\n")
        for student in students.values():
            while True:
                try:
                    student.assignment.pss_submitted = input("Did {} submit the post-pss? > ".format(student.__get_name__())).lower()[0] == "y"
                    break
                except IndexError:
                    print('ERROR: Invalid input, please try again')
                    continue

        print("\n...GRADING THE LABS...\n")
        for student in students.values():
            while True:
                try:
                    student.assignment.submitted = input("Did {} submit the lab? > ".format(student.__get_name__())).lower()[0] == "y"
                    break
                except IndexError:
                    print('ERROR: Invalid input, please try again')
                    continue

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
                        adjust(student)
                    elif add == 'n':
                        note(student)
                    elif add == 'p':
                        with open(f_dir[:-3]+'json', 'w+') as fp2:
                            fp2.write(''student.id+'\n')
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
            fp.write(student.__to_string__())

def grade_resume(process:Class, f_dir:str):
    """

    :param process:
    :param f_dir:
    :return:
    """