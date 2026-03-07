"""
Seed script to populate the database with sample movies, actors, directors, and genres.
Called once on startup if the database is empty.
"""

from sqlalchemy.orm import Session
from models import Movie, Actor, Director, Genre


def seed_database(db: Session) -> None:
    """Insert sample data into the database if it's empty."""
    if db.query(Movie).count() > 0:
        return  # Already seeded

    # --- Genres ---
    genre_names = ["Action", "Drama", "Sci-Fi", "Thriller", "Comedy",
                   "Crime", "Adventure", "Romance", "Horror", "Animation"]
    genres: dict[str, Genre] = {}
    for name in genre_names:
        g = Genre(name=name)
        db.add(g)
        genres[name] = g

    # --- Directors ---
    nolan = Director(name="Christopher Nolan", bio="British-American filmmaker known for complex, cerebral storytelling.", birth_year=1970)
    spielberg = Director(name="Steven Spielberg", bio="Legendary Hollywood director with decades of iconic films.", birth_year=1946)
    fincher = Director(name="David Fincher", bio="Known for dark, meticulous thrillers and crime dramas.", birth_year=1962)
    scorsese = Director(name="Martin Scorsese", bio="Master of American cinema and crime dramas.", birth_year=1942)
    tarantino = Director(name="Quentin Tarantino", bio="Cult filmmaker known for non-linear storytelling and sharp dialogue.", birth_year=1963)
    villeneuve = Director(name="Denis Villeneuve", bio="Canadian director known for visually stunning sci-fi and thrillers.", birth_year=1967)
    anderson = Director(name="Wes Anderson", bio="Auteur known for symmetrical compositions and quirky storytelling.", birth_year=1969)
    peele = Director(name="Jordan Peele", bio="Horror director and social commentator.", birth_year=1979)

    for d in [nolan, spielberg, fincher, scorsese, tarantino, villeneuve, anderson, peele]:
        db.add(d)

    # --- Actors ---
    dicaprio = Actor(name="Leonardo DiCaprio", bio="Oscar-winning actor known for intense dramatic roles.", birth_year=1974)
    pitt = Actor(name="Brad Pitt", bio="Hollywood star known for versatile performances.", birth_year=1963)
    johansson = Actor(name="Scarlett Johansson", bio="One of the highest-paid actresses in Hollywood.", birth_year=1984)
    hardy = Actor(name="Tom Hardy", bio="British actor known for physically demanding roles.", birth_year=1977)
    blanchett = Actor(name="Cate Blanchett", bio="Award-winning actress known for transformative performances.", birth_year=1969)
    washington = Actor(name="Denzel Washington", bio="Acclaimed actor and director.", birth_year=1954)
    bale = Actor(name="Christian Bale", bio="British actor famous for extreme physical transformations.", birth_year=1974)
    gosling = Actor(name="Ryan Gosling", bio="Canadian actor known for dramatic and comedic range.", birth_year=1980)
    portman = Actor(name="Natalie Portman", bio="Harvard-educated Oscar-winning actress.", birth_year=1981)
    hanks = Actor(name="Tom Hanks", bio="America's beloved actor known for heartfelt performances.", birth_year=1956)
    neeson = Actor(name="Liam Neeson", bio="Irish actor known for action and dramatic roles.", birth_year=1952)
    cumberbatch = Actor(name="Benedict Cumberbatch", bio="British actor known for intelligent, complex characters.", birth_year=1976)
    damon = Actor(name="Matt Damon", bio="Oscar-winning actor and screenwriter.", birth_year=1970)
    mila = Actor(name="Mila Kunis", bio="Ukrainian-American actress known for comedy and drama.", birth_year=1983)

    for a in [dicaprio, pitt, johansson, hardy, blanchett, washington, bale, gosling,
              portman, hanks, neeson, cumberbatch, damon, mila]:
        db.add(a)

    db.flush()  # Assign IDs before building relationships

    # --- Movies ---
    movies_data = [
        {
            "title": "Inception",
            "release_year": 2010,
            "synopsis": "A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
            "rating": 8.8,
            "runtime_minutes": 148,
            "director": nolan,
            "genres": [genres["Action"], genres["Sci-Fi"], genres["Thriller"]],
            "actors": [dicaprio, hardy, johansson],
        },
        {
            "title": "The Dark Knight",
            "release_year": 2008,
            "synopsis": "When the menace known as the Joker wreaks havoc on Gotham, Batman must accept one of the greatest psychological tests of his ability to fight injustice.",
            "rating": 9.0,
            "runtime_minutes": 152,
            "director": nolan,
            "genres": [genres["Action"], genres["Crime"], genres["Drama"]],
            "actors": [bale, hardy],
        },
        {
            "title": "Interstellar",
            "release_year": 2014,
            "synopsis": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
            "rating": 8.6,
            "runtime_minutes": 169,
            "director": nolan,
            "genres": [genres["Sci-Fi"], genres["Adventure"], genres["Drama"]],
            "actors": [damon, blanchett],
        },
        {
            "title": "Fight Club",
            "release_year": 1999,
            "synopsis": "An insomniac office worker and a devil-may-care soap maker form an underground fight club that evolves into something much more.",
            "rating": 8.8,
            "runtime_minutes": 139,
            "director": fincher,
            "genres": [genres["Drama"], genres["Thriller"]],
            "actors": [pitt, blanchett],
        },
        {
            "title": "Se7en",
            "release_year": 1995,
            "synopsis": "Two detectives hunt a serial killer who uses the seven deadly sins as his motives.",
            "rating": 8.6,
            "runtime_minutes": 127,
            "director": fincher,
            "genres": [genres["Crime"], genres["Drama"], genres["Thriller"]],
            "actors": [pitt, washington],
        },
        {
            "title": "The Social Network",
            "release_year": 2010,
            "synopsis": "The story of the founding of Facebook and the resulting lawsuits.",
            "rating": 7.8,
            "runtime_minutes": 120,
            "director": fincher,
            "genres": [genres["Drama"]],
            "actors": [damon],
        },
        {
            "title": "Goodfellas",
            "release_year": 1990,
            "synopsis": "The story of Henry Hill and his life in the mob, covering his relationship with his wife Karen and his mob partners.",
            "rating": 8.7,
            "runtime_minutes": 146,
            "director": scorsese,
            "genres": [genres["Crime"], genres["Drama"]],
            "actors": [pitt],
        },
        {
            "title": "Pulp Fiction",
            "release_year": 1994,
            "synopsis": "The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.",
            "rating": 8.9,
            "runtime_minutes": 154,
            "director": tarantino,
            "genres": [genres["Crime"], genres["Drama"], genres["Thriller"]],
            "actors": [pitt, johansson],
        },
        {
            "title": "Django Unchained",
            "release_year": 2012,
            "synopsis": "With the help of a German bounty-hunter, a freed slave sets out to rescue his wife from a brutal plantation owner.",
            "rating": 8.4,
            "runtime_minutes": 165,
            "director": tarantino,
            "genres": [genres["Drama"], genres["Action"]],
            "actors": [dicaprio, washington],
        },
        {
            "title": "Arrival",
            "release_year": 2016,
            "synopsis": "A linguist works with the military to communicate with alien lifeforms after twelve mysterious spacecraft appear around the world.",
            "rating": 7.9,
            "runtime_minutes": 116,
            "director": villeneuve,
            "genres": [genres["Sci-Fi"], genres["Drama"], genres["Thriller"]],
            "actors": [blanchett],
        },
        {
            "title": "Blade Runner 2049",
            "release_year": 2017,
            "synopsis": "Young Blade Runner K's discovery of a long-buried secret leads him to track down former Blade Runner Rick Deckard.",
            "rating": 8.0,
            "runtime_minutes": 164,
            "director": villeneuve,
            "genres": [genres["Sci-Fi"], genres["Drama"], genres["Thriller"]],
            "actors": [gosling, damon],
        },
        {
            "title": "Dune",
            "release_year": 2021,
            "synopsis": "A noble family becomes embroiled in a war for control over the galaxy's most valuable asset.",
            "rating": 8.0,
            "runtime_minutes": 155,
            "director": villeneuve,
            "genres": [genres["Sci-Fi"], genres["Adventure"], genres["Drama"]],
            "actors": [cumberbatch],
        },
        {
            "title": "The Grand Budapest Hotel",
            "release_year": 2014,
            "synopsis": "A writer encounters the owner of an aging European hotel between the wars and hears his story about a legendary concierge.",
            "rating": 8.1,
            "runtime_minutes": 99,
            "director": anderson,
            "genres": [genres["Comedy"], genres["Adventure"]],
            "actors": [gosling, blanchett],
        },
        {
            "title": "Get Out",
            "release_year": 2017,
            "synopsis": "A young African-American visits his white girlfriend's parents for the weekend, where his simmering uneasiness eventually reaches a boiling point.",
            "rating": 7.7,
            "runtime_minutes": 104,
            "director": peele,
            "genres": [genres["Horror"], genres["Thriller"], genres["Drama"]],
            "actors": [washington],
        },
        {
            "title": "Us",
            "release_year": 2019,
            "synopsis": "A family's serene beach vacation turns to chaos when their doppelgängers appear and begin to terrorize them.",
            "rating": 6.8,
            "runtime_minutes": 116,
            "director": peele,
            "genres": [genres["Horror"], genres["Thriller"]],
            "actors": [johansson],
        },
        {
            "title": "Schindler's List",
            "release_year": 1993,
            "synopsis": "In German-occupied Poland during World War II, industrialist Oskar Schindler gradually becomes concerned for his Jewish workforce after witnessing their persecution by the Nazis.",
            "rating": 9.0,
            "runtime_minutes": 195,
            "director": spielberg,
            "genres": [genres["Drama"], genres["Crime"]],
            "actors": [neeson, blanchett],
        },
        {
            "title": "Saving Private Ryan",
            "release_year": 1998,
            "synopsis": "Following the Normandy Landings, a group of U.S. soldiers go behind enemy lines to retrieve a paratrooper whose brothers have been killed in action.",
            "rating": 8.6,
            "runtime_minutes": 169,
            "director": spielberg,
            "genres": [genres["Drama"], genres["Action"], genres["Adventure"]],
            "actors": [hanks, damon],
        },
        {
            "title": "The Revenant",
            "release_year": 2015,
            "synopsis": "A frontiersman fights for survival after being mauled by a bear in the 1820s wilderness.",
            "rating": 8.0,
            "runtime_minutes": 156,
            "director": scorsese,
            "genres": [genres["Action"], genres["Adventure"], genres["Drama"]],
            "actors": [dicaprio, hardy],
        },
        {
            "title": "La La Land",
            "release_year": 2016,
            "synopsis": "While navigating their careers in Los Angeles, a pianist and an actress fall in love while attempting to reconcile their aspirations for the future.",
            "rating": 8.0,
            "runtime_minutes": 128,
            "director": anderson,
            "genres": [genres["Drama"], genres["Romance"], genres["Comedy"]],
            "actors": [gosling, portman],
        },
        {
            "title": "Black Swan",
            "release_year": 2010,
            "synopsis": "A committed dancer struggles to maintain her sanity after winning the lead role in a production of Tchaikovsky's Swan Lake.",
            "rating": 8.0,
            "runtime_minutes": 108,
            "director": fincher,
            "genres": [genres["Drama"], genres["Thriller"], genres["Horror"]],
            "actors": [portman, mila],
        },
    ]

    for data in movies_data:
        movie = Movie(
            title=data["title"],
            release_year=data["release_year"],
            synopsis=data["synopsis"],
            rating=data["rating"],
            runtime_minutes=data["runtime_minutes"],
            director=data["director"],
            genres=data["genres"],
            actors=data["actors"],
        )
        db.add(movie)

    db.commit()
    print("✅ Database seeded successfully!")
