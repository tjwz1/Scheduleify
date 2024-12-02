import requests
from Schedule import *

def print_class_map(class_map):
    for class_name, uf_classes in class_map.items():
        print(f"{uf_classes}")
        for uf_class in uf_classes:
            print(f"\nClass Name: {uf_class.name}")
            print(f"Class Code: {uf_class.code}")
            print(f"Sections:")

            for section in uf_class.sections:
                print(f"  Section code: {section.code}")
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

        for each_course in courses:
            sections_data = each_course.get("sections", [])
            class_name = each_course.get('name', " ")
            class_code = each_course.get("code", " ")
            uf_class = Course(name=class_name, sections=[], code=class_code)

            for each_section in sections_data:
                credit = each_section.get("credits")
                meet_times = each_section.get("meetTimes", [])
                section_code = each_section.get("classNumber", 0)
                section = Section(credit=credit, code=section_code, course=class_code)

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

                #print(f"Raw Response for {course}:")
                #print(data)

            else:
                print(f"Error for {course}: {response.status_code}")
                print("Response text:", response.text)

        except requests.exceptions.RequestException as e:
            print(f"An error occurred for {course}: {e}")
    #best_schedule, best_num_classes, c = dp_schedule(classMap)
    print_class_map(classMap)
    greedy_schedule(classMap)
