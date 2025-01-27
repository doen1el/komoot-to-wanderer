import requests
import os

def login_to_wanderer():
    """
    Logs into the Wanderer service using credentials stored in environment variables.
    This function retrieves the username and password from the environment variables
    'WANDERER_EMAIL' and 'WANDERER_PASSWORD', respectively. It then sends a POST request
    to the Wanderer API's login endpoint to authenticate the user.
    Returns:
        dict: A dictionary containing the JSON response from the Wanderer API if the login is successful.
    Raises:
        HTTPError: If the response status code is not 200, an HTTPError is raised with the response details.
    """
    json = {
        "username": os.getenv("WANDERER_EMAIL"),
        "password": os.getenv("WANDERER_PASSWORD")
    }
    
    headers = {}
    response = requests.post(f"{os.getenv("WANDERER_BASE_URL")}/api/v1/auth/login", json=json, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()