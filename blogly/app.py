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

    q = (
        db.select(User)
    )
    users = dbx(q).scalars().all()

    return render_template("users.jinja", users=users)


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

    user = db.get_or_404(User, user_id)

    return render_template(
        "user_detail.jinja", user=user)


@app.get("/users/<int:user_id>/edit")
def show_edit_page(user_id):
    """ Show the edit page for a user. """

    user = db.get_or_404(User, user_id)

    # will handle an invalid user_id
    # TODO: check whether we need to validate any form data further
    return render_template(
        "edit_profile.jinja", user=user)


@app.post("/users/<int:user_id>/edit")
def process_edit_form(user_id):
    """Process edit user form => Get data from form and update database
    with new user information"""

    user = db.get_or_404(User, user_id)

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

    user = db.get_or_404(User, user_id)

    db.session.delete(user)
    db.session.commit()
    
    flash("User successfully deleted.")

    return redirect("/users")
