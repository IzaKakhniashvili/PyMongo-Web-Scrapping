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