import aiohttp
import asyncio
from bs4 import BeautifulSoup
from mongo_data import (get_mongo_client, insert_data, close_client,
                        get_average_ingredients, get_average_steps,
                        get_most_recipes_author, get_most_portions_recipe)


base_url = 'https://kulinaria.ge'
url = 'https://kulinaria.ge/receptebi/cat/xorceuli/'

async def fetch_html(session, url):
    async with session.get(url, ssl=False) as response:
        return await response.text()


async def get_recipe_urls(session):
    html = await fetch_html(session, url)
    soup = BeautifulSoup(html, 'lxml')

    recipe_titles = soup.find_all('a', class_='box__title')
    urls = [{'name': recipe.get_text(strip=True), 'url': base_url + recipe['href']} for recipe in recipe_titles]
    return urls


async def get_recipe_details(session, recipe_url, sem):
    async with sem:
        html = await fetch_html(session, recipe_url)
        soup = BeautifulSoup(html, 'lxml')

        # Fetch categories and categories' URLs
        categories = soup.find_all('a', class_='pagination__item')
        if len(categories) >= 2:
            category = categories[-2].get_text(strip=True)
            category_url = categories[-2]['href']
            subcategory = categories[-1].get_text(strip=True)
            subcategory_url = categories[-1]['href']
        else:
            category, subcategory, category_url, subcategory_url = None, None, None, None

        # Fetch photo URL
        post_image = soup.find('img', class_='post__img')
        photo_url = base_url + post_image['src'] if post_image else None

        # Fetch description
        description = soup.find('div', class_='post__description')
        description_text = description.get_text(strip=True) if description else 'No description'

        # Fetch author
        author_name = soup.find('span', class_='bold')
        author = author_name.get_text(strip=True) if author_name else 'Unknown author'

        # Fetch steps
        steps = soup.find_all('div', class_='lineList__item')
        step_list = [step.get_text(strip=True) for step in steps]

        # Fetch ingredients
        ingredients = soup.find_all('div', class_='list__item')
        ingredient_texts = [' '.join(ingredient.get_text(strip=True).split()) for ingredient in ingredients]

        # Fetch portion (Servings)
        portion_time = soup.find_all('div', class_='lineDesc__item')
        portion = next((p.get_text(strip=True) for p in portion_time if 'ულუფა' in p.get_text(strip=True)), None)

        return {
            'category': category,
            'category_url': category_url,
            'subcategory': subcategory,
            'subcategory_url': subcategory_url,
            'photo_url': photo_url,
            'description': description_text,
            'author': author,
            'steps': step_list,
            'ingredients': ingredient_texts,
            'portion': portion
        }


async def scrape_recipes():
    async with aiohttp.ClientSession() as session:
        sem = asyncio.Semaphore(10)
        recipe_urls = await get_recipe_urls(session)

        tasks = [get_recipe_details(session, recipe['url'], sem) for recipe in recipe_urls]

        recipe_details = await asyncio.gather(*tasks)

        recipes = []
        for i, details in enumerate(recipe_details):
            recipe_info = {
                'name': recipe_urls[i]['name'],
                'url': recipe_urls[i]['url'],
                **details
            }
            recipes.append(recipe_info)

        return recipes


async def main():
    recipe_data = await scrape_recipes()
    mongo_client = get_mongo_client('mongodb://localhost:27017/')
    insert_data(mongo_client, 'recipe_data', recipe_data)

    collection = mongo_client['recipe_data']['recipes']
    author, count = get_most_recipes_author(collection)
    if author:
        print(f"ყველაზე მეტი რეცეპტის ავტორი: {author}, რეცეპტების რაოდენობა: {count}")
    else:
        print("ავტორი არ მოიძებნა.")

    recipe_name, recipe_url, portion = get_most_portions_recipe(collection)
    if recipe_name:
        print(f"რეცეპტის სახელი: {recipe_name}, რეცეპტის URL: {recipe_url}, პორცია: {portion}")

    avg_ingredients = get_average_ingredients(collection)
    avg_steps = get_average_steps(collection)

    print(f'ინგრედიენტების საშუალო რაოდნეობა: {int(avg_ingredients)}')
    print(f'მომზადების ეტაპების საშუალო რაოდენობა: {int(avg_steps)}')
    close_client(mongo_client)


if __name__ == "__main__":
    asyncio.run(main())
