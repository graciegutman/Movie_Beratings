from flask import Flask, render_template
import model

app = Flask(__name__)

@app.route("/")
def index():
    user_list = model.s.query(model.User).limit(10).all()
    html = render_template("user_list.html", user_list=user_list)
    print html
    return html



# rendering templates
# our model
# acces to the 'request' object (for forms)
# the ability to redirect
# debug mode








if __name__ == "__main__":
    app.run(debug=True)
