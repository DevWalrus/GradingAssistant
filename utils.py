import os
import re
from typing import List, Tuple

from classes import Student

GITHUB_VALUE = 0

def set_github_value(value:int):
    global GITHUB_VALUE
    GITHUB_VALUE = value

def lst_tup_to_str(tuples: List[Tuple]) -> str:
    pretty = ""
    for t in tuples:
        for e in t:
            pretty += f"{e}, "
        pretty = pretty[:-2]
        pretty += "; "
    return pretty[:-2]


def absent_pss(stu: Student):
    stu.assignment.absent_pss()

def no_github(stu: Student):
    stu.assignment.no_github(GITHUB_VALUE)

def in_missing(stu: Student):
    stu.assignment.in_missing()

def stu_late(stu: Student):
    stu.assignment.set_late()

def stu_missing(stu: Student):
    stu.assignment.set_missing()

def process_stus(msg, process, action):
    while True:
        stu_str = input(f"Were there any {msg}? ([n]o or list student names Last, "
                        "First separated by a semicolon) > ")
        if stu_str.lower() == "n" or stu_str.lower() == "no" or stu_str == "":
            break
        stu_str = re.split("[ ]*;[ ]*", stu_str)
        stu_lst = list(map(lambda stu: re.split("[ ]*,[ ]*", stu), stu_str))
        all_stus = process.get_stus()
        bad_names = []

        for stu in stu_lst:
            stu = tuple(stu)
            if stu in all_stus:
                action(all_stus[stu])
            else:
                bad_names.append(stu)
        if len(bad_names) == 0:
            return
        else:
            print(f"The following names were not in the student list: {lst_tup_to_str(bad_names)}")

def grade(student: Student, f_dir: str, process, fp):
    str_stu = student.__get_name__()

    if not student.assignment.submitted:
        print('Skipping {} (They have no lab submission)'.format(str_stu))
        student.assignment.__add_adjustment__(-75, "No Lab Submission")
        student.__finalize__()
        with open(f_dir[:-3] + 'json', 'w') as fp2:
            fp2.write(process.to_json())
        fp.write(student.__to_string__())
        return
    else:

        print('Grading {}'.format(str_stu))
        done = False
        while not done:
            add = ""
            while True:
                try:
                    add = input("\tWould you like to add an adjustment or note? ([a]djustment, [n]ote, "
                                "[p]ause, [m]ove on, [h]elp) > ").lower()[0]
                    break
                except IndexError:
                    print('\tERROR: Invalid input, please try again')
                    continue
            if add == 'a':
                student.__add_adjustment__()
            elif add == 'n':
                student.__add_note__()
            elif add == 'p':
                exit(0)
            elif add == 'm':
                student.__finalize__()
                with open(f_dir[:-3] + 'json', 'w') as fp2:
                    fp2.write(process.to_json())
                fp.write(student.__to_string__())
                done = True
            else:
                print("\tHelp Menu:",
                      "\t\t[a]djustment : add an adjustment to the current student (an item that adjusts their grade)",
                      "\t\t[n]ote : add an note to the current student (an item that doesn't adjust their grade)",
                      "\t\t[p]ause : output some temp data and quit so I can Pause my grading",
                      "\t\t[m]ove on : move onto the next student for grading",
                      "\t\t[h]elp : print this help menu", sep='\n')