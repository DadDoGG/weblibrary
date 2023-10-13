from flask import request, redirect, url_for, render_template

from sweater import app, db
from sweater.models import Books, Authors, Relation

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html', books=Books.query.all(), authors=Authors.query.all())

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    title = request.form['title']
    god_vipuska = request.form['god_vipuska']
    surname = request.form['surname']
    initials = request.form['initials']

    book = Books.query.filter_by(title=title).first()
    if not book:
        book = Books(title=title, god_vipuska=god_vipuska)
        db.session.add(book)
        db.session.commit()

    author = Authors.query.filter_by(surname=surname).first()
    if not author:
        author = Authors(surname=surname, initials=initials)
        db.session.add(author)
        db.session.commit()

    association = Relation(book_id=book.id, author_id=author.id)
    db.session.add(association)
    db.session.commit()

    return redirect(url_for('index'))

@app.route("/book/<int:id_book>")
def showBook(id_book):
    book = Books.query.get(id_book)
    if book is not None:
        return render_template('book.html', book=book)
    else:
        return "Книга не найдена", 404

@app.route("/book/<int:id_book>/del")
def deleteBook(id_book):
    book = Books.query.get_or_404(id_book)
    try:
        db.session.delete(book)
        db.session.commit()
        return redirect('/index')
    except:
        return "При удалении произошла ошибка"

