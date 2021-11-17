import csv
import os
import glob
from os.path import exists

import labs
import singleSubmission as single
from classes import *

from typing import List

PATH = 'students/'
EXT = 'csv'

def pretty_print(classes:List[Class]) -> None:
    for item in classes:
        item.__to_string__()

def get_classes() -> List[Class]:
    os.chdir(PATH)
    results = glob.glob('*.{}'.format(EXT))
    classes = []
    for result in results:
        with open(result, "r", newline='') as file:
            reader = csv.reader(file)
            for line in reader:
                if line[0].strip() == 'info':
                    classes.append(Class(line[1].strip(),line[2].strip(),int(line[3]), dict()))
                else:
                    temp_student = Student(line[0].strip(), line[1].strip(), line[2].strip(), Assignment(False, False, 100, [], []))
                    classes[len(classes)-1].students[line[2].strip()] = temp_student
    return classes

def grade_class(process:Class):
    if input("Do you want to start grading a new assignment? ('y' or 'n') > ")[0].lower() == 'y':
        grade_new(process)
    else:
        grade_resume(process)

def grade_new(process:Class):
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    class_folder = os.path.join(THIS_FOLDER, "grades\{}_{}_{}\\".format(process.name, process.grader, process.year))
    if not exists(class_folder):
        os.mkdir(class_folder)
        print('Directory {} was created'.format(class_folder))
    f_name = input('What assignment are you grading? > ').lower()
    my_file = os.path.join(class_folder, "{}.txt".format(f_name))

    if exists(my_file):
        if input('WARNING: The file {} already exists, do you want to overwrite it? (\'y\' or \'n\') > '.format(my_file))[0].lower() != 'y':
            print("QUITTING: Have a great day!")
            return

    if f_name[0] == 'l':
        labs.grade_new(process, my_file)
    else:
        single.grade_new(process, my_file)

def grade_resume(process:Class):
    f_name = input('What assignment are you grading? > ').lower()
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    class_folder = os.path.join(THIS_FOLDER, "grades\{}_{}_{}\\".format(process.name, process.grader, process.year))
    my_file = os.path.join(class_folder, "{}.txt".format(f_name))

    if f_name[0] == 'l':
        labs.grade_resume(my_file)
    else:
        single.grade_resume(my_file)

def main():
    classes = get_classes()
    while True:
        class_list = 'Choices\n\t'
        for class_num in range(1, len(classes) + 1):
            class_list += ' {} : {}{}'.format(class_num, classes[class_num-1].__get_name__(), '' if class_num == len(classes) else '\n\t')
        print('Please select a class to use\n' + class_list)
        try:
            choice = int(input('> '))-1
            if 0 <= choice < len(classes):
                break
            else:
                print("You didn't select a class. Please try again.\n")
        except ValueError:
            print("You didn't select a class. Please try again.\n")
    grade_class(classes[choice])

if __name__ == '__main__':
    main()