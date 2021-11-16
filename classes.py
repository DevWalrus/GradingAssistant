from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass()
class Class:
    name : str
    grader : str
    year : int
    students : Dict

    def __to_string__(self):
        print('Class: {}'.format(self.name))
        print('\tFirst \tLast \tID')
        students = self.students
        for student in students:
            print(
                '\t{} \t{} \t{}'.format(students[student].firstName, students[student].lastName, students[student].id))

    def __get_name__(self):
        return '{} {} {}'.format(self.name, self.grader, str(self.year))

@dataclass()
class Adjustment:
    value: int
    message : str

    def __to_string__(self):
        return '{}% {}'.format(self.value, self.message)

@dataclass()
class Note:
    message : str

    def __to_string__(self):
        return 'NOTE: {}'.format(self.message)

@dataclass()
class Assignment:
    submitted : bool
    pss_submitted : bool
    grade : int
    adjustments : List[Adjustment]
    notes : List[Note]

    def __to_string__(self):
        result = 'Submission {}\n'.format('[X]' if self.submitted else '[ ]')
        result += 'PSS Submission {}\n'.format('[X]' if self.pss_submitted else '[ ]')
        result += 'Grade {}/100\n'.format(self.grade)
        for adjustment in list(self.adjustments):
            result += '{}\n'.format(adjustment.__to_string__())
        for note in list(self.notes):
            result += '{}\n'.format(note.__to_string__())
        return result + '\n'

    def __add_adjustment__(self, value, message):
        self.adjustments.append(Adjustment(value, message))
        self.grade += value

    def __add_note__(self, message):
        self.notes.append(Note(message))

@dataclass()
class Student:
    first_name:str
    last_name:str
    id:str
    assignment : Assignment

    def __to_string__(self):
        return '{}\t\t{}\t\t{}\n{}'.format(self.first_name, self.last_name, self.id, self.assignment.__to_string__())

    def __get_name__(self):
        return '{}\t\t{}\t\t{}'.format(self.first_name, self.last_name, self.id)

def adjust(student:Student):
    """

    :param student:
    :return:
    """
    while True:
        try:
            value = input("\tWhat how much is this item worth? > ")
            message = input("\tWhat message would you like to associate with this adjustment ('c' to cancel) > ")
            if value[0] == 'c' or message[0] == 'c':
                return
            break
        except IndexError:
            print('\tERROR: Invalid input, please try again')
            continue

    student.assignment.__add_adjustment__(int(value), message)

def note(student:Student):
    """

    :param student:
    :return:
    """
    while True:
        try:
            message = input("\tWhat message would you like to associate with this adjustment ('c' to cancel) > ")
            if message[0] == 'c':
                return
            break
        except IndexError:
            print('\tERROR: Invalid input, please try again')
            continue
    student.assignment.__add_note__(message)

def finalize(student:Student):
    if len(student.assignment.adjustments) == 0:
        student.assignment.__add_note__("Great Job!")