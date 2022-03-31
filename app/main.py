from flask import Flask
#import spoonacular

#API_KEY = "a80ce6a267f14f4f86a64efe027f6495"

app = Flask(__name__)
#api = spoonacular.API(API_KEY)



@app.route("/")
def home_view():
    return "<h1>HAIID peep PEEPS!</h1>"

@app.route("/diet=:dietstring")
def get_meal_plan(dietstring):
    response = api.generate_meal_plan(diet=dietstring)
    data = response.json()
    meals = data["items"]
    day_meals = [m for m in meals if m['day']==1]

    return "<h1>" + str(day_meals) + "</h1>"
    
