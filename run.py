import os
from flask import Flask, render_template, request, url_for, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import search


app = Flask(__name__)
app.config['MONGO_DATABASE'] ='mongo ds111623.mlab.com:11623/cookbook'
app.config['MONGO_URI'] = 'mongodb://root:root2pass@ds111623.mlab.com:11623/cookbook'

mongo = PyMongo(app)

@app.route('/')
@app.route('/add_recipe')
def add_recipe():
    return render_template('addrecipe.html')

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
    categories = "categories"
    return render_template('home.html', what=categories)

@app.route('/get_recipes')
def get_recipes():
    return render_template('recipes.html', recipes=mongo.db.recipes.find())

@app.route('/insert_recipe', methods=['POST'])
def insert_recipes():
    searchable = {}
    recipes = mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    searchable['recipe'] = request.form['recipe_name']
    searchable['author'] = request.form['author']
    searchable['country'] = request.form['country']
    searchable['cuisine'] = request.form['cuisine']
    search.insert(searchable)
    return redirect(url_for("get_recipes"))    
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=os.environ.get('PORT'), debug=True)
    