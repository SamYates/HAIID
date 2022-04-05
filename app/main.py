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
    diet = request.args.get('diet', default='None', type= str)
    user_ingredients = request.args.get('userIngredients',default='', type=str)
    allowed_missed_ingredients = request.args.get('userIngredients',default='', type=int)
    num_recipes_wanted = request.args.get('recipesWanted',default='', type=int)

    
    return diet + user_ingredients
