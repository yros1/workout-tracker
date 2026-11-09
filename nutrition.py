import os
import requests
import sys

class Nutrition:

    def __init__(self, exercise_data, weight_kg, height_cm, age, gender):
        self.base_url = "https://app.100daysofpython.dev"
        self.exercise_data = exercise_data
        self.weight_kg = weight_kg
        self.height_cm = height_cm
        self.age = age
        self.gender = gender

    def is_api_running(self):
        """
        Check if the API server is running by sending a GET request to the health check endpoint.
        Returns True if the server is running, False otherwise.
        """
        try:
            health_endpoint = f"{self.base_url}/healthz"
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

    def get_exercise_stats(self):
        """
        Calculate calories burned from a natural language exercise description.
        Get exercise stats with natural language queries and print the result.
        "https://app.100daysofpython.dev/v1/nutrition/natural/exercise"
        1. Check if the API server is running.
        2. Check if the API key and App ID are set in the environment variables.
        3. Send a POST request to the exercise endpoint with the provided exercise data and user parameters.
        4. Handle errors and print the first exercise result if successful.
        Character limit: Maximum 50 characters

        Supported activities:
            Running/Jogging - "ran for 30 minutes", "jogged 2 miles"
            Swimming - "swam for 1 hour", "swimming laps"
            Walking - "walked 3 miles", "brisk walk 45 min"
            Cycling - "biked for 1 hour", "rode bike 10 miles"
            Weightlifting - "lifted weights 45 min", "weight training"
        """
        if not self.is_api_running():
            print("API server is not running. Please check the server status.")
            sys.exit(1)

        if not os.getenv("YOUR_NUTRITION_API_KEY") or not os.getenv("YOUR_NUTRITION_APP_ID"):
            print("API key or App ID is not set. Please set them in the .env file.")
            sys.exit(1)

        exercise_url = f"{self.base_url}/v1/nutrition/natural/exercise"

        exercise_parameters = {
            "query": self.exercise_data,
            "weight_kg": self.weight_kg,  # Optional: Weight in kg (1-500)
            "height_cm": self.height_cm,  # Optional: Height in cm (1-300)
            "age": self.age,  # Optional: Age (1-150)
            "gender": self.gender  # Optional: "male" or "female"
        }

        headers = {
            "Content-Type": "application/json",
            "x-app-id": os.getenv("YOUR_NUTRITION_APP_ID"),
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

        exercise = exercises[0]

        return exercise