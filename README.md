searchable- lists
  recipe-name, author, cuisine, 
addrecipe - buttons materialise

[ ..not yet ..]
# Cookbook  
An online cookbook where users can post and vote on recipes.

Recipes are searchable for parameters of country, cuisine, [most popular] and author.
Users can also edit their own recipes using their [password].

## UX
This App provides users with an easily searchable database of recipes. 
The App allows also users to provide and edit a recipe.
As a recipe contains a lot of data, I want to make the input form easy to use.
The input is broken into three sections; recipe details, ingredients and preparation.
The form is accordion style to be easy to use and less daunting.
A button provides additional input fields as required.

## Features

# Input Form
- Easy to use accordion style form with button for additional input fields

# Home 
- Choose a category then sub-category to view recipe names.

# Recipes.html
- Display the recipe names in the selected categories and allow user to choose one.

# Showrecipe.html
- Display the chosen recipe. Page has buttons to vote and edit.

# Stats
- Analyse the various categories with d3/dc graphs

### Existing Features
- Searchability - Homepage allows user to choose a category by which to search for recipes
- Accordion style input form - enables user to focus on one part at a time.
- Adaptable input form - create-more-inputs button allows user to add more input lines as needed. 
- Vote and edit buttons - allow user to take action directly from the recipe page.

### Features Left to Implement
- Allergens / Vegan etc info
- user signin
- 

## Technologies Used

 all of the languages, frameworks, libraries, tools 
- [Python 3] ( https://www.python.org/ )
    - This project is python driven.
- [Materialize 0.100.2] ( https://materializecss.com/ )
   - The styling framework
- [JQuery](https://jquery.com)
    - The project uses **JQuery** to simplify DOM manipulation.
- [d3] (https://d3js.org/) . 
    - Used indirectly through dc.
- [crossfilter] (http://square.github.io/crossfilter/)
    - Prepares the data for dc
- [dc] (https://cdnjs.com/libraries/dc)
    - Used to draw the graphs on the stats page
- [queue] (https://cdnjs.com/libraries/queue-async). 
    - Loads data from stored files for dc use.
 


## Testing

In this section, you need to convince the assessor that you have conducted enough testing to legitimately believe that the site works well. Essentially, in this part you will want to go over all of your user stories from the UX section and ensure that they all work as intended, with the project providing an easy and straightforward way for the users to achieve their goals.

Whenever it is feasible, prefer to automate your tests, and if you've done so, provide a brief explanation of your approach, link to the test file(s) and explain how to run them.

For any scenarios that have not been automated, test the user stories manually and provide as much detail as is relevant. A particularly useful form for describing your testing process is via scenarios, such as:

1. Contact form:
    1. Go to the "Contact Us" page
    2. Try to submit the empty form and verify that an error message about the required fields appears
    3. Try to submit the form with an invalid email address and verify that a relevant error message appears
    4. Try to submit the form with all inputs valid and verify that a success message appears.

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
