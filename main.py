import requests

# Base URL for the API
base_url = "https://one.ufl.edu/apix/soc/schedule/"

# Query Parameters
params = {
    "category": "CWSP",
    "term": "2251",
    "course-code": "",  # Leave this empty initially
    "last-row": 0
}

course_list = ["STA3100", "COP3502C", "STA4210", "ENC1102"]  # Avoid using `list` as it shadows the built-in list type

for class_name in course_list:
    # Update the 'course-code' parameter for each class
    params["course-code"] = class_name

    # Send GET Request
    try:
        response = requests.get(base_url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Display the response (or process it further)
            print(f"Data for {class_name}:")
            print(data)
        else:
            print(f"Error for {class_name}: {response.status_code}")
            print(response.text)  # Print additional details for debugging

    except requests.exceptions.RequestException as e:
        print(f"An error occurred for {class_name}: {e}")
