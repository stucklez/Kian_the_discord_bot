import classes as classes
import shlex
import random

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
        movies.append(classes.Movie(i["_id"], i["Title"], i["Genre"], i["Year"], i["Server"]))
    return movies

def get_quote(message):
    string_split = message.split(" ")
    string_split.remove('<3quote_add')
    string_split.remove('-')
    author = string_split[0]
    del string_split[0]
    quote = ""
    for i in string_split:
        quote += i + " "
    return classes.Quote("", author, quote)

def get_movie(message):
    string_split = shlex.split(message)
    string_split.remove('<3add_movie')
    movie = classes.Movie("", string_split[0], string_split[1].lower(), int(string_split[2]), 0)
    return movie

def choose_by_genre(movies, server_id):
    server_movies = []
    for i in movies:
        if i.server == server_id:
            server_movies.append(i)
    if len(server_movies) > 0:
        return random.choice(server_movies)
    else:
        return None