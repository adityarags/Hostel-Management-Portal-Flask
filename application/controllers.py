from flask import render_template
from flask import current_app as app
from flask_security import login_required


@app.route("/", methods = ["GET", "POST"])
@login_required
def home():
    return render_template("index.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
