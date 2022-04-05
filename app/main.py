from flask import Flask
from flask import send_file
from flask import request
import spoonacular

API_KEY = "a80ce6a267f14f4f86a64efe027f6495"

app = Flask(__name__)
api = spoonacular.API(API_KEY)

@app.route("/")
def home_view():
    return "<h1>HAIID peep & STUFF! /n does it</h1>"

@app.route("/generate_meal_plan_from_diet=<string:dietstring>/")
def get_meal_plan(dietstring):
    response = api.generate_meal_plan(diet=dietstring)
    data = response.json()
    meals = data["items"]
    day_meals = [m for m in meals if m['day']==1]

    return "<h1>" + str(day_meals) + "</h1>"

@app.route("/recipe_search_str=<string:query>/")
def recipe_search(query):
    response = api.search_recipes_complex(query)
    data = response.json()
    img = data['results'][0]['image']
    return "<h1>" + str(img) + "</h1>"


@app.route("/get_growth_stage/<string:image>/")
def nn(image):
    return "RIPE TOMATO"


@app.route("/get_recipes")
def get_recipes():
    #inputs
    diet = request.args.get('diet', default='None', type = str)
    user_ingredients = request.args.get('userIngredients',default='', type=str)
    allowed_missed_ingredients = request.args.get('allowMissed',default='', type=int)
    num_recipes_wanted = request.args.get('recipesWanted',default='', type=int)

    return diet + user_ingredients+str(allowed_missed_ingredients)+str(num_recipes_wanted)

    valid_recipes = []
    while len(valid_recipes) < num_recipes_wanted:
        rec_from_ingr = api.search_recipes_by_ingredients(user_ingredients)
        for rec in rec_from_ingr:
            if rec['missedIngredientCount'] <= allowed_missed_ingredients:
                if diet=='None':
                    valid_recipes.append(rec)
                else:
                    rec_details = api.get_recipe_information(rec['id'])
                    if diet in rec_details['diets']:
                        valid_recipes.append(rec)
                

    
    return valid_recipes
