# done - add recipe=insert and categories=update
#next - home = select by cuisine. author. all, ---popular
#  count views to recipe page
# add dc/d3 popular.top3 votes/views average-votes recipes-with-ingredient

import os
from flask import Flask, render_template, request, url_for, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)
app.config['MONGO_DATABASE'] ='mongo ds111623.mlab.com:11623/cookbook'
app.config['MONGO_URI'] = 'mongodb://root:root2pass@ds111623.mlab.com:11623/cookbook'

mongo = PyMongo(app)

#==================Functions x 6=============================================#
# extract_num(name, letter)  ------ get the number from eg ingredient5
# category_check(category, item) -- is item already in db-categories?
# extract_recipe(show) ------------ get the full recipe from db
# extract_category(show)----------- get all recipe names for specified category
# num_steps(recipe) --------------- find number of fields for ingredients/instructions
#    ""  return (ingreds, prep, steps)          and return fields as lists
# view_count(recipe) -------------- increment views field

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
    for cat in range(1,steps[0]+1):
        item = (str(cat), str(recipe['ingredients'][str(cat)]))
        ingreds.append(item)
    for cat in range(1,steps[1]+1):
        item = (str(cat), recipe['instructions'][str(cat)].encode('utf-8').strip())
        prep.append(item)
    return (ingreds, prep, steps)

def view_count(recipe):
    for category in recipe:             #########################needed?????????
        if category == "views":
            recipe['views'] = str(int(recipe['views']) + 1)
            recipes=mongo.db.recipes
            recipes.update( {'recipe_name' : recipe['recipe_name'] }, recipe)
            print("viewcount==", recipe)
   
#======================Views x 8=======================================================# 
# home()---------------- Form to select recipes to view by category------>home
# get_recipes()--------- Get recipes for chosen category----------------->recipes
# show_recipe()--------- Get chosen recipe ---------------------------...>showrecipe
# add_recipe() --------- Form to submit new recipe----------------------->addrecipe
# insert_recipe()------- Put new recipe in db collections---------------->addrecipe
# edit_recipe() -- ----- Form to edit selected recipe ------------------->editrecipe
# update_recipe() ------ Update recipe in db collection------------------>home
# vote()---------------- Add 1 to chosen recipe votes  ------------------>home
# get_stats()


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
    recipes = mongo.db.recipes.find()
    cats= [category for category in recipes]
    recipeNames=[]
    for cat in cats:
        recipeNames.append(cat['recipe_name'])
    #get categories   
    categories = mongo.db.categories.find()
    cats= [category for category in categories]
    return render_template('home.html', recipes=recipeNames, cats=cats)

@app.route('/vote', methods=['POST'])  
def vote():
    print("edit==", request.form['recipe'])
    recipe_name = request.form['recipe']
    vote = request.form['vote']
    show = ('recipe_name', recipe_name)
    recipe = extract_recipe(show)
    for category in recipe:
        if category == "votes":
            recipe['votes'] = str(int(recipe['votes']) + 1)
            recipes=mongo.db.recipes
            recipes.update( {'recipe_name' : recipe_name }, recipe)
    return redirect(url_for("home"))

@app.route('/edit_recipe', methods=['POST']) 
def edit_recipe():
    print("edit==", request.form['recipe'])
    show = ('recipe_name', request.form['recipe'])
    showrecipe = extract_recipe(show)
    lists= num_steps(showrecipe)
    ingreds = lists[0]
    prep = lists[1]
    steps = lists[2]
    return render_template('editrecipe.html', recipe=showrecipe, prep=prep, ingreds=ingreds, steps=steps)
   
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
            view_count(recipe)                                                  #####redirect?
            return render_template('showrecipe.html', recipe=recipe, steps=steps)####this
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
    #recipes=mongo.db.recipes.find()
    #categories=mongo.db.categories.find()
    return render_template('recipes.html', recipe_names=byCategory)

@app.route('/show_recipe', methods=['POST'])
def show_recipe():
    print("sr==", request.form)
    form = request.form.to_dict()
    cats= [category for category in form]
    steps = ()
    for cat in cats:
        print("sr-cat", cat)
        show = ('recipe_name', form['recipe_name'])
        recipe = extract_recipe(show)
        steps = num_steps(recipe)
    view_count(recipe)
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

@app.route('/update_recipe', methods=['POST'])
def update_recipe():
    form = request.form.to_dict()
    print("updateform==", form)
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
    show = ('recipe_name', form['recipe_name'])
    recipe = extract_recipe(show)
    print("update--recipe", recipe)
    form['cuisine'] = recipe['cuisine']
    form['country'] = recipe['country']
    form['author'] = recipe['author']
    form['votes'] = recipe['votes']
    print("update--form", form)
    recipes = mongo.db.recipes
    recipes.update( {'recipe_name' : form['recipe_name']}, form)
   
    return redirect(url_for("home")) 
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=os.environ.get('PORT'), debug=True)
    