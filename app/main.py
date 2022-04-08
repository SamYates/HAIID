from flask import Flask
from flask import request
import spoonacular
import cv2
import numpy as np
import os
from tensorflow import keras
from werkzeug.utils import secure_filename

API_KEY = "a80ce6a267f14f4f86a64efe027f6495"

app = Flask(__name__)
api = spoonacular.API(API_KEY)

#home_dir = os.path.expanduser("~")
UPLOAD_FOLDER = "/upload_images" #change to host directory
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#classifier = keras.models.load_model('classifierModel')

#strawberryModel = keras.models.load_model('strawberryModel')
#onionModel = keras.models.load_model('onionModel')
#carrotModel = keras.models.load_model('carrotModel')
#beetrootModel = keras.models.load_model('beetrootModel')
#cucumberModel = keras.models.load_model('cucumberModel')
#tomatoModel = keras.models.load_model('tomatoModel')
#potatoModel = keras.models.load_model('potatoModel')
#pepperModel = keras.models.load_model('pepperModel')
#modelArray = [beetrootModel, carrotModel, cucumberModel, onionModel, strawberryModel, tomatoModel] #potatoModel pepperModel

classNames = ["beetroot", "carrot", "cucumber", "onion", "strawberry", "tomato"] #potato pepper

@app.route("/")
def home_view():
    return "<h1>HAIID peep & STUFF! \n does this work YET</h1>"


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


@app.route("/get_growth_stage", methods = ['POST'])
def get_growth_stage():
    new_file = request.files['image']
    npimg = np.fromstring(new_file, np.uint8)
    image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    image = np.array([cv2.resize(image/255, (224, 224), interpolation = cv2.INTER_AREA)])
    
    return str(image)


@app.route("/get_recipes")
def get_recipes():
    #inputs
    diet = request.args.get('diet', default='None', type = str)
    user_ingredients = request.args.get('userIngredients',default='flour,egg,milk,banana,honey,golden syrup,butter', type=str)
    allowed_missed_ingredients = request.args.get('allowMissed',default=2, type=int)
    num_recipes_wanted = request.args.get('recipesWanted',default=5, type=int)
    #ADD TEST VALUES SO DONT CALL API!!!!!

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

##@app.route("/generate_meal_plan")
##def get_meal_plan():
##    time_frame = request.args.get('timeFrame', default='None', type = str)
##    diet = request.args.get('diet', default='None', type = str)
##    user_ingredients = request.args.get('userIngredients',default='flour,egg,milk,banana,honey,golden syrup,butter', type=str)
    


#DEBUG MODE!!
#if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=105, debug=True)
