from bs4 import BeautifulSoup
import requests
import json

from accents import remove_accents


URL = 'https://www.przepisy.pl/'


def get_recipe_ingredients(recipe_name_url):
    current_url = URL + 'przepis/' + recipe_name_url
    source = requests.get(current_url)
    if source.ok:
        soup = BeautifulSoup(source.text, 'html.parser')
        div_list = soup.find_all('div', class_='ingredients-list-content-item')
        ingredients_list = []
        for element in div_list:
            ingredients_list.append(element.find('p', class_='ingredient-name').text.strip().capitalize())
        return ingredients_list
    raise AttributeError("Source does not exist")


def get_recipe_names(category_url):
    current_url = URL + 'przepisy/' + category_url
    source = requests.get(current_url)
    if source.ok:
        soup = BeautifulSoup(source.text, 'html.parser')
        div_list = soup.find_all('div', class_='title-recipe')
        names_list = []
        for element in div_list:
            names_list.append(element.text.strip())
        return names_list
    raise AttributeError("Wrong URL address")


def get_data(category_url, category_name):
    recipe_names = None
    try:
        recipe_names = get_recipe_names(category_url)
    except AttributeError:
        print("Category address is illegal")
        exit(1)

    error_number = 0
    success_number = 0

    recipe_list = []

    for recipe in recipe_names:
        recipe_url = remove_accents(recipe.lower().replace(' ', '-'))
        try:
            ingredients = get_recipe_ingredients(recipe_url)
        except AttributeError:
            error_number += 1
            continue
        success_number += 1

        recipe_list.append({
            "recipe": recipe,
            "recipe_url": URL + 'przepis/' + recipe_url,
            "ingredients": ingredients
        })

    res = {
        "category": category_name,
        "recipes": recipe_list,
        "errors": error_number,
        "success": success_number
    }

    return res


if __name__ == "__main__":
    # print(get_recipe_ingredients('kruche-ciasto-z-budyniowa-pianka-i-owocami-12057'))
    # print(get_recipe_names('posilek/sniadanie'))
    data = get_data('posilek/sniadanie', "Śniadanie")

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile, ensure_ascii=False)
