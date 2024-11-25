import requests
from UFClass import UFClass, Section


def parse_data(class_name, data):
    def parse_data(class_name, data):
        if not data or not isinstance(data, list):
            raise ValueError(f"Invalid data format for class {class_name}: {data}")

        # Extract the first course entry
        response_data = data[0]
        courses = response_data.get("COURSES", [])
        if not courses:
            raise ValueError(f"No course data found for {class_name}: {response_data}")

        # Extract course details
        course_data = courses[0]
        sections_data = course_data.get("sections", [])

        # Parse sections
        sections = []
        for section_data in sections_data:
            meetTimes = section_data.get("meetTimes", [])
            instructors = [inst["name"] for inst in section_data.get("instructors", [])]
            waitList = section_data.get("waitList", {})
            sections.append(
                Section(
                    number=section_data["number"],
                    classNumber=section_data["classNumber"],
                    gradBasis=section_data["gradBasis"],
                    acadCareer=section_data["acadCareer"],
                    display=section_data["display"],
                    credits=section_data["credits"],
                    credits_min=section_data["credits_min"],
                    credits_max=section_data["credits_max"],
                    note=section_data.get("note", ""),
                    genEd=section_data.get("genEd", []),
                    instructors=instructors,
                    meetTimes=meetTimes,
                    finalExam=section_data.get("finalExam", ""),
                    dropaddDeadline=section_data.get("dropaddDeadline", ""),
                    startDate=section_data.get("startDate", ""),
                    endDate=section_data.get("endDate", ""),
                    waitList=waitList,
                )
            )

        # Create UFClass instance
        return UFClass(
            code=course_data["code"],
            courseId=course_data["courseId"],
            name=course_data["name"],
            description=course_data["description"],
            prerequisites=course_data.get("prerequisites", ""),
            termInd=course_data.get("termInd", ""),
            openSeats=course_data.get("openSeats"),
            sections=sections,
            lastControlNumber=response_data.get("LASTCONTROLNUMBER"),
            retrievedRows=response_data.get("RETRIEVEDROWS"),
            totalRows=response_data.get("TOTALROWS"),
        )


#main
if(__name__ == "__main__"):

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

    course_list = ["STA3100", "COP3502C", "STA4210", "ENC1102"]


    for class_name in course_list:
        # Update the 'course-code' parameter for each class
        params["course-code"] = class_name

        print(f"Sending request for course: {class_name}")
        try:
            # Send GET Request
            response = requests.get(base_url, params=params)



            # Print the response status code
            print(f"Response Status Code: {response.status_code}")

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the JSON response
                data = response.json()

                uf_class = parse_data(class_name, data)
                classMap[class_name] = uf_class

                # Print the raw response to debug
                print(f"Raw Response for {class_name}:")
                print(data)

            else:
                print(f"Error for {class_name}: {response.status_code}")
                print("Response text:", response.text)  # Print details for debugging

        except requests.exceptions.RequestException as e:
            print(f"An error occurred for {class_name}: {e}")

