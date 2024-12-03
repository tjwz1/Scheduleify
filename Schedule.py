import copy
from Course import *


class Day:
    def __init__(self):
        self.periods = {}

    # add a class to a specific period of the day
    def add_class(self, section, start_period, end_period):
        self.periods[start_period] = section
        self.periods[end_period] = section
        return True

    # delete all occurence of a section in the day
    def remove_class(self, section):
        for period in self.periods:
            if self.periods[period] == section:
                del self.periods[period] # Remove class from the period

        return True

    # check if the current period is occupied by a section
    def is_period_occupied(self, start_period, end_period):
        if start_period in self.periods:
            return True
        if end_period in self.periods:
            return True
        return False

class Week:
    def __init__(self):
        self.days = {day: Day() for day in ["M", "T", "W", "R", "F"]}
        self.courses = set()

    # Add one section to the weekly schedule
    def add_class(self, section):
        # check if the current section is already scheduled
        if section.course in self.courses:
            print(f"Course {section.course} is already scheduled.")
            return False
        
        # check if the current section has conflict periods with another section
        for meeting in section.meetings:
            for day in meeting["days"]:
                if self.days[day].is_period_occupied(meeting['start_period'], meeting['end_period']):
                    return False

        # adds each meeting to its corresponding day of the week
        for meeting in section.meetings:
            for day in meeting["days"]:

                if day not in self.days:
                    print(f"Invalid meeting day for {section.course}, section code: {section.code}")
                    return False
                
                self.days[day].add_class(section, meeting["start_period"], meeting["end_period"])
        
        self.courses.add(section.course)
        return True

    def remove_class(self, section):
        if section.course not in self.courses:
            return True
        for meeting in section.meetings:
            for meet_day in meeting["days"]:
                self.days[meet_day].remove_class(section)
        self.courses.remove(section.course)
        return True

    def print_schedule(self):
        for day, day_obj in self.days.items():
            print(f"\nSchedule for {day}:")
            for period, section in day_obj.periods.items():
                print(f"{section.course}, section number: {section.code} is scheduled for period {period}")

    def copy(self):
        return copy.deepcopy(self)

def greedy_schedule(class_map):
    greedy_week = Week()
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
                if greedy_week.add_class(section):
                    total_credits += section.credit
                    break
                else:
                    print(f"{uf_class.name} unsuccessfully added")
    greedy_week.print_schedule()
    return greedy_week, total_credits

def dp_schedule(class_map):
    credit_limit = 18
    max_classes = 0
    best_num_credits = 0
    dp_week = Week()
    schedule_states = {0: (Week(), 0)}

    for class_name, uf_classes in class_map.items():
        next_states = {}

        for current_credits, (current_schedule, current_num_classes) in schedule_states.items():
            for uf_class in uf_classes:
                for section in uf_class.sections:
                    new_schedule = current_schedule.copy()

                    if new_schedule.add_class(section):
                        new_credits = current_credits + section.credit

                        if new_credits > credit_limit:
                            new_schedule.remove_class(section)
                            continue
                        new_num_classes = sum(len(day.periods) for day in new_schedule.days.values())
                        if new_num_classes > max_classes or (
                                new_num_classes == max_classes and new_credits > best_num_credits):
                            max_classes = new_num_classes
                            dp_week = new_schedule.copy()
                            best_num_credits = new_credits
                        if new_credits not in next_states:
                            next_states[new_credits] = (new_schedule, new_num_classes)
        schedule_states = next_states

    dp_week.print_schedule()

    return dp_week, best_num_credits
