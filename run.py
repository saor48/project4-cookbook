# done - add recipe=insert and categories=update
#next - home = select by cuisine. author. all, ---popular
# add vote buttom and count views to recipe page
# add dc/d3 popular.top3 votes/views average-votes recipes-with-ingredient

import os
from flask import Flask, render_template, request, url_for, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import search

app = Flask(__name__)
app.config['MONGO_DATABASE'] ='mongo ds111623.mlab.com:11623/cookbook'
app.config['MONGO_URI'] = 'mongodb://root:root2pass@ds111623.mlab.com:11623/cookbook'

mongo = PyMongo(app)

#==================Functions x 3=============================================#

def extract_num(name, letter):
    if name[-2] == letter:
        i = name[-1]
    else:
        i= name[-2] + name[-1]
    return i

def category_check(category, item):
    categories = mongo.db.categories.find()
    cats= [cat for cat in categories]
    for cat in cats:
        items = cat[category]
        print("ck=1=", cats)
        print("ck=2=", cat)
        if item not in items:
            items.append(item)
            print("ck=3i=", items)
    return items
    
def extract_recipe(show):
    recipe_name = show[1]
    recipes=mongo.db.recipes.find()
    cats= [category for category in recipes]
    print("ex==1-",show)
    showrecipe = ['no dinner']
    for recipe in cats:
        if recipe_name == recipe['recipe_name']:
            print("ex==rs",recipe)
            showrecipe = recipe
            return showrecipe
    return showrecipe
    
def extract_category(show):
    recipes=mongo.db.recipes.find()
    cats= [category for category in recipes]
    print("exc==show,cats",show, cats)
    showrecipe = ['no dinner']
    for recipe in cats:
        print("exc==recipe==",recipe)
        if show[0] == 'cuisine':
            if show[1] == recipe['cuisine']:
                print("exc==r-nc",recipe['recipe_name'])
                showrecipe.append(recipe['recipe_name'])
        elif show[0] == 'author':
            if show[1] == recipe['author']:
                showrecipe.append(recipe['recipe_name'])
        elif show[0] == 'country':
            if show[1] == recipe['country']:
                showrecipe.append(recipe['recipe_name'])
    return showrecipe

def num_steps(recipe):
    ingreds = []
    prep = []
    num_ingredients = 0
    num_instructions = 0
    for cat in recipe:
        if cat == 'ingredients':
            num_ingredients = len(recipe['ingredients'])
        if cat == 'instructions':
            num_instructions = len(recipe['instructions'])
    steps=(num_ingredients, num_instructions)
    print("steps======",steps)
    for cat in range(1,steps[0]+1):
        print("steps======",str(cat), str(recipe['ingredients'][str(cat)]))
        item = (str(cat), str(recipe['ingredients'][str(cat)]))
        ingreds.append(item)
    for cat in range(1,steps[1]+1):
        print("steps======",str(cat), recipe['instructions'][str(cat)].encode('utf-8'))
        item = (str(cat), recipe['instructions'][str(cat)].encode('utf-8').strip())
        prep.append(item)
    return (ingreds, prep)
#======================Views x 5=======================================================# 
# add_recipe() --------- Form to submit new recipe
# insert_recipe()------- Put new recipe in db collections= recipes and categories
# home()---------------- Form to select recipes to view by category
# get_stats()
# get_recipes()--------- Get recipes for chosen category
# show_recipe()--------- Display the recipe
## get-recipes works with extract 1 recipe, cuisines
### now do for authors, popular
## showrecipe.html for full recipe display- improve display


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
    #get recipe names
    categories = mongo.db.recipes.find()
    cats= [category for category in categories]
    recipes=[]
    for cat in cats:
        recipes.append(cat['recipe_name'])
        recipes=recipes
    #get categories   
    categories = mongo.db.categories.find()
    cats= [category for category in categories]
    return render_template('home.html', recipes=recipes, cats=cats)
    
@app.route('/get_stats')
def get_stats():
    stats = "stats"
    return render_template('home.html', what=stats)

@app.route('/get_recipes', methods=['POST'])
def get_recipes():
    byCategory = []
    print("rf==", request.form)
    form = request.form.to_dict()
    # change from flat to nested json
    cats= [category for category in form]
    print("gr-cats", cats)
    for cat in cats:
        print("gr-cat", cat)
        if 'recipe_name' in cat:
            show = ('recipe_name', form['recipe_name'])
            recipe=extract_recipe(show)
            steps=num_steps(recipe)
            return render_template('showrecipe.html', recipe=recipe, steps=steps)
        elif 'cuisine' in cat:
            show = ('cuisine', form['cuisine'])
            byCategory=extract_category(show)
            print("byCuisine", byCategory)
        elif 'author' in cat:
            show = ('author', form['author'])
            byCategory=extract_category(show)
            print("byAuthor", byCategory)
        elif 'country' in cat:
            show = ('country', form['country'])
            byCategory=extract_category(show)
            print("byCountry", byCategory)
        else:
            show = 'blnk'
    print("show", show)
    recipes=mongo.db.recipes.find()
    categories=mongo.db.categories.find()
    return render_template('recipes.html', recipe_names=byCategory)

@app.route('/show_recipe', methods=['POST'])
def show_recipe():
    print("sr==", request.form)
    form = request.form.to_dict()
    # change from flat to nested json
    cats= [category for category in form]
    steps = ()
    for cat in cats:
        print("sr-cat", cat)
        show = ('recipe_name', form['recipe_name'])
        recipe=extract_recipe(show)
        steps = num_steps(recipe)
    return render_template('showrecipe.html', recipe=recipe, steps=steps)
    

@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    form = request.form.to_dict()
    # change from flat to nested json
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
    #insert in recipes
    recipes = mongo.db.recipes
    recipes.insert_one(form)
    #insert in categories
    cuisines = category_check('cuisine', form['cuisine'])
    authors = category_check('author', form['author'])
    countries = category_check('country', form['country'])
    mongo.db.categories.update( {},
                    {  'cuisine' : cuisines,
                       'author' : authors,
                       'country' : countries
                    } 
            )
    return redirect(url_for("add_recipe"))    
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=os.environ.get('PORT'), debug=True)
    