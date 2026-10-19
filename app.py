import os
from datetime import datetime

from flask import Flask, request, render_template, redirect, url_for

from data_models import db, Author, Book

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'data/library.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"

db.init_app(app)


# with app.app_context(): db.create_all()

@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """Show the form for a new author (GET) and save it to the DB (POST)."""
    message = None
    if request.method == 'POST':
        author_name = request.form.get('name')
        author_dob = request.form.get('birthdate')
        author_dod = request.form.get('date_of_death')
        author_dob = datetime.strptime(author_dob, '%Y-%m-%d').date()
        if author_dod == '':
            author_dod = None
        else:
            author_dod = datetime.strptime(author_dod, '%Y-%m-%d').date()

        new_author = Author(
            name=author_name,
            birth_date=author_dob,
            date_of_death=author_dod,
        )
        db.session.add(new_author)
        db.session.commit()
        message = (
            'Thanks :) - Your author has successfully '
            'been added to the DB!'
        )
    return render_template(
        'add_author.html',
        message=message,
    )


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """Show the form for a new book (GET) and save it to the DB (POST)."""
    message = None
    if request.method == 'POST':
        title = request.form.get('title')
        isbn = request.form.get('isbn') or None
        publication_year = int(request.form.get('publication_year'))
        author_id = int(request.form.get('author_id'))

        new_book = Book(
            title=title,
            isbn=isbn,
            publication_year=publication_year,
            author_id=author_id,
        )
        db.session.add(new_book)
        db.session.commit()
        message = (
            'Thanks :) - Your book has been added '
            'successfully to the DB!'
        )

    authors = Author.query.all()
    return render_template(
        'add_book.html',
        authors=authors,
        message=message,
    )


@app.route('/')
def home():
    """Search for keyword in TITLE, sort by ID, TITLE, AUTHOR """
    search = request.args.get('search')
    sort = request.args.get('sort')
    message = request.args.get('message')

    if search:
        books = Book.query.filter(Book.title.like(f'%{search}%')).all()
    elif sort == 'title':
        books = Book.query.order_by(Book.title).all()
    elif sort == 'author':
        books = Book.query.join(Author).order_by(Author.name).all()
    elif sort == 'id':
        books = Book.query.order_by(Book.id).all()
    else:
        books = Book.query.all()
    return render_template(
        'home.html',
        books=books,
        search=search,
        message=message,
    )


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """Delete the book with the given ID and redirect to the home page."""
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for(
        'home',
        message='Your book with the ID '
                f'{book_id} has been deleted.')
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
