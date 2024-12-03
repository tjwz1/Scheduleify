from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from Schedule import *

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:3000"}})

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


@app.route('/generate_schedules', methods=['POST'])
def generate_schedules():
    try:
        # Parse input JSON
        data = request.json
        print(f"DEBUG: Received data: {data}")

        if not data or "courses" not in data:
            return jsonify({"status": "error", "message": "Invalid input data"}), 400

        courses = data["courses"]
        print(f"DEBUG: Courses to fetch: {courses}")

        class_map = {}

        # Base URL for the API
        base_url = "https://one.ufl.edu/apix/soc/schedule/"

        # Query Parameters
        params = {
            "category": "CWSP",
            "term": "2251",
            "course-code": "", # Leave this empty initially
            "last-row": 0
        }

        # Fetch and parse data for each course
        for course in courses:
            params["course-code"] = course
            print(f"DEBUG: Sending request for course {course}")

            response = requests.get(base_url, params=params)
            # Print the response status code
            print(f"Response Status Code: {response.status_code}")

            if response.status_code == 200:
                data = response.json()

                parsed_classes = parse_data(course, data)
                class_map[course] = parsed_classes
                print(f"DEBUG: Parsed classes for {course}")

            else:
                print(f"ERROR: Failed to fetch data for {course}, Status Code: {response.status_code}")
                return jsonify({"status": "error", "message": f"Failed to fetch data for {course}"}), 500

        print_class_map(class_map)

        # Run DP and Greedy algorithms
        greedy_week, greedy_total_credits = greedy_schedule(class_map)
        dp_week, dp_total_credits = dp_schedule(class_map)

        # Format schedules into JSON
        dp_schedule_data = format_week(dp_week)
        greedy_schedule_data = format_week(greedy_week)

        # Return the schedules
        return jsonify({
            "status": "success",
            "dp_schedule": dp_schedule_data,
            "dp_credits": dp_total_credits,
            "greedy_schedule": greedy_schedule_data,
            "greedy_credits": greedy_total_credits
        })
    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


def format_week(week):
    schedule = {}
    # iterate through each day of the week
    for day_name, day_obj in week.days.items():
        schedule[day_name] = []
        # iterate through each class section on the current day
        for period, section in day_obj.periods.items():
            schedule[day_name].append({
                "class_name": section.course,
                "section_code": section.code,
                "start_period": period
            })
    return schedule

if __name__ == "__main__":
    app.run(debug=True)
