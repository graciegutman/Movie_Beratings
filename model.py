from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
import correlation 


engine = create_engine("sqlite:///ratings.db", echo=False)
s = scoped_session(sessionmaker(
                                bind=engine,
                                autocommit = False,
                                autoflush = False))

# SQLalchemy introspection magic
Base = declarative_base()
Base.query = s.query_property()

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

    # returns dictionary of movie ratings for self
    def dictionary_creation(self):
        u_ratings = {}
        for r in self.ratings:
            u_ratings[r.movie_id] = r # r is the rating object for movie corresponding to movie_id

        return u_ratings

    # We are creating a dictionary every time this function is called. 
    # This bothers me. I would rather pass in a dictionary. 
    
    # u_ratings = dict, other = one other user object
    def similarity(self, u_ratings, other):
        paired_ratings = []

        for r in other.ratings:
            u_r = u_ratings.get(r.movie_id)
            if u_r:
                paired_ratings.append((u_r.rating, r.rating))

        if paired_ratings:
            return correlation.pearson(paired_ratings)
        else:
            return 0.0

    def predict_rating(self, movie):
        other_ratings = s.query(Rating).filter_by(movie_id=movie.id).all() # list of rating objects
        u_dict = self.dictionary_creation()
        similarities = [(self.similarity(u_dict, r.user), r) \
            for r in other_ratings]
        similarities.sort(reverse=True)
        # filter out negative similarities
        similarities = [sim for sim in similarities if sim[0] > 0]

        # This is shit. 
        if not similarities:
            return None
        # unpack tuple in this list comprehension
        numerator = sum([r.rating * similarity for similarity, r in similarities])
        denominator = sum([similarity[0] for similarity in similarities])
        return numerator/denominator


class Movie(Base):

    __tablename__ = "movies"
    id = Column(Integer, ForeignKey("ratings.movie_id"), primary_key=True)
    name = Column(String(64), nullable=True)
    released_at = Column(DateTime, nullable=True)
    imdb_url = Column(String(64), nullable=True)

    rating = relationship("Rating", backref=backref("movies", order_by=id))

class Rating(Base):

    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    rating = Column(Integer, nullable=True)

    user = relationship("User",
            backref=backref("ratings", order_by=id))

def new_user(email, password, age, zipcode):
    # check if email already in database
    # if so, return "that email is already in our system"
    # if not, make new user
    # return true
    user_object = s.query(User).filter_by(email=email).all()
    if user_object != []:
        print "That email has already been registered."
        return "That email has already been registered."
    # add object to session
    new_user = User(
                    email=email,
                    password=password,
                    age=int(age), 
                    zipcode=zipcode)
    
    s.add(new_user)
    s.commit()
    print "Email successfully registered!"
    return "Email successfully registered!"

def update_rating(movie_rating_object, rating):
    movie_rating_object.rating = rating
    s.commit()
    return "Rating successfully updated."

def new_rating(movie_id, user_id, rating):
    new_rating = Rating(
                    movie_id=movie_id,
                    user_id=user_id,
                    rating=rating
                    )
    s.add(new_rating)
    s.commit()
    return "New movie rating added."

def authenticate(email, password):
    # session.query(model.Movie).filter_by(title = "Aladdin").first()

    user_object = s.query(User).filter_by(email=email).first()

    if user_object:
        correct_password = user_object.password

        if hash(password) == int(correct_password):
            print user_object.email, user_object.id
            return (user_object.email, user_object.id)
    else: 
        return None



### End class declarations
## code is now outside this function in first lines. 
# def connect():
#     global ENGINE
#     global Session
#     ENGINE = create_engine("sqlite:///ratings.db", echo=True)
#     Session = sessionmaker(bind=ENGINE)

#     return Session()


def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
