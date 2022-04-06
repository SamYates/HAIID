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
    try: meals = data["items"]
    except: return data['message']
    day_meals = [m for m in meals if m['day']==1]

    return "<h1>" + str(day_meals) + "</h1>"

@app.route("/recipe_search_str=<string:query>/")
def recipe_search(query):
    response = api.search_recipes_complex(query)
    data = response.json()
    try: img = data['results'][0]['image']
    except: return data['message']
    return "<h1>" + str(img) + "</h1>"


@app.route("/get_growth_stage/<string:image>/")
def nn(image):
    return "RIPE TOMATO"


@app.route("/get_recipes")
def get_recipes():
    #inputs
    diet = request.args.get('diet', default='None', type = str)
    user_ingredients = request.args.get('userIngredients',default='flour,egg,milk,banana,honey,golden syrup,butter', type=str)
    allowed_missed_ingredients = request.args.get('allowMissed',default=2, type=int)
    num_recipes_wanted = request.args.get('recipesWanted',default=5, type=int)

    #return diet + user_ingredients+str(allowed_missed_ingredients)+str(num_recipes_wanted)

    valid_recipes = []
    #try:
    while len(valid_recipes) < num_recipes_wanted:
        rec_from_ingr = api.search_recipes_by_ingredients(user_ingredients).json()
        try:
            if rec_from_ingr['status'] == 'failure': return str(rec_from_ingr['message'])
        except: pass
        
        for rec in rec_from_ingr:
            if rec['missedIngredientCount'] <= allowed_missed_ingredients:
                if diet=='None':
                    valid_recipes.append(rec)
                else:
                    rec_details = api.get_recipe_information(rec['id']).json()
                    try:
                        if rec_details['status'] == 'failure': return str(rec_details['message'])
                    except: pass
                    
                    if diet in rec_details['diets']:
                        valid_recipes.append(rec)
    #except Exception as e:
        #return "Hi there " + str(e)
                    
                

    
    return str(valid_recipes)



#DEBUG MODE!!
##if __name__ == '__main__':
##    app.run(host='0.0.0.0', port=105, debug=True)
