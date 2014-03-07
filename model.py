from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref


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
