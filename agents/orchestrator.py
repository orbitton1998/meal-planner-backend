import json
from agents.meal_agents import (
    IngredientAnalyzerAgent,
    RecipeGeneratorAgent,
    NutritionAgent,
    ShoppingListAgent
)

class MealPlannerOrchestrator:
    def __init__(self):
        self.analyzer = IngredientAnalyzerAgent()
        self.recipe_generator = RecipeGeneratorAgent()
        self.nutrition_agent = NutritionAgent()
        self.shopping_agent = ShoppingListAgent()
    
    def run(self, ingredients: list[str], preferences: list[str], people: int) -> dict:
        print("\n🚀 Starting MealPlanner Agent Pipeline...\n")
        
        # Step 1: Analyze ingredients
        analysis = self.analyzer.run(
            f"Ingredients: {', '.join(ingredients)}\nPreferences: {', '.join(preferences) or 'none'}\nPeople: {people}"
        )
        analysis_data = json.loads(analysis)
        print(f"📊 Analysis: {analysis_data}")
        
        # Step 2: Generate meal plan
        meal_plan = self.recipe_generator.run(
            f"Ingredient analysis: {analysis}\nNumber of people: {people}"
        )
        meal_plan_data = json.loads(meal_plan)
        
        # Step 3: Nutrition analysis
        nutrition = self.nutrition_agent.run(
            f"Meal plan: {meal_plan}"
        )
        nutrition_data = json.loads(nutrition)
        
        # Step 4: Shopping list
        shopping = self.shopping_agent.run(
            f"Meal plan: {meal_plan}\nAvailable ingredients: {', '.join(ingredients)}"
        )
        shopping_data = json.loads(shopping)
        
        print("\n✅ All agents completed successfully!\n")
        
        return {
            "meal_plan": meal_plan_data,
            "nutrition": nutrition_data,
            "shopping_list": shopping_data["shopping_list"],
            "ingredient_analysis": analysis_data
            }