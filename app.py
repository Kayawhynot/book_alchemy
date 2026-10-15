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
    return render_template('add_author.html')
