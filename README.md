# PyMongo-Web-Scrapping


## Description
This project is an asynchronous web scraper designed to extract recipes from the website kulinaria.ge. It collects details like the recipe title, ingredients, cooking steps, and other useful information from the given recipe category. The informarion should be in a MongoDB database using PyMongo. 


## Overview
The scraper navigates to the meat recipe section of the website and fetches a list of recipes. It retrieves important details about each recipe, including:
- Recipe title and URL
- Categories and subcategories
- Categories urls and subcategories urls
- Photo URL
- Description
- Author name
- Cooking steps
- Ingredients
- Number of servings 

The project is built using asynchronous programming with aiohttp and asyncio for efficient data fetching and BeautifulSoup for parsing the HTML. The scraped data is then stored in a MongoDB database using PyMongo. Using PyMongo, this project aggregates information from saved data, that includes:
- How many ingredients does a recipe need on average
- How many preparation steps does a recipe have on average
- Which recipe has the most servings (Print its name and URL)
- Print the name of the author who has the most recipes posted

## Features
- Asynchronous Web Scraping: Efficient data collection using aiohttp for multiple requests in parallel.
- BeautifulSoup Parsing: Extracts detailed information from the HTML structure of each recipe page.
- MongoDB Storage: Stores the collected recipe data in a MongoDB database.
- Handles Recipe Attributes: Gathers various information like ingredients, steps, author, photo, and category.

## Task Division
This project was a pairing assignment with tasks divided equally between the two contributors:

  - Tinatin's tasks:
        - Retrieve data from the website, including:
                - Recipe's description
                - Author name
                - Cooking steps
                - Ingredients
                - Number of servings
        - MongoDB tasks:
                - Calculate how many ingredients a recipe needs on average
                - Calculate how many preparation steps a recipe has on average
  - Iza's tasks:
        - Retrieve data from the website, including:
                - Recipe title and URL
                - Categories and subcategories
                - Categories URLs and subcategories URLs
                - Photo URL
        - MongoDB tasks:
                - Identify which recipe has the most servings and print its name and URL
                - Print the name of the author who has the most recipes posted