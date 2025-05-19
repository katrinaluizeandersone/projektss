import json
import os
import re
import requests
from bs4 import BeautifulSoup

FRIDGE_FILE = "fridge_items.json"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com/'
}

def load_items():
    if not os.path.exists(FRIDGE_FILE):
        return {}
    try:
        with open(FRIDGE_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def save_items(items):
    try:
        with open(FRIDGE_FILE, "w") as f:
            json.dump(items, f, indent=2)
    except IOError as e:
        print(f"Error saving items: {e}")

def list_items(items):
    if not items:
        print("\nYour fridge is empty.\n")
        return
    print("\nItems in your fridge:")
    for idx, (item, quantity) in enumerate(items.items(), 1):
        print(f"  {idx}. {item} (quantity: {quantity})")
    print()

def add_item(items):
    item = input("Enter the name of the food item to add: ").strip()
    if not item:
        print("Cannot add empty item.")
        return
    key = item.lower()
    if key in items:
        print(f'"{item}" is already in your fridge, increasing quantity by 1.')
        items[key] += 1
    else:
        items[key] = 1
        print(f'Added "{item}" to your fridge with quantity 1.')
    save_items(items)

def remove_item(items):
    if not items:
        print("Your fridge is empty. Nothing to remove.")
        return
    list_items(items)
    choice = input("Enter the number or name of the item to remove (or blank to cancel): ").strip()
    if not choice:
        print("Removal cancelled.")
        return
    # Try removing by number
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(items):
            key = list(items.keys())[idx]
            qty = items[key]
            if qty > 1:
                items[key] -= 1
                print(f"Decreased quantity of '{key}' to {items[key]}")
            else:
                items.pop(key)
                print(f'Removed "{key}" from your fridge.')
            save_items(items)
            return
        else:
            print("Invalid item number.")
            return
    # Remove by name
    key = choice.lower()
    if key in items:
        qty = items[key]
        if qty > 1:
            items[key] -= 1
            print(f"Decreased quantity of '{key}' to {items[key]}")
        else:
            items.pop(key)
            print(f'Removed "{key}" from your fridge.')
        save_items(items)
    else:
        print(f'Item "{choice}" not found in your fridge.')

def get_ingredients(recipe_name):
    search_query = recipe_name.replace(' ', '+')
    search_url = f"https://www.easyhomemeals.com/?s={search_query}"

    response = requests.get(search_url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to retrieve search results. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    recipe_title_elem = soup.find(class_='content')
    if not recipe_title_elem:
        print("No recipe found for the given name.")
        return []

    recipe_link = None
    link_tag = recipe_title_elem.find('a')
    if link_tag:
        recipe_link = link_tag['href']
    if not recipe_link:
        print("Could not find link to the recipe.")
        return []

    recipe_response = requests.get(recipe_link, headers=HEADERS)
    if recipe_response.status_code != 200:
        print(f"Failed to retrieve recipe page. Status code: {recipe_response.status_code}")
        return []

    recipe_soup = BeautifulSoup(recipe_response.text, 'html.parser')
    ingredients_container = recipe_soup.find(class_='section ingredient-col')
    if not ingredients_container:
        print("Ingredients section not found on recipe page.")
        return []

    ingredient_items = ingredients_container.find_all(['li', 'p', 'span'])
    ingredients = [item.get_text(strip=True) for item in ingredient_items if item.get_text(strip=True)]

    if not ingredients:
        ingredients = [ingredients_container.get_text(separator='\n').strip()]

    return ingredients

def extract_core_ingredient_name(raw_ingredient):
    if not raw_ingredient:
        return ""

    ingredient = raw_ingredient.lower()
    ingredient = re.sub(r'(\d+(\s\d+/\d+)?|\d+/\d+|\d+\.\d+)', '', ingredient)

    units_pattern = r'\b(cup|cups|tbsp|tablespoon|tablespoons|tsp|teaspoon|teaspoons|' \
                    r'ounce|ounces|oz|pound|pounds|lb|lbs|gram|grams|g|kilogram|kilograms|kg|kgs|' \
                    r'ml|l|pinch|dash|clove|cloves|slice|slices|can|cans|package|packages|quart|quarts|' \
                    r'liter|liters)\b'
    ingredient = re.sub(units_pattern, '', ingredient)

    descriptors_pattern = r'\b(fresh|minced|chopped|diced|ground|crushed|peeled|sliced|grated|' \
                          r'large|small|medium|optional|to taste|organic|unsalted|salted|skinless|' \
                          r'boneless|extra virgin|virgin|dried|freshly|room temperature|softened|' \
                          r'packed|firm|ripe|thinly|thick|coarsely|shredded|julienned|warm|cold|hot|' \
                          r'sweetened|unsweetened|cold-pressed|melted|crumbled|pressed|light|dark|' \
                          r'torn|seeded|deveined|trimmed|blanched|peeled|peeled and deveined|skinless|boneless)\b'
    ingredient = re.sub(descriptors_pattern, '', ingredient)

    ingredient = re.sub(r'\([^)]*\)', '', ingredient)
    ingredient = re.sub(r'[^\w\s]', '', ingredient)
    ingredient = re.sub(r'\s+', ' ', ingredient).strip()

    return ingredient

def create_shopping_list(fridge_items, recipe_ingredients):
    fridge_core_items = set(fridge_items.keys())
    shopping_list = []

    for ingredient in recipe_ingredients:
        core_name = extract_core_ingredient_name(ingredient)
        core_name_key = core_name.lower()
        matched = False
        # Match by substring logic
        for fridge_item in fridge_core_items:
            if fridge_item and (fridge_item in core_name_key or core_name_key in fridge_item):
                matched = True
                break
        if not matched and core_name:
            shopping_list.append(core_name)

    return sorted(set(shopping_list))  # Remove duplicates

def check_recipe_ingredients(recipe_name):
    recipe_ingredients = get_ingredients(recipe_name)
    if not recipe_ingredients:
        print("No ingredients found.")
        return
    core_ingredients = [extract_core_ingredient_name(ing) for ing in recipe_ingredients]
    unique_core_ingredients = sorted(set(ci for ci in core_ingredients if ci))
    print(f"\nCore ingredients for recipe '{recipe_name}':")
    for ing in unique_core_ingredients:
        print(f"- {ing}")

def main():
    print("Welcome to your Virtual Fridge!")
    items = load_items()

    while True:
        print("\nPlease choose an option:")
        print("  1. Show all items")
        print("  2. Add an item")
        print("  3. Remove an item")
        print("  4. Get shopping list from a recipe")
        print("  5. Exit")
        print("  6. Check core ingredients of a recipe")

        choice = input("Your choice: ").strip()

        if choice == '1':
            list_items(items)
        elif choice == '2':
            add_item(items)
        elif choice == '3':
            remove_item(items)
        elif choice == '4':
            recipe_name = input("Enter the recipe name: ")
            recipe_ingredients = get_ingredients(recipe_name)
            if recipe_ingredients:
                shopping_list = create_shopping_list(items, recipe_ingredients)
                if shopping_list:
                    print(f"\nShopping list for '{recipe_name}':")
                    for ing in shopping_list:
                        print(f"- {ing}")
                else:
                    print("You have all the ingredients for this recipe!")
            else:
                print("No ingredients found.")
        elif choice == '5':
            print("Goodbye! Your fridge items are saved.")
            break
        elif choice == '6':
            recipe_name = input("Enter the recipe name: ")
            check_recipe_ingredients(recipe_name)
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")

if __name__ == "__main__":
    main()
