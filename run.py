# nodinner select error
import os
from flask import Flask, render_template, request, url_for, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from time import sleep
import csv, json

app = Flask(__name__)
app.config['MONGO_DATABASE'] ='mongo ds111623.mlab.com:11623/cookbook'
app.config['MONGO_URI'] = 'mongodb://root:root2pass@ds111623.mlab.com:11623/cookbook'

mongo = PyMongo(app)

#line=================Functions x 10=============================================#
#26 meal_type(recipe) --------------- check ingredients for meat and dairy
#47 extract_num(name, letter)  ------ get the number from eg ingredient5
#58 category_check(category, item) -- add item to list if not in db-categories?
#67 category_remove_author(author) -- remove author from list 
#64 extract_recipe(show) ------------ get the full recipe from db
#86 extract_category(show)----------- get all recipe names for specified category
#93 num_steps(recipe) --------------- find number of fields for ingredients/instructions
#    ..  return (ingreds, prep, steps)          and return fields as lists
#112 view_count(recipe) -------------- increment views field
#122 remove_blanks(adict) ------------ remove blank fields from input forms
#129 name_check(item): --------------- Add X to recipe name if already in db

def meal_type(recipe):
    # these lists are not complete
    meat = ['beef', 'chicken', 'lamb', 'pork', 'mutton', 'venison', 'veal', 'turkey']
    dairy = ['milk', 'cheese', 'yogurt', 'egg']
    fish = ['fish', 'salmon']
    # set value for field 'vegan' if ingredient in lists.
    ingreds = recipe['ingredients']
    meal = 'vegan'
    for d in dairy:
        for item in ingreds:
            if d in ingreds[item]:
                meal = 'vegetarian'
    for m in meat:
        for item in ingreds:
            if m in ingreds[item]:
                meal = 'meat'
    for f in fish:
        for item in ingreds:
            if f in ingreds[item]:
                meal = 'fish'
    
    return meal

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
        if item not in items and item != '':
            items.append(item)
            print("ck=3i=", items)
    return items
    
def category_remove_author(author):
    categories = mongo.db.categories.find()
    cats= [cat for cat in categories]
    for cat in cats:
        cat['author'].remove(author)
        print("cra=author=", cat['author'])
    return cat['author']
    
def extract_recipe(show):
    recipe_name = show[1]
    recipes=mongo.db.recipes.find()
    cats= [category for category in recipes]
    showrecipe = []
    for recipe in cats:
        if recipe_name == recipe['recipe_name']:
            showrecipe = recipe
            return showrecipe
    return showrecipe
    
def extract_category(show):
    recipes=mongo.db.recipes.find()
    cats= [category for category in recipes]
    showrecipes = []
    for recipe in cats:
        if show[0] == 'cuisine':
            if show[1] == recipe['cuisine']:
                showrecipes.append(recipe['recipe_name'])
        elif show[0] == 'author':
            if show[1] == recipe['author']:
                showrecipes.append(recipe['recipe_name'])
                print("exc==show",show)
        elif show[0] == 'country':
            if show[1] == recipe['country']:
                showrecipes.append(recipe['recipe_name'])
    return showrecipes

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
            recipe['views'] = str(int(recipe['views']) + 1)
            recipes=mongo.db.recipes
            recipes.update( {'recipe_name' : recipe['recipe_name'] }, recipe)

def remove_blanks(adict):
    blanks = 0
    newdict = {}
    for i in range(1,len(adict)+1):
        if adict[str(i)] != "":
                index = str(i-blanks)
                newdict[index] = adict[str(i)]
        else :
                blanks += 1
    return newdict

def name_check(item):
    recipes=mongo.db.recipes.find()
    cats= [category for category in recipes]
    for cat in cats:
        name = cat['recipe_name']
        if name.lower() == item.lower():
            item += "X"
            print("ck=X=", item)
    return item    
#line======================Views x 10=====================================8 x pages=========# 
#172 home()---------------- Form to select recipes to view by category------>home
#208 get_recipes()--------- Get recipes for chosen category----------------->recipes
#237 show_recipe()--------- Get chosen recipe ---------------------------...>showrecipe
#164 add_recipe() --------- Form to submit new recipe----------------------->addrecipe
#251 insert_recipe()------- Put new recipe in db collections---------------->addrecipe
#197 edit_recipe() -- ----- Form to edit selected recipe ------------------->editrecipe
#292 update_recipe() ------ Update recipe in db collection------------------>home
#186 vote()---------------- Add 1 vote to chosen recipe   ------------------>home
#145 visual() ------------- View charts of cookbook db --------------------->visual
#328 delete_recipe() ------ Delete recipe from db -------------------------->delete/home/errors

@app.route('/visual')
def visual():
    pointer=mongo.db.recipes.find()
    recipes = [category for category in pointer]
   
    with open("static/data/vav.csv", "w") as vav:
        heading = "views"+","+"votes"+","+"name"+","+"vegan"
        vav.writelines(heading+ "\n")
    with open("static/data/vav.csv", "a") as vav:
        for recipe in recipes:
            views = recipe['views']
            votes = recipe['votes']
            name = recipe['recipe_name']
            vegan = recipe['vegan']
            vav.writelines( views+","+votes+","+name+","+vegan+ "\n")
 # need delay here ? sleep(5)
    return render_template('visual.html')

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
    recipe_name = request.form['recipe']
    vote = request.form['vote']
    show = ('recipe_name', recipe_name)
    recipe = extract_recipe(show)
    recipe['votes'] = str(int(recipe['votes']) + 1)
    recipes=mongo.db.recipes
    recipes.update( {'recipe_name' : recipe_name }, recipe)
    return redirect(url_for("home"))

@app.route('/edit_recipe', methods=['POST']) 
def edit_recipe():
    show = ('recipe_name', request.form['recipe'])
    showrecipe = extract_recipe(show)
    lists= num_steps(showrecipe)
    ingreds = lists[0]
    prep = lists[1]
    steps = lists[2]
    return render_template('editrecipe.html', recipe=showrecipe, prep=prep, ingreds=ingreds, steps=steps)

@app.route('/get_recipes', methods=['POST'])
def get_recipes():
    byCategory = []
    form = request.form.to_dict()
    # change from flat to nested json
    cats= [category for category in form]
    if cats:
        for cat in cats:
            if 'recipe_name' in cat:
                show = ('recipe_name', form['recipe_name'])
                recipe=extract_recipe(show)
                steps=num_steps(recipe)
                view_count(recipe)                                                  #####redirect?
                return render_template('showrecipe.html', recipe=recipe, steps=steps)####this
            elif 'cuisine' in cat:
                show = ('cuisine', form['cuisine'])
                byCategory=extract_category(show)
            elif 'author' in cat:
                show = ('author', form['author'])
                byCategory=extract_category(show)
            elif 'country' in cat:
                show = ('country', form['country'])
                byCategory=extract_category(show)
    else:
        return redirect(url_for("home"))
   
    return render_template('recipes.html', recipe_names=byCategory)

@app.route('/show_recipe', methods=['POST'])
def show_recipe():
    print("sr==", request.form)
    form = request.form.to_dict()
    cats= [category for category in form]
    steps = ()
    if len(cats) == 0 :
        return redirect(url_for("home"))
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
            ingredients[i] = form[cat]
            del form[cat]
        if "instruction" in cat:
            i = extract_num(cat, 'n')
            instructions[i] = form[cat]
            del form[cat]    
    form['ingredients'] = remove_blanks(ingredients)
    form['instructions'] = remove_blanks(instructions)
    if len(form['ingredients']) < 2:
        error_message = "--> Insufficient Ingredients - Edit Denied  <--"
        return render_template('errors.html', error=error_message )
    if len(form['instructions']) < 1:
        error_message = "--> Insufficient Instructions - Edit Denied  <--"
        return render_template('errors.html', error=error_message )
    form['views'] = "0"
    form['votes'] = "0"
    form['vegan'] = meal_type(form)
    if form.get('cuisine') == None :
        form['cuisine'] = "not stated"
    form['recipe_name'] = name_check(form['recipe_name'])
    #insert in recipes
    recipes = mongo.db.recipes
    recipes.insert_one(form)
    #update categories
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
    print("ur--", form)
    # change from flat to nested json
    cats= [category for category in form]
    ingredients = {}
    instructions = {}
    for cat in cats:
        if "ingredient" in cat:
            i = extract_num(cat, 't')
            ingredients[i] = form[cat].strip()
            del form[cat]
        if "instruction" in cat:
            i = extract_num(cat, 'n')
            instructions[i] = form[cat].strip()
            del form[cat] 
    
    form['ingredients'] = remove_blanks(ingredients)
    form['instructions'] = remove_blanks(instructions)
    if len(form['ingredients']) < 2:
        error_message = "--> Insufficient Ingredients - Edit Denied  <--"
        return render_template('errors.html', error=error_message )
    if len(form['instructions']) < 1:
        error_message = "--> Insufficient Instructions - Edit Denied  <--"
        return render_template('errors.html', error=error_message )
    
    #del form['action']
    #insert in recipes
    show = ('recipe_name', form['recipe_name'])
    recipe = extract_recipe(show)
    form['cuisine'] = recipe['cuisine']
    form['country'] = recipe['country']
    form['author'] = recipe['author']
    form['votes'] = recipe['votes']
    form['views'] = recipe['views']
    form['vegan'] = meal_type(form)
    print("update--form", form)
    recipes = mongo.db.recipes
    recipes.update( {'recipe_name' : form['recipe_name']}, form)
   
    return redirect(url_for("home")) 

@app.route('/delete_recipe', methods=['POST'])    
def delete_recipe():
    print("rf--", request.form)
    form = request.form.to_dict()
    name=""
    oid=""
    # showrecipe form = "name", "id", "author"
    # delete form = "name", "same_name", oid", "delete", "author"
    if 'delete' not in form:
            name = form["name"]
            oid = form["id"]
            author = form["author"]
    if 'delete' in form:
        if form['name'].lower() == form['same_name'].lower():
            show = ('author', form['author'])
            same_author_recipes = extract_category(show)
            if len(same_author_recipes) == 1:
                authors = category_remove_author(form['author'])
                 #update categories
                cuisines = category_check('cuisine', '')
                countries = category_check('country', '')
                mongo.db.categories.update( {},
                    {  'cuisine' : cuisines,
                       'author' : authors,
                       'country' : countries
                    } 
                )
            deleted = mongo.db.recipes.delete_one({'_id':ObjectId(form['oid'])})
            return redirect(url_for("home"))
        else:
            error_message = "--> Names do not match. Deletion denied <--"
            return render_template('errors.html', error=error_message )
   
    return render_template('delete.html', delete_name=name, oid=oid, author=author)
    
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=os.environ.get('PORT'), debug=True)
    