import json
from agents.base_agent import BaseAgent

class IngredientAnalyzerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="IngredientAnalyzer",
            system_prompt="""You are a culinary expert. Analyze the ingredients provided 
            and return a JSON object with:
            - available_ingredients: list of ingredients the user has
            - cuisine_possibilities: list of 3 cuisine types that work with these ingredients
            - missing_basics: list of common pantry items that seem to be missing
            Respond ONLY with valid JSON, no markdown."""
        )

class RecipeGeneratorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="RecipeGenerator",
            system_prompt="""You are a professional chef. Based on the ingredient analysis provided,
            create a 7-day meal plan (breakfast, lunch, dinner).
            Respond ONLY with valid JSON in this exact format:
            {
              "monday":    {"breakfast": "...", "lunch": "...", "dinner": "..."},
              "tuesday":   {"breakfast": "...", "lunch": "...", "dinner": "..."},
              "wednesday": {"breakfast": "...", "lunch": "...", "dinner": "..."},
              "thursday":  {"breakfast": "...", "lunch": "...", "dinner": "..."},
              "friday":    {"breakfast": "...", "lunch": "...", "dinner": "..."},
              "saturday":  {"breakfast": "...", "lunch": "...", "dinner": "..."},
              "sunday":    {"breakfast": "...", "lunch": "...", "dinner": "..."}
            }"""
        )

class NutritionAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="NutritionAnalyst",
            system_prompt="""You are a nutritionist. Given a 7-day meal plan, estimate the 
            daily nutritional values. Respond ONLY with valid JSON in this format:
            {
              "daily_average": {
                "calories": 0,
                "protein_g": 0,
                "carbs_g": 0,
                "fat_g": 0
              },
              "nutrition_notes": "brief health assessment in one sentence"
            }"""
        )

class ShoppingListAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="ShoppingList",
            system_prompt="""You are a smart shopping assistant. Given a meal plan and 
            available ingredients, generate a shopping list of ONLY the missing items needed.
            Organize by category. Respond ONLY with valid JSON in this format:
            {
              "shopping_list": {
                "produce": ["item1", "item2"],
                "proteins": ["item1"],
                "dairy": ["item1"],
                "pantry": ["item1"],
                "other": ["item1"]
              }
            }"""
        )