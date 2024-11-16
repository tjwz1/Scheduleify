class UFClass:
    def __init__(self, name, sections, description, credit_amount):
        """
        Initialize a UFClass object.
        :param name: str, class name (e.g., "STA3100")
        :param sections: list of dict, each section includes time and location
        :param description: str, description of the class
        :param credit_amount: float, number of credits
        """
        self.name = name
        self.sections = sections  # List of section dictionaries
        self.description = description
        self.credit_amount = credit_amount

    def __repr__(self):
        return f"UFClass(name={self.name}, sections={len(self.sections)}, credits={self.credit_amount})"
