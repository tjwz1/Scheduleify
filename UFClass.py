class UFClass:
    def __init__(self, name, sections, description, credit_amount):
        self.name = name
        self.sections = sections
        self.description = description
        self.credit_amount = credit_amount

    def __repr__(self):
        return f"UFClass(name={self.name}, sections={len(self.sections)}, credits={self.credit_amount})"
