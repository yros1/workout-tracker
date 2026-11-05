import os

import requests
from dotenv import load_dotenv
import sys

load_dotenv()

base_url = "https://app.100daysofpython.dev"

def is_api_running():
    """
    Check if the API server is running by sending a GET request to the health check endpoint.
    Returns True if the server is running, False otherwise.
    """
    try:
        health_endpoint = f"{base_url}/healthz"
        health_response = requests.get(url=health_endpoint, timeout=5)
    except requests.exceptions.RequestException as re:
        print(f"Error checking server status: {re}")
        return False

    if health_response.status_code != 200:
        print(f"Health check failed with HTTP status {health_response.status_code}.")
        return False

    try:
        health_result = health_response.json()
    except requests.exceptions.JSONDecodeError as jde:
        print(f"Health check returned invalid JSON: {jde}")
        return False

    if not isinstance(health_result, dict):
        print("Health check returned an unexpected response format.")
        return False

    return health_result.get("status") == "ok"

# 1. Get Exercise Stats with Natural Language Queries.
# "https://app.100daysofpython.dev/v1/nutrition/natural/exercise"

if not is_api_running():
    print("API server is not running. Please check the server status.")
    sys.exit(1)

if not os.getenv("YOUR_NUTRITION_API_KEY") or not os.getenv("YOUR_APP_ID"):
    print("API key or App ID is not set. Please set them in the .env file.")
    sys.exit(1)

exercise_url = f"{base_url}/v1/nutrition/natural/exercise"

exercise_text = input("Tell me which exercise you did (e.g., 'ran 9 miles'): ")

exercise_parameters = {
    "query": exercise_text,
    "weight_kg": 78,                  # Optional: Weight in kg (1-500)
    "height_cm": 175,                 # Optional: Height in cm (1-300)
    "age": 30,                        # Optional: Age (1-150)
    "gender": "male"                  # Optional: "male" or "female"
}

headers = {
    "Content-Type": "application/json",
    "x-app-id": os.getenv("YOUR_APP_ID"),
    "x-app-key": os.getenv("YOUR_NUTRITION_API_KEY")
}

try:
    response = requests.post(
        url=exercise_url,
        json=exercise_parameters,
        headers=headers,
        timeout=5
    )
except requests.exceptions.RequestException as e:
    print(f"Exercise request failed: {e}")
    sys.exit(1)

error_messages = {
    401: "Missing or invalid API credentials.",
    422: "The request was invalid. Check the required fields.",
    429: "Rate limit exceeded. Wait before trying again.",
    500: "The server encountered an internal error."
}

if not 200 <= response.status_code < 300:
    message = error_messages.get(
        response.status_code,
        "The server returned an unsuccessful response."
    )
    print(f"Exercise request failed (HTTP {response.status_code}): {message}")
    sys.exit(1)

try:
    result = response.json()
except requests.exceptions.JSONDecodeError:
    print("Exercise request returned invalid JSON.")
    sys.exit(1)

if not isinstance(result, dict):
    print("Exercise request returned an unexpected response format.")
    sys.exit(1)

exercises = result.get("exercises")
if not isinstance(exercises, list) or not exercises:
    print("The response did not contain any exercises.")
    sys.exit(1)

print(exercises[0]) # Print the first exercise result