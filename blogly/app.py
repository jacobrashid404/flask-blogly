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
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
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
        user_name = user.full_name
        img_url = user.img_url
        return render_template(
            "user_detail.jinja", user_name=user_name, img_url=img_url)


@app.get("/users/<int:user_id>/edit")
def show_edit_page(user_id):
    """ Show the edit page for a user. """

    q = (
        db.select(User)
        .where(User.id == user_id)
    )

    user = dbx(q).scalar().first()

    # will handle an invalid user_id
    # TODO: check whether we need to validate any form data further
    if user == None:
        flash("User not found :-(")
        return redirect("/")

    else:
        user_id = user.id
        first_name = user.first_name
        last_name = user.last_name
        img_url = user.img_url
        return render_template(
            "edit_profile.jinja", first_name=first_name, last_name=last_name, img_url=img_url, user_id=user_id)


@app.post("/users/<int:user_id>/edit")
def process_edit_form(user_id):
    """Process edit user form => Get data from form and update database
    with new user information"""

    q = (
        db.select(User)
        .where(User.id == user_id)
    )

    user = dbx(q).scalar().first()

    # will handle an invalid user_id
    if user == None:
        flash("User not found :-(")

    else:
        # get form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        img_url = request.form['img_url']

        # update database with new values
        user.first_name = first_name
        user.last_name = last_name
        user.img_url = img_url

        flash(f"User details for {user.full_name} updated.")

        db.session.commit()

    return redirect("/")


@app.post("/users/<int:user_id>/delete")
def delete_user(user_id):
    """ Delete the user data and redirect to /users page. """

    q = (
        db.select(User)
        .where(User.id == user_id)
    )

    user = dbx(q).scalar().first()

    # handle invalid user_id
    if user == None:
        flash("Nice try! You can't delete a nonexistent user.")

    else:
        db.session.delete(user)
        flash("User successfully deleted.")

    return redirect("/users")
