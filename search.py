

def insert(searchable):
    cuisine = []
    author = []
    country = []
    popular = []
    
    categories = [1][2] # mongo.db.categories
    
    if len(categories) > 0:
        cuisine = categories['cuisine']
        if searchable['cuisine'] not in cuisine:
            cuisine.append(searchable['cuisine'])
        author = categories['author']
        if searchable['author'] not in author:
            author.append(searchable['author'])
        country = categories['country']
        if searchable['country'] not in country:
            country.append(searchable['country']) 
        popular = categories['recipe']
        if searchable['recipe'] not in popular:
            popular.append(searchable['recipe'])
    else:
        cuisine.append(searchable['cuisine'])
        author.append(searchable['author'])
        country.append(searchable['country'])
        popular.append(searchable['recipe'])
    
    categories.insert(
        { 
            'cuisine' : cuisine, 
            'author' : author,
            'country' : country,
            'popular' : popular
        }
    )