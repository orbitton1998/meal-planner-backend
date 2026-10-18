from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from datetime import date, timedelta
import anthropic
import os
import sys
import json

# Agents print emoji; the default Windows console encoding (cp1252) can't encode them.
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from agents.orchestrator import MealPlannerOrchestrator
from auth import get_current_user, require_user
from supabase_client import supabase

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

def _current_week_start() -> str:
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    return monday.isoformat()


@app.post("/generate-meal-plan")
async def generate_meal_plan(request: MealPlanRequest, user=Depends(get_current_user)):
    orchestrator = MealPlannerOrchestrator()
    result = orchestrator.run(
        ingredients=request.ingredients,
        preferences=request.preferences,
        people=request.people
    )

    saved = False
    if user is not None:
        supabase.table("meal_plans").insert({
            "user_id": user.id,
            "week_start": _current_week_start(),
            "plan": result["meal_plan"],
            "shopping_list": result["shopping_list"],
        }).execute()
        saved = True

    result["saved"] = saved
    return result


@app.get("/meal-plans/{user_id}")
async def get_meal_plans(user_id: str, user=Depends(require_user)):
    if user.id != user_id:
        raise HTTPException(status_code=403, detail="Cannot access another user's meal plans")

    response = (
        supabase.table("meal_plans")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )
    return response.data

