import os
import requests
import sys

from datetime import datetime

class Sheets:
    def __init__(self):
        #https://api.sheety.co/your_sheety_api_username_here/workoutTracking/workouts
        self.base_url = "https://api.sheety.co"

    def save_exercise(self, exercise):
        """
        Save exercise data to Google Sheets using the Sheety API.
        :param exercise:
        {
            "workout": {
                "date": "21/07/2020",
                "time": "",
                "exercise": exercise["name"],
                "duration": exercise["duration_min"],
                "calories": exercise["nf_calories"]
              }
        }
        :return:
        """

        today = datetime.now()

        parameters = {
            "workout": {
                "date": f"{today.strftime('%d/%m/%Y')}",
                "time": f"{today.strftime('%H:%M:%S')}",
                "exercise": exercise["name"].title(),
                "duration": exercise["duration_min"],
                "calories": exercise["nf_calories"]
            }
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"{os.getenv('YOUR_SHEETY_API_AUTHENTICATION_BEARER_TOKEN')}"
        }

        if not os.getenv("YOUR_SHEETY_API_USERNAME"):
            print("Environment variable 'YOUR_SHEETY_API_USERNAME' is not set.")
            sys.exit(1)

        try:
            sheety_url = f"{self.base_url}/{os.getenv('YOUR_SHEETY_API_USERNAME')}/workoutTracking/workouts"
            response = requests.post(
                url=sheety_url,
                json=parameters,
                headers=headers,
                timeout=10
            )
        except requests.exceptions.RequestException as e:
            print(f"Failed to send data to Sheety API: {e}")
            sys.exit(1)

        try:
            result = response.json()
        except requests.exceptions.JSONDecodeError:
            print("Save request returned invalid JSON.")
            sys.exit(1)

        if not isinstance(result, dict):
            print("Save request returned an unexpected response format.")
            sys.exit(1)

        workout = result["workout"]
        if not isinstance(workout, dict) or not workout:
            print("The response did not contain any workout data.")
            sys.exit(1)

        print(f"Data workout sent to Sheety API: {workout}")