from dotenv import load_dotenv
from nutrition import Nutrition
from sheets import Sheets

load_dotenv()

# 1. Get Exercise Stats with Natural Language Queries.
exercise_text = input("Tell me which exercise you did (e.g., 'ran 9 miles'): ")

nutrition = Nutrition(
    exercise_data=exercise_text,
    weight_kg=78,
    height_cm=175,
    age=30,
    gender="male")

exercise = nutrition.get_exercise_stats()
print(exercise)

# 2. Saving Workout Data into Google Sheets
sheet = Sheets()
sheet.save_exercise(exercise=exercise)