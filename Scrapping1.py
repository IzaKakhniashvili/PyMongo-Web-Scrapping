import requests
from bs4 import BeautifulSoup


url = "https://kulinaria.ge/receptebi/cat/xorceuli/"
response = requests.get(url)

soup = BeautifulSoup(response.content, "lxml")

base_url = "https://kulinaria.ge"


def get_categories(recipe_url):
    new_response = requests.get(recipe_url)
    soup = BeautifulSoup(new_response.content, 'lxml')
    
    categories = soup.find_all('a', class_='pagination__item')
    
    if len(categories) >= 2:
        subcategory = categories[-1].get_text(strip=True)
        category = categories[-2].get_text(strip=True)
        sub_url = base_url + categories[-1]['href']
        cat_url = base_url + categories[-2]['href']
    else:
        subcategory, category, sub_url, cat_url = None, None, None, None
    
    return category, subcategory, cat_url, sub_url


def get_photo_url(recipe_url):
    new_response = requests.get(recipe_url)
    soup = BeautifulSoup(new_response.content, 'lxml')
    
    post_image = soup.find('img', class_='post__image')
    
    if post_image:
        photo_url = base_url + post_image['src']
    else:
        photo_url = None
    
    return photo_url

info = []
recipe_title = soup.find_all('a', class_='box__title')

for rec in recipe_title:
    recipe = {}
    recipe_name = rec.get_text(strip=True)
    recipe_url = base_url + rec['href']
    
    category, subcategory, cat_url, sub_url = get_categories(recipe_url)
    photo_url = get_photo_url(recipe_url)
    
    recipe["recipe name"] = recipe_name
    recipe["recipe url"] = recipe_url
    recipe["category"] = category
    recipe["subcategory"] = subcategory
    recipe["category url"] = cat_url
    recipe["subcategory url"] = sub_url
    recipe["photo url"] = photo_url
    info.append(recipe)

print(info)