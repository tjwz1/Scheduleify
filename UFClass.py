class UFClass:
    def __init__(
        self,
        code,
        courseId,
        name,
        description,
        prerequisites,
        termInd=None,
        openSeats=None,
        sections=None,
        lastControlNumber=None,
        retrievedRows=None,
        totalRows=None
    ):
        self.code = code
        self.courseId = courseId
        self.name = name
        self.description = description
        self.prerequisites = prerequisites
        self.termInd = termInd
        self.openSeats = openSeats
        self.sections = sections if sections else []
        self.lastControlNumber = lastControlNumber
        self.retrievedRows = retrievedRows
        self.totalRows = totalRows

    def __repr__(self):
        return f"UFClass(code={self.code}, name={self.name}, sections={len(self.sections)})"

class Section:
    def __init__(
        self,
        number,
        classNumber,
        gradBasis,
        acadCareer,
        display,
        credits,
        credits_min,
        credits_max,
        note,
        genEd,
        instructors,
        meetTimes,
        finalExam,
        dropaddDeadline,
        startDate,
        endDate,
        waitList,
    ):
        self.number = number
        self.classNumber = classNumber
        self.gradBasis = gradBasis
        self.acadCareer = acadCareer
        self.display = display
        self.credits = credits
        self.credits_min = credits_min
        self.credits_max = credits_max
        self.note = note
        self.genEd = genEd
        self.instructors = instructors
        self.meetTimes = meetTimes
        self.finalExam = finalExam
        self.dropaddDeadline = dropaddDeadline
        self.startDate = startDate
        self.endDate = endDate
        self.waitList = waitList

    def __repr__(self):
        return f"Section(number={self.number}, credits={self.credits})"

