from flask import request, redirect, url_for, render_template

from sweater import app, db
from sweater.models import Books


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', Books=Books.query.all)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    title = request.form['title']
    god_vipuska = request.form['god_vipuska']

    db.session.add(Books(title, god_vipuska))
    db.session.commit()

    return redirect(url_for('/'))