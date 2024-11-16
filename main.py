import requests

# Base URL for the API
base_url = "https://one.ufl.edu/apix/soc/schedule/"

# Query Parameters
params = {
    "category": "CWSP",
    "term": "2251",
    "course-code": "COP3530",
    "last-row": 0
}

# Send GET Request
try:
    response = requests.get(base_url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Display the response (or process it further)
        print(data)
    else:
        print(f"Error: {response.status_code}")
        print(response.text)  # Print additional details for debugging

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
