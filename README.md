remove author from categories if deleted
clean visual.js

[ ..not yet ..]
# Cookbook  
An online cookbook where users can post their recipes and vote on other recipes.

Recipes are searchable for parameters of country, cuisine, [most popular] and author.

## UX
The App uses Materialize collapsible menus for a simple and clear interface that works well on mobiles.
The color scheme is warm muted colors that are associated with food.
This App provides users with an easily searchable database of recipes. 
Users may provide and edit recipes.
As a recipe contains a lot of data, I tried to make the input form easy to use.
The input is broken into three sections; recipe details, ingredients and preparation.
The form is accordion style to be easy to use and less daunting.
A button provides additional input fields as required.

## Features

# Add Recipe
- Easy to use accordion style form with button for additional input fields

# Home 
- Choose a category to view recipe names.

# Recipes.html
- Display the recipe names in the selected category and allow user to choose one.

# Showrecipe.html
- Display the chosen recipe. Page has buttons to vote and edit.

# Visualize
- Provides two visualizations of the cookbook with d3 graphs

### Existing Features
- Searchability - Homepage allows user to choose a category by which to search for recipes
- Accordion style input form - enables user to focus on one part at a time.
- Adaptable input form - create-more-inputs button allows user to add more input lines as needed. 
- Vote and edit buttons - allow user to take action directly from the recipe page.
- Automatic categorization - ingredient list is parsed and recipe type derived from lists(*incomplete) as meat, vegan, vegatarian or fish.
- 


### Features Left to Implement
- user signin to edit recipes. Presently any user can edit any recipe.
- search for recipes by popularity.
- search by clicking on the graphs.

## Technologies Used

 all of the languages, frameworks, libraries, tools 
- [Flask] (http://flask.pocoo.org/)
    - microframework used for this project
- [MongoDB] (https://www.mongodb.com/)
    -  Project database with two collections
        - Recipes holds the details of each recipe.
        - Categories holds the values for each category.
- [Python 3] ( https://www.python.org/ )
    - This project is python driven.
- [Materialize 0.100.2] ( https://materializecss.com/ )
   - The styling library
- [JQuery](https://jquery.com)
    - Generates additional recipe input lines on add and edit forms
    - Submits valid form on Home page.
    - used for materialize collapsible menu
- [d3] (https://d3js.org/) . 
    - Used to draw the graphs on the visualize page
- [queue] (https://cdnjs.com/libraries/queue-async). 
    - Loads data from stored file for d3 use.
 


## Testing

### Tests

1. Home Page:
    1. Choosing any category item gives correct new page.
    
2. New Recipe:
    1. Empty form submit has no effect
    2. Submit form with blank cuisine field results in cuisine='not stated' value.
    3. Submit form with blank author/cuisine/country gives html5 message 'Please fill out this field'.
    4. Submit form with blank ingredient1/ingredient2 field gives same html5 message
    5. Submit form with blank instructions is allowed - this should be changed
    6. Submit form with empty ingredient/instructions field results in correct saving of details without empty fields.
    7. Submit form with 'recipename' already in db adds X to name i.e 'recipenameX'   

3. Edit Recipe:
    1. Submit form without 2 non-blank ingredient lines redirects to error page
    2. Submit form with empty ingredient/instructions field results in correct saving of details without empty fields.
    3. Submit form with blank instructions redirects to error page

### Devices
    - Tested on google inspect for different screen sizes. No issues found.

### Issues:
1. Bugs:
    1. Graphs on visualize page sometimes do not show updated information without a hard reset.
        This is a problem on c9 and heroku. Putting in a 5 second sleep between 
        updating the vav.csv file and rendering the page does not solve the issue.

## Deployment:

1. App deployed on Heroku :https://project4-cookbook.herokuapp.com/
2. Files created for this deployment: Procfile, requirements.txt.

## Credits

### Content
Recipes were obtained from:
- https://www.tasteofhome.com

Color palette inspired by:
- https://en.wikipedia.org/wiki/File:Color_star-en.svg
