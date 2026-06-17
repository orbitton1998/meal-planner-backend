from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import anthropic
import os
import json

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

class MealPlanRequest(BaseModel):
    ingredients: list[str]
    preferences: list[str] = []
    people: int = 2

def build_meal_plan_prompt(ingredients: list[str], preferences: list[str], people: int) -> str:
    ingredients_str = ", ".join(ingredients)
    preferences_str = ", ".join(preferences) if preferences else "none"
    
    return f"""You are a professional chef and nutritionist.
    
The user has these ingredients at home: {ingredients_str}
Dietary preferences: {preferences_str}
Number of people: {people}

Create a full 7-day meal plan (breakfast, lunch, dinner).
Then create a shopping list of missing ingredients needed.

Respond ONLY in this exact JSON format:
{{
  "meal_plan": {{
    "monday":    {{"breakfast": "...", "lunch": "...", "dinner": "..."}},
    "tuesday":   {{"breakfast": "...", "lunch": "...", "dinner": "..."}},
    "wednesday": {{"breakfast": "...", "lunch": "...", "dinner": "..."}},
    "thursday":  {{"breakfast": "...", "lunch": "...", "dinner": "..."}},
    "friday":    {{"breakfast": "...", "lunch": "...", "dinner": "..."}},
    "saturday":  {{"breakfast": "...", "lunch": "...", "dinner": "..."}},
    "sunday":    {{"breakfast": "...", "lunch": "...", "dinner": "..."}}
  }},
  "shopping_list": ["item1", "item2", "item3"]
}}"""

@app.post("/generate-meal-plan")
async def generate_meal_plan(request: MealPlanRequest):
    prompt = build_meal_plan_prompt(
        request.ingredients,
        request.preferences,
        request.people
    )
    
    message = client.messages.create(
        model= "claude-sonnet-4-6",
        max_tokens=2000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    response_text = message.content[0].text
    print("RAW CLAUDE RESPONSE:", response_text)  # for debugging
    
    # Strip markdown code fences if Claude added them
    cleaned = response_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
    
    meal_data = json.loads(cleaned.strip())
    return meal_data