from pymongo import MongoClient

def get_mongo_client(uri):
    client = MongoClient(uri)
    return client

def insert_data(client, db_name, recipes):
    db = client[db_name]
    if isinstance(recipes, list):
        db.recipes.insert_many(recipes)
    else:
        db.recipes.insert_one(recipes)

def close_client(client):
    client.close()


def get_average_ingredients(collection):
    total_ingredients = collection.aggregate([
        {'$project': {
        'num_ingredients': {'$size': '$ingredients'}
        }},
        {'$group': {'_id': None,
        'avgIngredients': {'$avg': '$num_ingredients'}
            }}
    ])
    avg_ingredients = list(total_ingredients)
    return avg_ingredients[0]['avgIngredients'] if avg_ingredients else 0

def get_average_steps(collection):
    total_steps = collection.aggregate([
        {'$project': {
         'num_steps': {'$size': '$steps'}
        }},
        {'$group': {'_id': None,
         'avgSteps': {'$avg': '$num_steps'}
        }}
    ])
    avg_steps = list(total_steps)
    return avg_steps[0]['avgSteps'] if avg_steps else 0


def get_most_recipes_author(collection):
    most_recipes_author = collection.aggregate([
        {"$group": {
            "_id": "$author",
            "recipe_count": {"$sum": 1}
        }},
        {"$sort": {"recipe_count": -1}},
        {"$limit": 1}
    ])

    for author in most_recipes_author:
        return author['_id'], author['recipe_count']
    return None, None

def get_most_portions_recipe(collection):
    most_portions_recipe = collection.aggregate([
        {"$match": {"portion": {"$ne": None}}},
        {"$sort": {"portion": -1}},
        {"$limit": 1}
    ])

    for recipe in most_portions_recipe:
        return recipe['name'], recipe['url'], recipe['portion']
    return None, None, None

