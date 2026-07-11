import csv  # Import the csv module to read data from CSV files.
import re  # Import the re module to work with regular expressions.
from pathlib import Path  # Import Path to handle file paths easily.

import streamlit as st  # Import Streamlit to build the web app interface.

# Set the page configuration for the Streamlit app.
st.set_page_config(page_title="Recipe Suggestor", page_icon="🍳", layout="centered")

# Display the main title of the app.
st.title("🍽️ Recipe Suggestor")
# Display a short description for the user.
st.write("Enter your available ingredients and I will suggest matching recipes from your CSV file.")

# Define the path to the CSV file in the same folder as this script.
DEFAULT_FILE = Path(__file__).with_name("all_recipies.csv")


# Define a function that converts input text into a clean set of ingredients.
def parse_ingredients(raw_text: str) -> set[str]:
    # Split the text by new lines, commas, or semicolons.
    items = re.split(r"[\n,;]+", raw_text)
    # Return only non-empty ingredient names in lowercase.
    return {item.strip().lower() for item in items if item.strip()}


# Define a function that reads recipe data from a CSV file.
def load_recipes_from_csv(file_path: Path) -> list[dict[str, str]]:
    # Check whether the file exists before trying to read it.
    if not file_path.exists():
        # Return an empty list if the file is missing.
        return []

    # Create an empty list to store recipe dictionaries.
    recipes: list[dict[str, str]] = []
    # Open the CSV file for reading.
    with file_path.open("r", encoding="utf-8", newline="") as handle:
        # Create a CSV reader object.
        reader = csv.DictReader(handle)
        # Loop through each row in the CSV file.
        for row in reader:
            # Read the recipe name from the CSV row.
            name = (row.get("recipe_name") or "").strip()
            # Read the recipe description from the CSV row.
            description = (row.get("description") or "").strip()
            # Skip rows that do not contain a recipe name or description.
            if not name and not description:
                # Continue to the next row.
                continue
            # Store the recipe as a dictionary with a searchable text field.
            recipes.append(
                {
                    # Store the recipe name.
                    "name": name,
                    # Store the recipe description.
                    "description": description,
                    # Create a simple cooking instruction based on the recipe name.
                    "instructions": self_make_instruction(name),
                    # Create a lowercase text version for matching.
                    "text": f"{name} {description}".lower(),
                }
            )
    # Return the list of recipes.
    return recipes


# Define a function that finds matching recipes and missing ingredients.
def self_make_instruction(recipe_name: str) -> str:
    # Create a simple generic cooking instruction based on the recipe name.
    lowered = recipe_name.lower()
    if "salmon" in lowered:
        return "Season the salmon, cook it until tender, and serve with your favorite sides."
    if "chicken" in lowered:
        return "Cook the chicken thoroughly, add seasoning, and serve hot."
    if "pasta" in lowered:
        return "Boil the pasta, prepare the sauce, and combine them until well coated."
    if "sandwich" in lowered:
        return "Toast or warm the bread, add the filling, and serve immediately."
    if "wrap" in lowered:
        return "Fill the wrap with your ingredients, roll it tightly, and serve."
    if "omelette" in lowered or "frittata" in lowered:
        return "Beat the eggs, cook them in a pan, and fold before serving."
    if "rice" in lowered:
        return "Cook the rice, stir-fry the ingredients, and mix everything together."
    if "steak" in lowered:
        return "Season the steak, sear it until cooked to your liking, and rest before serving."
    if "potato" in lowered or "fries" in lowered:
        return "Cook the potatoes until crisp and golden, then serve warm."
    return "Prepare the ingredients, cook them carefully, and serve with your preferred side."


def suggest_recipes(available_ingredients: set[str], recipes: list[dict[str, str]]) -> list[tuple[int, dict[str, str], set[str], list[str]]]:
    # Create an empty list for the suggestions.
    suggestions: list[tuple[int, dict[str, str], set[str], list[str]]] = []
    # Loop through each recipe.
    for recipe in recipes:
        # Find which ingredients from the user's input appear in the recipe text.
        matched = {item for item in available_ingredients if item in recipe["text"]}
        # Only keep recipes that matched at least one ingredient.
        if matched:
            # Create an empty list for missing ingredients.
            missing: list[str] = []
            # Check a short list of common ingredient words.
            for ingredient in ["rice", "egg", "onion", "tomato", "cheese", "chicken", "pasta", "bread", "salmon", "steak"]:
                # Add the ingredient to the missing list if it appears in the recipe but is not in the user's list.
                if ingredient in recipe["text"] and ingredient not in available_ingredients:
                    # Append the missing ingredient.
                    missing.append(ingredient)
            # Store the recipe suggestion with its match count and missing list.
            suggestions.append((len(matched), recipe, matched, missing))

    # Sort recipes from most matched to least matched.
    suggestions.sort(key=lambda item: item[0], reverse=True)
    # Return the sorted suggestions.
    return suggestions


# Load the recipe list once when the app starts.
recipes: list[dict[str, str]] = load_recipes_from_csv(DEFAULT_FILE)

# Show a caption if recipes were loaded successfully.
if recipes:
    # Display how many recipes were loaded.
    st.caption(f"Loaded {len(recipes)} recipes from {DEFAULT_FILE.name}.")
else:
    # Warn the user if the CSV file was not found.
    st.warning(f"Could not find {DEFAULT_FILE.name}. Place it in this folder to use it.")

# Create a form for the user to enter ingredients.
with st.form("recipe_form"):
    # Create a text area for ingredient input.
    ingredients_input = st.text_area(
        # Label the input box.
        "Ingredients you already have",
        # Provide a helpful example placeholder.
        placeholder="Example: rice, egg, onion, tomato, cheese",
        # Set the height of the text area.
        height=120,
    )
    # Create a button to submit the form.
    submitted = st.form_submit_button("Suggest recipes")

# Handle the submitted form data.
if submitted:
    # Parse the entered ingredients into a set.
    available_ingredients = parse_ingredients(ingredients_input)

    # Check whether the user entered anything.
    if not available_ingredients:
        # Show a warning if the input is empty.
        st.warning("Please enter at least three ingredients.")
    else:
        # Generate recipe suggestions based on the entered ingredients.
        suggestions = suggest_recipes(available_ingredients, recipes)

        # Check whether any suggestions were found.
        if suggestions:
            # Show the heading for the suggestions section.
            st.subheader("Recommended recipes")
            # Loop through the top suggestions.
            for _, recipe, matched, missing in suggestions[:10]:
                # Create a container for each suggestion.
                with st.container():
                    # Display the recipe name.
                    st.markdown(f"### {recipe['name']}")
                    # Display the recipe description.
                    st.write(recipe["description"])
                    # Show a simple instruction for making the recipe.
                    st.write(f"Instructions: {recipe['instructions']}")
                    # Show which ingredients were matched.
                    st.caption(f"Matched ingredients: {', '.join(sorted(matched)) or 'none'}")
                    # Show the missing ingredients if any exist.
                    if missing:
                        # Display the missing ingredients.
                        st.caption(f"Missing ingredients: {', '.join(sorted(missing))}")
                    else:
                        # Display a message when there are no missing ingredients.
                        st.caption("Missing ingredients: none")
                    # Add a blank line for spacing.
                    st.write("")
        else:
            # Show a message if no recipes matched.
            st.info("No recipe matches were found. Try adding more common ingredients like rice, egg, onion, tomato, or cheese.")
else:
    # Show an example hint before the user submits anything.
    st.info("Try entering ingredients like rice, egg, tomato, onion, and cheese.")
