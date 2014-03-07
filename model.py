from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker

ENGINE = None
Session = None

# SQLalchemy introspection magic
Base = declarative_base()

### Class declarations go here
class User(Base):
    # instances of this class will be stored in a table named "users"
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable=True)
    password = Column(String(64), nullable=True)
    age = Column(Integer, nullable=True)
    # gender = Column(Integer, nullable=True)
    zipcode = Column(String(15), nullable=True)

class Movie(Base):

    __tablename__ = "movies"
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=True)
    released_at = Column(DateTime, nullable=True)
    imdb_url = Column(String(64), nullable=True)

    # al = session.query(model.Movie).filter_by(title = "Aladdin").first()
    # al = s.query(Movie).filter_by("id<5").all() <-- syntax shit
    # al = s.query(Movie).filter("id<5").all()

al = s.query(Movie).filter(Movie.name.in_(s.query(Movie.name).filter(Movie.name.like('B%')))).all()
al = s.query(Movie).filter(Movie.released_at.like("1992%")).all()




al = s.query(Movie).filter(Movie.released_at.in_(s.query(Movie.released_at).filter("1970 < Movie.released_at[0] < 1973")).all()

class Rating(Base):

    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, nullable=True)
    user_id = Column(Integer, nullable=True)
    rating = Column(Integer, nullable=True)


### End class declarations

def connect():
    global ENGINE
    global Session
    ENGINE = create_engine("sqlite:///ratings.db", echo=True)
    Session = sessionmaker(bind=ENGINE)

    return Session()


def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
