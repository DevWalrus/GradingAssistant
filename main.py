import csv
import os
import glob
from os.path import exists

import labs
from classes import *

from typing import List

PATH = 'students/'
EXT = 'csv'

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

def pretty_print(classes: List[Class]) -> None:
    """
    Calls the to string method for every individual class.
    :param classes: A list of classes
    :return: Nothing
    """
    for item in classes:
        item.__print__()


def get_classes() -> List[Class]:
    """
    Looks for a csv file in a directory called students.
    :return: A list of class objects
    """
    os.chdir(PATH)
    results = glob.glob('*.{}'.format(EXT))
    print(results)
    classes = []
    for result in results:
        with open(result, "r", newline='') as file:
            reader = csv.reader(file)
            for line in reader:
                if line[0].strip() == 'info':
                    classes.append(Class(line[1].strip(), line[2].strip(), int(line[3]), dict()))
                else:
                    temp_student = Student(line[1].strip(), line[0].strip(), line[2].strip(),
                                           Assignment())
                    classes[-1].students[line[2].strip()] = temp_student
    return classes


def grade_class(process: Class) -> None:
    """

    :param process:
    :return:
    """
    new = input("Do you want to start grading a new assignment? ([y]es or [n]o) > ")[0].lower()
    f_name = input('What assignment are you grading? > ').lower()
    if new == 'y':
        grade_new(process, f_name)
    else:
        grade_resume(process, f_name)


def grade_new(process: Class, f_name: str):
    """

    :param process:
    :param f_name:
    :return:
    """
    class_folder = os.path.join(THIS_FOLDER, "grades", f"{process.name}_{process.grader}_{process.year}")
    if not exists(class_folder):
        os.mkdir(class_folder)
        print('Directory {} was created'.format(class_folder))

    if exists(f_name):
        if input('WARNING: The file {} already exists, do you want to overwrite it? ([y]es or [n]o) > '.format(
                f_name))[0].lower() != 'y':
            print("QUITTING: Have a great day!")
            return

    with open(f_name[:-3] + "json", 'w+') as fp2:
        fp2.write(process.to_json())
    labs.grade_new(process, f_name)


def grade_resume(process: Class, f_name: str):
    my_file = os.path.join(THIS_FOLDER, "grades", f"{process.name}_{process.grader}_{process.year}", f"{f_name}.txt")
    if not exists(my_file):
        if input(f'WARNING: The file {my_file} does not exist, do you want to begin grading it? ([y]es or [n]o) > ')[
            0].lower() == 'y':
            grade_new(process, my_file)
        else:
            print("QUITTING: Have a great day!")
            exit()
    labs.grade_resume(my_file)


def main():
    classes = get_classes()
    while True:
        class_list = 'Choices\n\t'
        for class_num in range(1, len(classes) + 1):
            class_list += ' {} : {}{}'.format(class_num, classes[class_num - 1].__get_name__(),
                                              '' if class_num == len(classes) else '\n\t')
        print('Please select a class to use\n' + class_list)
        try:
            choice = int(input('> ')) - 1
            if 0 <= choice < len(classes):
                break
            else:
                print("You didn't select a class. Please try again.\n")
        except ValueError:
            print("You didn't select a class. Please try again.\n")
    grade_class(classes[choice])


if __name__ == '__main__':
    main()
