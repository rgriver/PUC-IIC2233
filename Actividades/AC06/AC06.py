from datetime import datetime as dt

def set_id():
    i = 0
    while True:
        yield i
        i += 1


class Cast:
    def __init__(self, movie_title, name, character):
        self.name = name
        self.movie = movie_title
        self.character = character


class Movie:
    get_id = set_id()

    def __init__(self, title, rating, release, *args):
        self.id = next(Movie.get_id)
        self.title = title
        self.rating = float(rating)
        self.release = dt.strptime(release, '%Y-%m-%d')  # 2015-03-04
        self.genres = args#[]

def popular(movies, num):
    return list(filter(lambda m: m.rating >= num, movies))

def with_genres(movies, num):
    return list(filter(lambda m: len(m.genres) >= num, movies))

def tops_of_genre(movies, genre):
    genre_movies = filter(lambda m: genre in m.genres, movies)
    sorted_movies = sorted(map(lambda x: x.rating, genre_movies))
    sorted_movies_x = sorted_movies[len(sorted_movies) - 10:len(sorted_movies)]
    top = filter(lambda x: x.rating in list(sorted_movies_x), movies)
    return top

def actor_rating(movies, casts, actor):
    actor_casts = filter(lambda c: c.name == actor, casts)
    actor_movie_names = list(map(lambda c: c.movie, actor_casts))
    actor_movies = filter(lambda m: m.title in actor_movie_names, movies)
    ratings = list(map(lambda x: x.rating, actor_movies))
    average_rating = sum(ratings)/len(ratings)
    return average_rating

def compare_actors(movies, casts, actor_a, actor_b):
    rat_a = actor_rating(movies, casts, actor_a)
    rat_b = actor_rating(movies, casts, actor_b)
    if rat_a > rat_b:
        return actor_a
    else:
        return actor_b

def movies_of(casts, name):
    return filter(lambda c: c.name == name, casts)

def from_year(movies, year):
    return filter(lambda m: str(m.release)[0:4] == str(year), movies)

if __name__ == "__main__":
    with open('movies.txt', 'r') as f:
        stripped = map(lambda l: l.strip(), f)
        info = map(lambda l: list(l.split(',')), stripped)
        movies = list(map(lambda i: Movie(i[1], i[2], i[3], *list(i[4:])), info))

    with open('cast.txt', 'r') as f:

        stripped = map(lambda l: l.strip(), f)
        info = map(lambda l: list(l.split(',')), stripped)
        casts = list(
            map(lambda i: Cast(i[0], i[1], i[2]), info))

    '''
    for p in with_genres(movies, 3):
        print(p.title, p.genres)

    for p in tops_of_genre(movies, 'Action'):
        print(p.title, p.genres)

    for p in from_year(movies, 2017):
        print(p.title, p.release)

    for p in movies_of(casts, 'Anna Kendrick'):
        print(p.name, p.movie)

    '''

    #print(compare_actors(movies, casts, 'Anna Kendrick', 'Gwyneth Paltrow'))