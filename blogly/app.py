"""Blogly application."""

import os

from flask import Flask, request, flash, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import NotFound

from models import db, dbx, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_ECHO'] = True
db.init_app(app)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "i-will-never-tell")
print("secret key=", app.config['SECRET_KEY'])

debug = DebugToolbarExtension(app)


@app.get("/")
def redirect_to_users():
    """Redirect to user list"""

    return redirect("/users")


@app.get("/users")
def show_user_list():
    """Show user list"""

    return render_template("users.jinja")


@app.get("/users/new")
def show_add_user_form():
    """ Show new user form."""

    return render_template("new_user_form.jinja")


@app.post("/users/new")
def add_user_from_form():
    """ Process the add form, add new user to db, and redirect to /users. """

    first_name = request.form['first_name']
    last_name = request.form['last_name'] or None
    img_url = request.form['user_image'] or None

    user = User(
        first_name=first_name,
        last_name=last_name,
        img_url=img_url
    )
    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.get("/users/<int:user_id>")
def show_user_detail(user_id):
    """ Show information about given user. """

    q = (
        db.select(User)
        .where(User.id == user_id)
    )

    user = dbx(q).scalar().first()

    # will handle an invalid user_id
    if user == None:
        flash("User not found :-(")
        return redirect("/")

    else:
        user_name = user.get_full_name()
        img_url = user.img_url
        return render_template(
            "user_detail.jinja", user_name=user_name, img_url=img_url)


@app.get("/users/<int:user_id>/edit")
def show_edit_page(user_id):
    """ Show the edit page for a user. """

    return render_template("edit_profile.jinja", )
