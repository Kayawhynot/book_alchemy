from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    """Represent an author in the library Database."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    date_of_death = db.Column(db.Date, nullable=True)


class Book(db.Model):
    """Represent a book in the library database, written by one author."""
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String, nullable=True)
    title = db.Column(db.String, nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    author_id = db.Column(
        db.Integer,
        db.ForeignKey('author.id'),
        nullable=False,
    )
    author = db.relationship('Author', backref='books')
