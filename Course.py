# A class for each UF Course
class Course:
    def __init__(self, name, sections, code):
        self.name = name # A name string
        self.sections = sections # A list of sections
        self.code = code # course code

    def __repr__(self):
        return f"Course(name={self.name}, sections={len(self.sections)})"

# A class for each section
class Section:
    def __init__(self, credit, code, course):
        self.credit = credit
        self.meetings = []
        self.code = code # section code
        self.course = course # course code

    def add_meeting(self, start_period, end_period, days):
        self.meetings.append({
            "start_period": start_period,
            "end_period": end_period,
            "days": days
        })
