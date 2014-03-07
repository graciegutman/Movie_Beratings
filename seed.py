import model
import csv
import datetime

def load_users(session):
    # use u.user
    # open the file
    f = open("seed_data/u.user")

    for raw_line in f:
        # parse and clean up the line
        line = raw_line.split('|')
        clean_line = [x.strip().decode("latin-1") for x in line]
        # create object
        # must interact with model.py somehow
        new_user = model.User(age=clean_line[1], zipcode=clean_line[4])
        # add object to session
        session.add(new_user)

    # commit
    session.commit()

def load_movies(session):
    # use u.item
    # open the file
    f = open("seed_data/u.item")

    for raw_line in f:
        # parse and clean up the line
        line = raw_line.split('|')
        clean_line = [x.strip().decode("latin-1") for x in line]

        # freaking release dates are with the titles
        # This is dumb. If only we knew how to use Regex. 
        original_name_and_release_date = clean_line[1]
        for i in range(len(original_name_and_release_date)):
            # MAGIC for Scream of Stone (Schrei aus Stein) (1991). What?
            if original_name_and_release_date[i] in ["("]:
                name = original_name_and_release_date[:i-1]

        # create object
        if clean_line[2]:
            datetime_format = datetime.datetime.strptime(clean_line[2], "%d-%b-%Y")
        new_movie = model.Movie(name=name, released_at=datetime_format, imdb_url=clean_line[4])
        # add object to session
        session.add(new_movie)
    # commit
    session.commit()

def load_ratings(session):
    # use u.data
    # open the file
    f = open("seed_data/u.data")

    for raw_line in f:
        # parse and clean up the line
        line = raw_line.split()
        clean_line = [x.strip().decode("latin-1") for x in line]
        # create object
        # must interact with model.py somehow
        new_rating = model.Rating(movie_id=clean_line[1], user_id=clean_line[0], rating=clean_line[2])
        # add object to session
        session.add(new_rating)
    # commit
    session.commit()

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    # load_users(s)
    load_movies(s)
    # load_ratings(s)

if __name__ == "__main__":
    s = model.connect()
    main(s)
