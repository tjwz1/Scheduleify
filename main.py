import requests
import copy
from UFClass import *
from Schedule import *


def dp_schedule(class_map):
    best_schedule = Week()
    best_num_classes = 0
    schedule_states = [best_schedule.copy()]
    for class_name, uf_classes in class_map.items():
        for uf_class in uf_classes:
            for section in uf_class.sections:
                current_state = schedule_states[-1].copy()

                if current_state.add_class(section):
                    num_classes = sum([len(day.classes) for day in current_state.days.values()])

                    if num_classes > best_num_classes:
                        best_num_classes = num_classes
                        best_schedule = current_state.copy()
                    schedule_states.append(current_state)

                    current_state.remove_class(section)
                else:
                    continue
    return best_schedule, best_num_classes


def print_schedule(s):
    for day, day_obj in s.days.items():
        print(f"\nSchedule for {day}:")

        if day_obj.classes:
            for section in day_obj.classes:
                if section is None:
                    print("  No class scheduled for period")
                    print("\n")
                    continue
                # print(f"  Class Name: {section.name}")
                print(f"  Class Name: {section.code}")
                # print(f"  Description: {section.description}")
                print(f"  Section Credit: {section.credit}")

                # Print each meeting time for this section
                # for meeting in section.meetings:
                # print(f"    Days: {meeting['days']}")
                # print(f"    Start Period: {meeting['start_period']}")
                # print(f"    End Period: {meeting['end_period']}")


def print_class_map(class_map):
    for class_name, uf_classes in class_map.items():
        for uf_class in uf_classes:
            print(f"\nClass Name: {uf_class.name}")
            print(f"Description: {uf_class.description}")
            print(f"Sections:")

            for section in uf_class.sections:
                print(f"  Class code: {section.code}")
                print(f"  Class name: {section.name}")
                print(f"  Credits: {section.credit}")
                print(f"  Meeting Times:")

                for meeting in section.meetings:
                    print(f"    Days: {meeting['days']}")
                    print(f"    Start Period: {meeting['start_period']}")
                    print(f"    End Period: {meeting['end_period']}")


def parse_data(class_name, class_data):
    if not class_data or not isinstance(class_data, list):
        raise ValueError(f"Invalid data format for class {class_name}: {class_data}")

    # Iterate through all elements in class_data
    uf_classes = []
    for response_data in class_data:
        # Extract course details from each response_data
        courses = response_data.get("COURSES", [])
        if not courses:
            raise ValueError(f"No course data found for {class_name}: {response_data}")

        for c in courses:
            sections_data = c.get("sections", [])
            description = c.get("description", "No description available")
            class_name = c.get('name', " ")
            code = c.get("code", " ")
            uf_class = UFClass(name=class_name, sections=[], description=description)
            for s in sections_data:
                credit = s.get("credits")
                meet_times = s.get("meetTimes", [])
                section = Section(credit=credit, name=class_name, description=description, code=code)
                for meet_time in meet_times:
                    days = meet_time.get("meetDays", [])
                    start_period = meet_time.get("meetPeriodBegin", 0)
                    end_period = meet_time.get("meetPeriodEnd", 0)
                    section.add_meeting(start_period=start_period, end_period=end_period, days=days)
                uf_class.sections.append(section)
            uf_classes.append(uf_class)
    return uf_classes


# main method
if __name__ == "__main__":
    # taking input from students
    schedule = Week()
    classes = input(
        "Enter your preferred classes for semester by course code. Ex: COP3530, CEN3031, IDS2935. \n").split(
        ',')
    classes = [cls.strip() for cls in classes]

    classMap = {}

    # Base URL for the API
    base_url = "https://one.ufl.edu/apix/soc/schedule/"

    # Query Parameters
    params = {
        "category": "CWSP",
        "term": "2251",
        "course-code": "",  # Leave this empty initially
        "last-row": 0
    }

    for course in classes:
        # Update the 'course-code' parameter for each class
        params["course-code"] = course

        print(f"Sending request for course: {course}")
        try:
            response = requests.get(base_url, params=params)

            # Print the response status code
            print(f"Response Status Code: {response.status_code}")

            # Check if the request was successful
            if response.status_code == 200:
                data = response.json()

                new_class = parse_data(course, data)
                classMap[course] = new_class

                print(f"Raw Response for {course}:")
                print(data)

            else:
                print(f"Error for {course}: {response.status_code}")
                print("Response text:", response.text)

        except requests.exceptions.RequestException as e:
            print(f"An error occurred for {course}: {e}")
    best_schedule, best_num_classes = dp_schedule(classMap)
    # print_class_map(classMap)
    # schedule.greedy_schedule(classMap)
    print_schedule(best_schedule)
