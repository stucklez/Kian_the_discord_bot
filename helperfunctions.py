import classes as classes
def initquotes(quotes_col):
    kian = []
    mongo = list(quotes_col.find())
    for i in mongo:
        kian.append(classes.Quote(i["_id"], i["Author"], i["Quote"]))
    return kian

def initmovies(movies_col):
    movies = []
    mongo = list(movies_col.find())
    for i in mongo:
        movies.append(classes.Movie(i["_id"], i["Title"], i["Genre"], i["Year"]))
        movies.append(classes.Movie(i["_id"], i["Title"], i["Genre"], i["Year"]))
    return movies