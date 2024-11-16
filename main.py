import requests
from UFClass import UFClass



def parse_data(class_name, data):

    if not data or not isinstance(data, list):
        raise ValueError(f"Invalid data format for class {class_name}: {data}")

    # Extract the first item from the list
    response_data = data[0]

    # Extract course details
    courses = response_data.get("COURSES", [])
    if not courses:
        raise ValueError(f"No course data found for {class_name}: {response_data}")

    course_data = courses[0]  # Assuming we're interested in the first course entry

    sections = course_data.get("sections", [])
    description = course_data.get("description", "No description available")
    credits = course_data.get("credits", 0)

    return UFClass(name=class_name, sections=sections, description=description, credit_amount=credits)


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
