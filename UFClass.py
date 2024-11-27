class UFClass:
    def __init__(self, name, sections, description):
        self.name = name
        self.sections = sections
        self.description = description

    def __repr__(self):
        return f"UFClass(name={self.name}, sections={len(self.sections)})"


# find way to store sections, and for each day of the week


class Section:
    def __init__(self, credit, name, description, code):
        self.description = description
        self.credit = credit
        self.name = name
        self.meetings = []
        self.code = code

    def add_meeting(self, start_period, end_period, days):
        self.meetings.append({
            "start_period": start_period,
            "end_period": end_period,
            "days": days
        })
