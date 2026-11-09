# Workout Tracker

A command-line Python app that estimates exercise details from a natural-language
description and saves the result to a Google Sheet through the Sheety API.

## How It Works

1. Enter an exercise description, such as “ran for 30 minutes.”
2. The app sends it, along with your profile details, to the Nutrition API.
3. It saves the first exercise result to your Sheety workout sheet, including
   the date, time, exercise, duration, and calories.

## Requirements

- Python 3
- Dependencies listed in `requirements.txt`
- Nutrition API credentials
- A configured Sheety account and workout sheet

## Setup

1. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Copy `.env_example` to `.env`.

3. Add your credentials to `.env`:

   ```text
   YOUR_NUTRITION_APP_ID=your_nutrition_app_id
   YOUR_NUTRITION_API_KEY=your_nutrition_api_key
   YOUR_SHEETY_API_USERNAME=your_sheety_api_username
   YOUR_SHEETY_API_AUTHENTICATION_BEARER_TOKEN=your_sheety_bearer_token
   ```

   **Do not commit `.env` or share your credentials.**

4. Run the program from the project directory:

   ```bash
   python main.py
   ```

## Example Exercise Descriptions

- `ran for 30 minutes`
- `swam for 1 hour`
- `walked 3 miles`
- `biked for 1 hour`
- `lifted weights for 45 minutes`

The Nutrition API accepts exercise descriptions up to 50 characters. The profile
values (weight, height, age, and gender) are currently set in `main.py`; update
them there to match your details.

## Project Files

- `main.py` — Runs the workout tracking flow.
- `nutrition.py` — Requests exercise estimates from the Nutrition API.
- `sheets.py` — Saves workout data through the Sheety API.
- `requirements.txt` — Lists the Python dependencies.
- `.env_example` — Template for the required environment variables.
