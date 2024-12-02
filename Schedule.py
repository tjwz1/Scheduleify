import copy
from Course import *


class Day:
    def __init__(self):
        self.classes = [None] * 14

    # add a class to a specific period of the day
    def add_class(self, section, start_period, end_period):
        for period in range(start_period - 1, end_period):
            self.classes[period] = section
        return True

    # delete all occurence of a section in the day
    def remove_class(self, section):
        for i in range(len(self.classes)):
            if self.classes[i] == section:
                self.classes[i] = None  # Remove class from the period
        return True

    # check if the current period is occupied by a section
    def is_period_occupied(self, start_period, end_period):
        for period in range(start_period - 1, end_period):
            if self.classes[period] is not None:
                return True
        return False


class Week:
    def __init__(self):
        self.days = {day: Day() for day in ["M", "T", "W", "R", "F"]}
        self.courses = set()

    # Add one section to the weekly schedule
    def add_class(self, section):
        # check if the current section is already scheduled
        if section in self.courses:
            print(f"Course {section.code} is already scheduled.")
            return False
        
        # check if the current section has conflict periods with another section
        for meeting in section.meetings:
            for day in meeting["days"]:
                if self.days[day].is_period_occupied(int(meeting['start_period']), int(meeting['end_period'])):
                    return False

        # adds each meeting to its corresponding day of the week
        for meeting in section.meetings:
            for day in meeting["days"]:

                if day not in self.days:
                    print(f"Invalid meeting day for {section.course}, section code: {section.code}")
                    return False
                
                self.days[day].add_class(section, int(meeting["start_period"]), int(meeting["end_period"]))
        
        self.courses.add(section)
        print(f"{section.course}, section number: {section.code} successfully added to schedule")
        return True

    def remove_class(self, section):
        if section not in self.courses:
            return True
        for meeting in section.meetings:
            for meet_day in meeting["days"]:
                self.days[meet_day].remove_class(section)
        self.courses.remove(section)
        return True

    def copy(self):
        return copy.deepcopy(self)

    def greedy_schedule(self, class_map):
        total_credits = 0
        for class_name, uf_classes in class_map.items():
            if total_credits > 18:
                print("Max credit amount reached")
                break
            print(f"\nProcessing class: {class_name}")
            for uf_class in uf_classes:
                print(f"Scheduling: {uf_class.name}")
                for section in uf_class.sections:
                    print(f"Scheduling section for {uf_class.name}")
                    if self.add_class(section):
                        total_credits += section.credit
                        break
                    else:
                        print(f"{uf_class.name} unsuccessfully added")