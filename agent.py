import argparse
import json
import os
import re
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

load_dotenv()

RECIPE_PROMPT = """You are a professional chef and nutritionist. Given available ingredients and constraints,
suggest 3 recipes. Return JSON:
{
  "recipes": [
    {
      "name": "Recipe Name",
      "cuisine": "Italian/Asian/etc",
      "difficulty": "Easy/Medium/Hard",
      "ingredients_needed": ["ingredient (amount)"],
      "instructions": ["Step 1: ...", "Step 2: ..."]
    }
  ],
  "recommended": "Recipe Name (best match)"
}
Return only valid JSON."""

def parse_json_response(text: str) -> dict:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        cleaned = match.group(0)
    return json.loads(cleaned)

def get_recipes(ingredients: list[str], diet: str, time_limit: int, servings: int) -> dict:
    llm = ChatOpenAI(model="gpt-5.4-mini", temperature=0.5)

    constraints = []
    if diet:
        constraints.append(f"Dietary restriction: {diet}")
    if time_limit:
        constraints.append(f"Max total time: {time_limit} minutes")
    if servings:
        constraints.append(f"Servings needed: {servings}")

    messages = [
        SystemMessage(content=RECIPE_PROMPT),
        HumanMessage(content=f"Available ingredients: {', '.join(ingredients)}\n\nConstraints:\n{chr(10).join(constraints) if constraints else 'None'}"),
    ]

    response = llm.invoke(messages)
    return parse_json_response(response.content)
def display_recipe(recipe: dict):
    print(f"\n {recipe.get('name', 'Recipe')} ({recipe.get('cuisine', 'N/A')})")
    print(f" Difficulty: {recipe.get('difficulty', 'N/A')}")
    print(f"\n Ingredients:")
    for ing in recipe.get("ingredients_needed", []):
        print(f"  • {ing}")
    print(f"\n Instructions:")
    for i, step in enumerate(recipe.get("instructions", []), 1):
        print(f"  {i}. {step}")
def main():
    parser = argparse.ArgumentParser(description="Recipe Recommendation Agent")
    parser.add_argument("--ingredients", default="chicken, garlic, lemon", help="Comma-separated ingredients")
    parser.add_argument("--diet", default="", help="Dietary restriction")
    parser.add_argument("--time", type=int, default=0, help="Max cooking time in minutes")
    parser.add_argument("--servings", type=int, default=2, help="Number of servings")
    args = parser.parse_args()

    ingredients = [i.strip() for i in args.ingredients.split(",")]
    result = get_recipes(ingredients, args.diet, args.time, args.servings)

    recipes = result.get("recipes", [])
    print("\n RECOMMENDED:", result.get("recommended", "N/A"))
    for recipe in recipes:
        display_recipe(recipe)


if __name__ == "__main__":
    main()