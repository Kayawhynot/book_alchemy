from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book
import os
from datetime import datetime

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"

db.init_app(app)


# with app.app_context(): db.create_all()

@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
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

        new_author = Author(name=author_name, birth_date=author_dob, date_of_death=author_dod)
        db.session.add(new_author)
        db.session.commit()
        message = 'Thanks :) - Your author has successfully been added to the DB!'
    return render_template('add_author.html', message=message)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    message = None
    if request.method == 'POST':
        title = request.form.get('title')
        isbn = request.form.get('isbn') or None
        publication_year = int(request.form.get('publication_year'))
        author_id = int(request.form.get('author_id'))

        new_book = Book(title=title, isbn=isbn,publication_year=publication_year, author_id=author_id)
        db.session.add(new_book)
        db.session.commit()
        message = 'Thanks :) - Your book has been added successfully to the DB'

    authors = Author.query.all()
    return render_template('add_book.html', authors=authors, message=message)


@app.route('/')
def home():
    search = request.args.get('title')
    sort = request.args.get('sort')
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
    return render_template('home.html', books=books)