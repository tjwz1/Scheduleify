from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from UFClass import *
from Schedule import *
from Schedule import greedy_schedule

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:3000"}})


def dp_schedule(class_map):
    credit_limit = 18
    max_classes = 0
    best_num_credits = 0
    final_schedule = Week()
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
                        new_num_classes = sum(len(day.classes) for day in new_schedule.days.values())
                        if new_num_classes > max_classes or (
                                new_num_classes == max_classes and new_credits > best_num_credits):
                            max_classes = new_num_classes
                            final_schedule = new_schedule.copy()
                            best_num_credits = new_credits
                        if new_credits not in next_states:
                            next_states[new_credits] = (new_schedule, new_num_classes)
        schedule_states = next_states

    return final_schedule, best_num_credits


def parse_data(class_name, class_data):
    if not class_data or not isinstance(class_data, list):
        raise ValueError(f"Invalid data format for class {class_name}: {class_data}")

    uf_classes = []
    for response_data in class_data:
        courses = response_data.get("COURSES", [])
        if not courses:
            raise ValueError(f"No course data found for {class_name}: {response_data}")

        for c in courses:
            sections_data = c.get("sections", [])
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
        base_url = "https://one.ufl.edu/apix/soc/schedule/"
        params = {
            "category": "CWSP",
            "term": "2251",
            "course-code": "",
            "last-row": 0
        }

        # Fetch and parse data for each course
        for course in courses:
            params["course-code"] = course
            print(f"DEBUG: Sending request for course {course}")
            response = requests.get(base_url, params=params)

            if response.status_code == 200:
                data = response.json()
                parsed_classes = parse_data(course, data)
                class_map[course] = parsed_classes
                print(f"DEBUG: Parsed classes for {course}")
            else:
                print(f"ERROR: Failed to fetch data for {course}, Status Code: {response.status_code}")
                return jsonify({"status": "error", "message": f"Failed to fetch data for {course}"}), 500

        # Run DP and Greedy algorithms
        dp_week, dp_total_credits = dp_schedule(class_map)
        greedy_week, greedy_total_credits = greedy_schedule(class_map)

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
    for day_name, day_obj in week.days.items():
        schedule[day_name] = []
        for section in day_obj.classes:
            if section:
                for meeting in section.meetings:
                    schedule[day_name].append({
                        "class_name": section.code,
                        "start_period": meeting["start_period"],
                        "end_period": meeting["end_period"]
                    })
    return schedule


if __name__ == "__main__":
    app.run(debug=True)
