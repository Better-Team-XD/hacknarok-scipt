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
            image_url = f'https://s3.przepisy.pl/przepisy3ii/img/variants/800x0/{recipe_url}.jpg'
            if requests.get(image_url).status_code != 200:
                raise AttributeError
        except AttributeError:
            error_number += 1
            continue
        success_number += 1

        recipe_list.append({
            "name": recipe,
            "category": category_name,
            "url": URL + 'przepis/' + recipe_url,
            "imgUrl": f'https://s3.przepisy.pl/przepisy3ii/img/variants/800x0/{recipe_url}.jpg',
            "ingredients": ingredients
        })

    res = {
        "category": category_name,
        "recipes": recipe_list,
    }

    return res


if __name__ == "__main__":
    data = get_data('posilek/sniadanie?page=2', "Śniadanie")
    recipe_list = data["recipes"]
    for recipe in recipe_list:
        r = requests.post('http://localhost:8080/api/v1/recipes', json=recipe)
        print(r)
