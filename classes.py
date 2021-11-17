from dataclasses import dataclass
from typing import Dict, List
from dataclasses_json import dataclass_json

@dataclass_json()
@dataclass()
class Adjustment:
    value: int
    message : str

    def __to_string__(self):
        return '{}% {}'.format(self.value, self.message)

    def __eq__(self, other):
        return self.message == other.message and self.value == other.value

@dataclass_json()
@dataclass()
class Note:
    message : str

    def __to_string__(self):
        return 'NOTE: {}'.format(self.message)

@dataclass_json()
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

    def __add_note__(self, message):
        self.notes.append(Note(message))

    def finalize(self):
        for adjustment in self.adjustments:
            if adjustment.__eq__(Adjustment(-10, "Late Lab Submission")):
                print("-10 found")
                if self.grade + 10 <= 90:
                    print("-10 removed")

                    continue
            elif adjustment.__eq__(Adjustment(-20, "Late Lab Submission")):
                print("-20 found")

                if self.grade + 20 <= 80:
                    print("-20 removed")

                    continue
            self.grade += adjustment.value #gotta move this up or run it first, the things are being found but not removed cuz its happening before the other adjustments (-50)

@dataclass_json()
@dataclass()
class Student:
    first_name : str
    last_name : str
    id : str
    assignment : Assignment
    finalized : bool = False

    def __to_string__(self):
        return '{}\t\t{}\t\t{}\n{}'.format(self.first_name, self.last_name, self.id, self.assignment.__to_string__())

    def __get_name__(self):
        return '{}\t\t{}\t\t{}'.format(self.first_name, self.last_name, self.id)

    def __finalize__(self):
        self.assignment.finalize()
        if len(self.assignment.adjustments) == 0:
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
                value = input("\tWhat how much is this item worth? > ")
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
    name : str
    grader : str
    year : int
    students : Dict[str, Student]

    def __print__(self):
        print('Class: {}'.format(self.name))
        print('\tFirst \tLast \tID')
        students = self.students
        for student in students:
            print('\t{} \t{} \t{}'.format(students[student].first_name, students[student].last_name, students[student].id))

    def __get_name__(self):
        return '{} {} {}'.format(self.name, self.grader, str(self.year))