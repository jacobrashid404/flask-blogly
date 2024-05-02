"""Seed users db with data."""

from app.import app
from models import db, User

app.app_context().push()

db.drop_all()
db.create_all()
