from flask import Flask, render_template, redirect, session, url_for, request, flash
import model

app = Flask(__name__)
app.secret_key = "whytheactualfuckdoweneedthis"

@app.route("/")
def index():
    html = render_template("index.html")
    return html

@app.route("/", methods=["POST"])
def process_login():
    email = request.form.get("email")
    password = request.form.get("password")

    if model.authenticate(email, password):
        user_email, user_id = model.authenticate(email, password)
        if email != None:
            flash ("Welcome, %s!" % str(user_email))
            session['user_id'] = user_id # put user_id into the session rather than email
    else:
        flash("Authentication failed.")

    return redirect(url_for("index"))

@app.route("/register")
def register():
    # purpose of this is solely to check whether a user is already logged in
    # get 'email' cookie from session
    if session.get('user_id'):
        flash("You're logged in already.")
        return redirect(url_for("index"))
    else: 
        return redirect(url_for("create_account"))

@app.route("/create_account")
def create_account():
    return render_template('register.html')

@app.route("/create_account", methods=["POST"])
def process_create_account():
    password = request.form.get("password")
    password_verify = request.form.get("password_verify")

    if password == password_verify:
        email = request.form.get("email")
        age = request.form.get("age")
        zipcode = request.form.get("zipcode")
        # returns a string
        new_user_created = model.new_user(email, hash(password), age, zipcode)

        if new_user_created:
            # new_user_created is a string that indicates whether 
            # new user was created or user already exists in database
            flash(new_user_created)
            return redirect(url_for('index'))
        else:
            flash("FAAAAAIL")
            return redirect(url_for('index'))

    else:
        flash("Passwords do not match.")
        return redirect(url_for('create_account'))

@app.route("/all_users")
def all_users():
    user_list = model.s.query(model.User).limit(10).all()
    return render_template("user_list.html", user_list=user_list)

# list of movies rated by user_id
@app.route("/ratings/<user_id>")
def ratings(user_id):
    rating_list = model.s.query(model.Rating).filter_by(user_id=user_id).limit(10).all()
    return render_template("rating_list_by_user.html", rating_list=rating_list)

# when logged in and viewing a record for a movie
# add or update a personal rating for that movie

@app.route("/movie/<movie_id>")
def movie(movie_id):
    rating_list = model.s.query(model.Rating).filter_by(movie_id=movie_id).all()
    if session.get('user_id'):
        movie = model.s.query(model.Movie).get(movie_id)
        rating_nums = []
        user_rating = None

        for r in rating_list:
            # assign user_rating to logged in user's rating object
            if r.user_id == session['user_id']:
                user_rating = r
            rating_nums.append(r.rating)
        
        avg_rating = float(sum(rating_nums)) / len(rating_nums)
        # Prediction code: only predict if the user hasn't rated it.
        user = model.s.query(model.User).get(session['user_id'])
        prediction = None

        # only makes prediction if there is no existing rating from user
        if not user_rating:
            prediction = user.predict_rating(movie)
            effective_rating = prediction
        else:
            effective_rating = user_rating.rating

        the_eye = model.s.query(model.User).filter_by(email="eye@aol.com").one()
        eye_rating = model.s.query(model.Rating).filter_by(user_id=the_eye.id, 
                                                    movie_id=movie.id).first()
        if not eye_rating:
            eye_rating = the_eye.predict_rating(movie)
        else:
            eye_rating = eye_rating.rating

        if not eye_rating:
            beratement = "There is insufficient data for me to berate you."
        else: 
            difference = abs(eye_rating - effective_rating)
            messages = [ "I suppose you don't have bad taste after all.",
                "I regret every decision that I've ever made that has brought me to listen to your opinion.",
                "Words fail me, as your taste in movies has clearly failed you.",
                "That movie is great. For a clown to watch. Idiot.",
                "I don't even"]
            beratement = messages[int(difference)]
        # end prediction
        # return render_template("movie.html", movie=movie, average=avg_rating, user_rating=user_rating, prediction=prediction)
        return render_template("rating_list_by_movie_logged_in.html",
                                rating_list=rating_list, 
                                movie=movie, 
                                average=avg_rating, 
                                user_rating=user_rating, 
                                prediction=prediction,
                                beratement=beratement)
    else:
        return render_template("rating_list_by_movie.html", rating_list=rating_list)


@app.route("/movie/<movie_id>", methods=["POST"])
def movie_rating_update(movie_id):
    user_id = session.get('user_id')
    rating = request.form.get("rating")
    movie_rating_object = model.s.query(model.Rating).filter_by(user_id=user_id).first()
    # if rating already exists, update rating
    if movie_rating_object:
        # updates database and returns a string
        msg = model.update_rating(movie_rating_object, rating)
        flash(msg)
        return redirect(url_for('movie', movie_id=movie_id))
    # else create new object for database
    else: 
        # updates database with new rating and returns a string
        msg = model.new_rating(movie_id, user_id, rating)
        flash(msg)
        return redirect(url_for('movie', movie_id=movie_id))




# eventually create page listing all movies in database
# @app.route("/movies")
# def movie():
#     movie_list = 

# create page for viewing movie with all ratings
# if logged in and viewing a movie, 
# be able to add or update rating via form
# first check if user's rating exists. if it does, do whatever to update it
# 


# clear session
@app.route("/logout")
def clear_session():
    session.clear()
    return redirect(url_for('index'))


# rendering templates
# our model
# acces to the 'request' object (for forms)
# the ability to redirect
# debug mode








if __name__ == "__main__":
    app.run(debug=True)
