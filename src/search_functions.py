import csv
import requests  # https://pypi.org/project/requests/
from colored import fg, bg, attr
import time
import random
import pdfkit
import re
from meal_mate_functions import staple_ignore, staple_setting
from main import staple__default_setting, staple_setting


def get_recipes(ingr_file_name, staple_file_name):
    p = ""  # pantry + staples
    with open(ingr_file_name, "r") as f:
        reader = csv.reader(f)
        reader.__next__()
        for row in reader:
            p = p + str(row[0]) + ","
    if staple_ignore:
        with open(staple_file_name, "r") as f:
            reader = csv.reader(f)
            reader.__next__()
            for row in reader:
                if row[1] == "True":
                    p = p + row[0] + ","
    print(p)
    print(staple_setting)
    print(f"{fg(111)}Searching for recipes with {len(p.split(',')) - 1} items{attr(0)}{' and ignoring staple items' if not staple_setting else ''}")
    r = requests.get(
        'https://api.spoonacular.com/recipes/findByIngredients?apiKey=3e06d892f3044bab8b766176ccd0e18c&ingredients=' + p + '&ranking=2&number=5' + ('&ignorePantry=true' if not staple_ignore else ''))
    # r.headers['content-type'] = 'application/json; charset=utf8'
    json = r.json()
    if len(json) > 0:
        i = x = y = 0
        for recipe in json:
            i += 1
            if recipe["usedIngredientCount"] == (len(p.split(",")) - 1):
                if y == 0:
                    print(
                        f"\n{bg(2)}The following recipes utilise your existing ingredients!{attr(0)}")
                    time.sleep(2)
                    y += 1
                print(
                    f'{fg(random.randrange(0,256))}{i}. {recipe["title"]}{attr(0)}')
                print(f'Utilises: {recipe["usedIngredientCount"]} items, Requires: {recipe["missedIngredientCount"]} items')
                time.sleep(0.1)
            else:
                if x == 0:
                    print(
                        f"\n{bg(1)}Here are some recipes which may require a trip to the shops{attr(0)}")
                    time.sleep(2)
                    x += 1
                print(
                    f'{fg(random.randrange(0,256))}{i}. {recipe["title"]}{attr(0)}')
                print(
                    f'Utilises: {recipe["usedIngredientCount"]} items, Requires: {recipe["missedIngredientCount"]} items')
                time.sleep(0.1)
    elif len(json) == 0:
        print("No recipes found\nPlease use remove some ingredients or consider changing the prioritisation")
        return

    def search_menu():
        print(f'{bg(random.randrange(0, 256))}Recipe options{attr(0)}')
        print(
            f"{fg(random.randrange(0,256))}1. View more details{attr(0)} about a recipe")
        print(f"{fg(random.randrange(0,256))}2. Export{attr(0)} a recipe")
        print(f"{bg(1)}Exit{attr(0)}")
        print(f"{fg(1)}3.{attr(0)} to {fg(1)}exit{attr(0)}")
        # local variable
        choice = input("Enter your selection: ")
        return choice

    def recipe_menu(json):
        try:
            recipe_int = int(input(
                "Press q to return to search options menu\nWhich number recipe?: "))
            recipe_id = str(json[recipe_int - 1]["id"])
            recipe_id_response = requests.get(
                'https://api.spoonacular.com/recipes/' + recipe_id + '/information?apiKey=3e06d892f3044bab8b766176ccd0e18c')
            return recipe_id_response.json()
        except ValueError:
            return

    CLEANR = re.compile('<.*?>')

    def cleanhtml(raw_html):
        cleantext = re.sub(CLEANR, '', raw_html)
        return cleantext

    def recipe_export(json):
        recipe_id_details = recipe_menu(json)
        cleaned_summary = cleanhtml(recipe_id_details["summary"])
        index_clean_summary = cleaned_summary.split(".")
        # index_clean_summary = cleaned_summary.find("If you like this recipe")
        print(f'{fg(random.randrange(0, 256))}{recipe_id_details["title"]}{attr(0)}')
        print(
            f'{fg(random.randrange(0,256))}Total cooking time: {recipe_id_details["readyInMinutes"]}{attr(0)}')
        print(
            f'{fg(random.randrange(0,256))}Serving size: {recipe_id_details["servings"]}{attr(0)}')
        print(f'{fg(random.randrange(0,256))}Ingredients:{attr(0)}')
        for ingredients in recipe_id_details["extendedIngredients"]:
            print(f'-  {ingredients["original"]}')
        print(
            # f'{fg(random.randrange(0,256))}Summary:\n{cleaned_summary[:index_clean_summary]}{attr(0)}')
            f'{fg(random.randrange(0,256))}Summary:\n{cleaned_summary[:index_clean_summary[-2]]}{attr(0)}')

    # def specific_recipe(recipe_menu):
    #     recipe_id_details = recipe_menu(json)
    #     print(recipe_details["summary"])

    json = r.json()
    search_choice = ""
    while search_choice != "3":
        search_choice = search_menu()
        match search_choice:
            case "1":
                recipe_export(json)
            case "2":
                pass
            case "3":
                continue

        input(f"{bg(177)}Press Enter to continue...{attr(0)}\n")
