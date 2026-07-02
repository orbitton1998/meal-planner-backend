from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import anthropic
import os
import json
from agents.orchestrator import MealPlannerOrchestrator

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
    orchestrator = MealPlannerOrchestrator()
    result = orchestrator.run(
        ingredients=request.ingredients,
        preferences=request.preferences,
        people=request.people
    )
    return result
    
