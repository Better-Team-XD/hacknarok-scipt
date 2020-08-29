from bs4 import BeautifulSoup
import requests

URL = 'https://www.przepisy.pl/przepis/'


def get_recipe_ingredients(recipe_name_url):
    current_url = URL + recipe_name_url
    source = requests.get(current_url)
    if source.ok:
        soup = BeautifulSoup(source.text, 'html.parser')
        div_list = soup.find_all('div', class_='ingredients-list-content-item')
        ingredients_list = []
        for element in div_list:
            ingredients_list.append(element.find('p', class_='ingredient-name').text.strip().capitalize())
        return ingredients_list
    raise Exception("Bad source exception")


if __name__ == "__main__":
    print(get_recipe_ingredients('kruche-ciasto-z-budyniowa-pianka-i-owocami-12057'))

