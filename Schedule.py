import copy

from UFClass import *


class Day:
    def __init__(self):
        # self.classes = []
        self.classes = [None] * 14
        self.period_mapping = {
            "1": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5,
            "7": 6, "8": 7, "9": 8, "10": 9, "11": 10,
            "E1": 11, "E2": 12, "E3": 13
        }

    def add_class(self, section, start, end):
        start_index = self.period_mapping[start]
        end_index = self.period_mapping[end]
        for period in range(start_index, end_index + 1):
            if self.classes[period] is not None:
                return False
        # if not self.has_conflict(section):
        for period in range(start_index, end_index + 1):
            self.classes[period] = section
            # self.classes.append(section)
            # self.classes.sort(key=lambda x: x.meetings[0]['start_period'])
        return True
        # return False

    def remove_class(self, section):
        for i in range(len(self.classes)):
            if self.classes[i] == section:
                self.classes[i] = None  # Remove class from the period
        #print(f"Removed {section.name} from the schedule.")


class Week:
    def __init__(self):
        self.days = {day: Day() for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]}
        self.courses = set()
        self.day_mapping = {
            "M": "Monday",
            "T": "Tuesday",
            "W": "Wednesday",
            "R": "Thursday",
            "F": "Friday",
        }

    def add_class(self, section):
        if section.code in self.courses:
            #print(f"Course {section.code} is already scheduled.")
            return False
        for meeting in section.meetings:
            for day in meeting["days"]:
                full_day = self.day_mapping.get(day, day)
                if full_day not in self.days:
                    #print(f"Invalid meeting day for {section.code}")
                    return False
                if not self.days[full_day].add_class(section, meeting["start_period"], meeting["end_period"]):
                    return False
        self.courses.add(section.code)
        #print(f"{section.code} added to schedule")
        return True

    def remove_class(self, section):
        if section.code not in self.courses:
            return
        for meeting in section.meetings:
            for meet_day in meeting["days"]:
                full_day = self.day_mapping.get(meet_day, meet_day)
                self.days[full_day].remove_class(section)
        self.courses.remove(section.code)

    def copy(self):
        return copy.deepcopy(self)

    def greedy_schedule(self, class_map):
        total_credits = 0
        for class_name, uf_classes in class_map.items():
            if total_credits > 18:
                print("Max credit amount reached")
                break
            #print(f"\nProcessign class: {class_name}")
            for uf_class in uf_classes:
                print(f"  Scheduling: {uf_class.name} - {uf_class.description}")
                for section in uf_class.sections:
                    print(f"    Scheduling section for {uf_class.name}")
                    if self.add_class(section):
                        print(f"      {uf_class.name} successfully added")
                        total_credits += section.credit
                        break
                    else:
                        print(f"      {uf_class.name} unsuccessfully added")


def greedy_schedule(class_map):
    week = Week()
    total_credits = 0
    for class_name, uf_classes in class_map.items():
        if total_credits > 18:
            print("Max credit amount reached")
            break
        for uf_class in uf_classes:
            for section in uf_class.sections:
                if week.add_class(section):
                    total_credits += section.credit
                    break
    return week, total_credits
