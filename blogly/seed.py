"""Seed users db with data."""

from app import app
from models import db, User

app.app_context().push()

db.drop_all()
db.create_all()

captain = User(
    first_name = "Captain",
    last_name = "Planet",
    img_url = "https://static1.srcdn.com/wordpress/wp-content/uploads/Captain-Planet-1.jpeg"
)

test_user_one = User(
    first_name = "Firstname",
    last_name = "Lastname",
    img_url = "#"
)

db.session.add_all([captain, test_user_one])
db.session.commit()


