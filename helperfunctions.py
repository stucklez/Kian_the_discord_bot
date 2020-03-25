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
    return movies

def get_quote(message):
    string_split = message.split(" ")
    string_split.remove('<3quote_add')
    string_split.remove('-')
    author = string_split[0]
    del string_split[0]
    quote = ""
    for i in string_split:
        quote += i
    return classes.Quote("", author, quote)