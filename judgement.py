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
    if session.get('email'):
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
        new_user_created = model.new_user(email, hash(password), age, zipcode)

        if new_user_created:
            flash("SUCCESSSSS")
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

@app.route("/ratings/<user_id>")
def ratings(user_id):
    rating_list = model.s.query(model.Rating).limit(10).all()
    return render_template("rating_list.html", rating_list=rating_list)


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
