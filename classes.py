from dataclasses import dataclass
from typing import Dict, List, re, Tuple
from dataclasses_json import dataclass_json


@dataclass_json()
@dataclass()
class Adjustment:
    value: int
    message: str

    def __to_string__(self):
        return '{}% {}'.format(self.value, self.message)

    def __eq__(self, other):
        return self.message == other.message and self.value == other.value


@dataclass_json()
@dataclass()
class Note:
    message: str

    def __to_string__(self):
        return 'NOTE: {}'.format(self.message)


@dataclass_json()
@dataclass()
class Assignment:
    submitted: bool
    grade: int
    late_flag: bool
    adjustments: list
    notes: list

    def __init__(self):
        self.submitted = True
        self.grade = 100
        self.late_flag = False
        self.adjustments = []
        self.notes = []

    def setup(self, **kwargs):
        self.__init__()
        self.submitted = kwargs["submitted"]
        self.grade = kwargs["grade"]
        self.late_flag = kwargs["late_flag"]



    def __to_string__(self):
        result = 'Submission {}\n'.format('[X]' if self.submitted else '[ ]')
        result += 'Grade {}/100\n'.format(self.grade)
        for adjustment in list(self.adjustments):
            result += '{}\n'.format(adjustment.__to_string__())
        for note in list(self.notes):
            result += '{}\n'.format(note.__to_string__())
        return result + '\n'

    def __add_adjustment__(self, value, message):
        self.adjustments.append(Adjustment(value, message))

    def __add_note__(self, message):
        self.notes.append(Note(message))

    def finalize(self):
        for adjustment in self.adjustments:
            self.grade += adjustment.value
        if self.late_flag:
            self.grade *= 0.8

    def set_late(self):
        self.late_flag = True

    def set_missing(self):
        self.submitted = False

    def absent_pss(self):
        self.__add_adjustment__(-15, "Absent for PSS")

    def in_missing(self):
        self.__add_adjustment__(-10, "No In-Lab")

    def no_github(self, value):
        self.__add_adjustment__(value, "No Github Submission")


@dataclass_json()
@dataclass()
class Student:
    first_name: str
    last_name: str
    id: str
    assignment: Assignment
    finalized: bool

    def __init__(self, first_name, last_name, id, assignment):
        self.first_name = first_name
        self.last_name = last_name
        self.id = id
        self.assignment = assignment
        self.finalized = False

    def __to_string__(self):
        return '{}\t\t{}\t\t{}\n{}'.format(self.first_name, self.last_name, self.id, self.assignment.__to_string__())

    def __get_name__(self):
        return '{}\t\t{}\t\t{}'.format(self.first_name, self.last_name, self.id)

    def __finalize__(self):
        self.assignment.finalize()
        if self.assignment.grade == 100:
            self.assignment.__add_note__("Great Job!")
        self.finalized = True

    def __add_note__(self):
        message = ""
        while True:
            try:
                message = input("\tWhat message would you like to associate with this adjustment ('c' to cancel) > ")
                if message[0] == 'c':
                    return
                break
            except IndexError:
                print('\tERROR: Invalid input, please try again')
                continue
        self.assignment.__add_note__(message)

    def __add_adjustment__(self):
        value = ""
        message = ""
        while True:
            try:
                value = input("\tHow much is this item worth? > ")
                if value[0] == 'c':
                    return
                message = input("\tWhat message would you like to associate with this adjustment ('c' to cancel) > ")
                if value[0] == 'c' or message[0] == 'c':
                    return
                break
            except IndexError:
                print('\tERROR: Invalid input, please try again')
                continue
        self.assignment.__add_adjustment__(int(value), message)


@dataclass_json()
@dataclass()
class Class:
    name: str
    grader: str
    year: int
    students: dict

    def __print__(self):
        print('Class: {}'.format(self.name))
        print('\tFirst \tLast \tID')
        students = self.students
        for student in students:
            print('\t{} \t{} \t{}'.format(students[student].first_name, students[student].last_name,
                                          students[student].id))

    def __get_name__(self):
        return '{} {} {}'.format(self.name, self.grader, str(self.year))

    def get_stus(self) -> Dict[Tuple[str, str], Student]:
        return dict(map(lambda stu: ((stu.last_name, stu.first_name), stu), self.students.values()))
