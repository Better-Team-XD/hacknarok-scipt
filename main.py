from bs4 import BeautifulSoup
import requests

URL = 'https://www.przepisy.pl/przepis/'


def get_recipe(recipe_name_url):
    current_url = URL + recipe_name_url
    source = requests.get(current_url)
    if source.ok:
        soup = BeautifulSoup(source.text, 'html.parser')
        div_list = soup.find_all('div', class_='ingredients-list-content-item')
        name_list = []
        for element in div_list:
            name_list.append(element.find('p', class_='ingredient-name').text.strip().capitalize())
        return name_list
    raise Exception("Bad source exception")


if __name__ == "__main__":
    print(get_recipe('pomidorowa-z-makaronem'))

