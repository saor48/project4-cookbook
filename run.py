import os
from flask import Flask, render_template, request, url_for, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import search

app = Flask(__name__)
app.config['MONGO_DATABASE'] ='mongo ds111623.mlab.com:11623/cookbook'
app.config['MONGO_URI'] = 'mongodb://root:root2pass@ds111623.mlab.com:11623/cookbook'

mongo = PyMongo(app)

def extract_num(name, letter):
    if name[-2] == letter:
        i = name[-1]
    else:
        i= name[-2].append(name[-1])
    return i

@app.route('/')
@app.route('/add_recipe')
def add_recipe():
    categories = mongo.db.categories.find()
    cats= [category for category in categories]
    for cat in cats:
        cuisines = cat['cuisine']
    return render_template('addrecipe.html', cuisines=cuisines)

@app.route('/')
@app.route('/home')
def home():
    home="home"
    return render_template('home.html', what=home)
    
@app.route('/get_stats')
def get_stats():
    stats = "stats"
    return render_template('home.html', what=stats)
    
@app.route('/get_categories')
def get_categories():
    categories = mongo.db.categories.find()
    
    cats= [category for category in categories]
    print("cats==",cats)
    for cat in cats:
        cuisine = cat['cuisine']
    print("cuisine==",cuisine)
    return render_template('home.html', what=cuisine)

@app.route('/get_recipes')
def get_recipes():
    return render_template('recipes.html', recipes=mongo.db.recipes.find())

@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    form = request.form.to_dict()
    cats= [category for category in form]
    ingredients = {}
    instructions = {}
    for cat in cats:
        if "ingredient" in cat:
            i = extract_num(cat, 't')
            if form[cat] != "":
                ingredients[i] = form[cat]
            del form[cat]
        if "instruction" in cat:
            i = extract_num(cat, 'n')
            if form[cat] != "":
                instructions[i] = form[cat]
            del form[cat]    
    form['ingredients'] = ingredients
    form['instructions'] = instructions
    #del form['action']
    print(form)
    recipes = mongo.db.recipes
    recipes.insert_one(form)
    return redirect(url_for("add_recipe"))    
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=os.environ.get('PORT'), debug=True)
    