class Quote:
    _id = ""
    author = ""
    quote = ""

    def __init__(self, id, name, iquote):
        self._id = id
        self.author = name
        self.quote = iquote

class Movie:
    _id = ""
    title = ""
    genre = ""
    year = 0
    server = ""

    def __init__(self, id, title, genre, year, server):
        self._id = id
        self.title = title
        self.genre = genre
        self.year = year
        self.server = server
