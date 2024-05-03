"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
dbx = db.session.execute


class User(db.Model):
    """User model"""

    __tablename__ = "users"

    id = db.mapped_column(
        db.Integer,
        db.Identity(),
        primary_key=True,
    )

    first_name = db.mapped_column(
        db.String(50),
        nullable=False,
    )

    last_name = db.mapped_column(
        db.String(50),
        nullable=False
    )

    img_url = db.mapped_column(
        db.String(500)
    )

    @property
    def full_name(self):
        """ Generate full name from user's first and last names."""

        return f"{self.first_name} {self.last_name}"
