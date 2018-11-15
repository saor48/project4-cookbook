no dinner = showrecipe fail
add required to instructions?
use id for edit and vote not nme.


[ ..not yet ..]
# Cookbook  
An online cookbook where users can post and vote on recipes.

Recipes are searchable for parameters of country, cuisine, [most popular] and author.
Users can also edit their own recipes using their [password].

## UX
This App provides users with an easily searchable database of recipes. 
The App allows also users to provide and edit a recipe.
As a recipe contains a lot of data, I tried to make the input form easy to use.
The input is broken into three sections; recipe details, ingredients and preparation.
The form is accordion style to be easy to use and less daunting.
A button provides additional input fields as required.
Searching also uses the same accordion style.

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
- Automatic categorization - ingredient list is parsed and recipe type derived from lists as meat, vegan, vegatarian or fish
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

In this section, you need to convince the assessor that you have conducted enough testing to legitimately believe that the site works well. Essentially, in this part you will want to go over all of your user stories from the UX section and ensure that they all work as intended, with the project providing an easy and straightforward way for the users to achieve their goals.

Whenever it is feasible, prefer to automate your tests, and if you've done so, provide a brief explanation of your approach, link to the test file(s) and explain how to run them.

For any scenarios that have not been automated, test the user stories manually and provide as much detail as is relevant. A particularly useful form for describing your testing process is via scenarios, such as:


1. Home Page:
    1. Choosing any category item gives correct new page.
    
2. New Recipe:
    1. Empty form submit has no effect
    2. Submit form with blank cuisine field results in cuisine='not stated' value.
    3. Submit form with blank author/cuisine/country gives html5 message 'Please fill out this field'.
    4. Submit form with blank ingredient1/ingredient2 field gives same html5 message
    5. Submit form with blank instructions is allowed - this should be changed
    6. Submit form with empty ingredient/instructions field results in correct saving of details without empty fields.
    7. 

3. Edit Recipe:
    1. Submit form without 2 non-blank ingredient lines redirects to error page
    2. Submit form with empty ingredient/instructions field results in correct saving of details without empty fields.
    3. Submit form with blank instructions is allowed - this should be changed

=================

In addition, you should mention in this section how your project looks and works on different browsers and screen sizes.

You should also mention in this section any interesting bugs or problems you discovered during your testing, even if you haven't addressed them yet.

If this section grows too long, you may want to split it off into a separate file and link to it from here.

## Deployment

This section should describe the process you went through to deploy the project to a hosting platform (e.g. GitHub Pages or Heroku).

In particular, you should provide all details of the differences between the deployed version and the development version, if any, including:
- Different values for environment variables (Heroku Config Vars)?
- Different configuration files?
- Separate git branch?

In addition, if it is not obvious, you should also describe how to run your code locally.


## Credits

### Content
Recipes were obtained from:
- https://www.tasteofhome.com

Color palette inspired by:
- https://en.wikipedia.org/wiki/File:Color_star-en.svg
