from flask import request, redirect, url_for, render_template, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from sweater import app, db
from sweater.models import book, user, book_user, menu


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', current_user=current_user, menus=menu.query.all())


@app.route('/add-book', methods=['GET', 'POST'])
@login_required
def add_book():
    title = request.form['title']
    year_created = request.form['year_created']
    User = user.query.filter_by(id=current_user.id).first()

    books = book.query.filter_by(title=title).first()
    if not books:
        books = book(title=title, year_created=year_created)
        db.session.add(books)
        db.session.commit()

    association = book_user(book_id=books.id, user_id=User.id)
    db.session.add(association)
    db.session.commit()

    users = user.query.get(current_user.id)
    if users.permission == "User":
        users.permission = "author"
        db.session.commit()
        db.session.close()

    return redirect('/')


@app.route("/book/<int:id_book>")
def show_book(id_book):
    books = book.query.get(id_book)
    if books:
        authors = books.user
        author_ids = [user.id for user in authors]
        return render_template('book.html', books=books, authors=authors, author_ids=author_ids, current_user=current_user, menus=menu.query.all())
    else:
        return "Книга не найдена", 404


@app.route("/book/<int:id_book>/del")
@login_required
def delete_book(id_book):
    books = book.query.get_or_404(id_book)
    if books:
        users = books.user
        user_id = current_user.id
        is_user_of_book = any(user.id == user_id for user in users)
        if current_user.permission == "admin" or is_user_of_book:
            try:
                db.session.delete(books)
                db.session.commit()
                db.session.close()
                return redirect('/')
            except Exception:
                return "При удалении произошла ошибка"
        else:
            return "вы не автор данной книги"


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/profile')
    else:
        email = request.form.get('email')
        password = request.form.get('password')

        if email and password:
            User = user.query.filter_by(email=email).first()

            if User and check_password_hash(User.password, password):
                rm = True if request.form.get('remain') else False
                login_user(User, remember=rm)

                return redirect('/profile')
            else:
                flash("Логин или пароль заполнены неверно")

        return render_template('login.html', menus=menu.query.all())


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("Вы успешно вышли из аккаунта", "success")
    return redirect('/login')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        if len(request.form['password']) > 4 and request.form['password'] == request.form['password2']:
            hash = generate_password_hash(request.form['password'])
            res = user(email=request.form['email'], surname=request.form['surname'], last_name=request.form['last_name'],
                       password=hash)
            db.session.add(res)
            db.session.commit()
            if res:
                flash("Вы успешно зарегестрированы", "success")
                return redirect(url_for('login'))
            else:
                flash("Ошибка при добавлении в БД", "error")
        else:
            flash("Неверно заполнены поля", "error")
    db.session.close()

    return render_template('register.html', menus=menu.query.all())


@app.route("/book/<int:id_book>/upd", methods=['GET', 'POST'])
@login_required
def update_book(id_book):
    books = book.query.get(id_book)
    if books:
        users = books.user
        user_id = current_user.id
        is_user_of_book = any(user.id == user_id for user in users)
        if current_user.permission == "admin" or is_user_of_book:
            if request.method=="POST":
                books.title = request.form['title']
                books.year_created = request.form['year_created']

                try:
                    db.session.commit()
                    db.session.close()
                    return redirect('/')
                except Exception:
                    return "при редактировании произошла ошибка"
            else:
                return render_template('update.html', books=books, menus=menu.query.all())
        else:
            return "вы не автор данной книги"


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', current_user=current_user, menus=menu.query.all())

@app.route('/books')
def books():
    return render_template('all_books.html', menus=menu.query.all(), books=book.query.all())

@app.route('/authors')
def authors_list():
    return render_template('authors_list.html', menus=menu.query.all(), authors=user.query.all())

@app.route("/authors/<int:id_user>")
def show_user(id_user):
    users = user.query.get(id_user)
    if users:
        books = users.book
        return render_template('author.html', users=users, books=books, current_user=current_user, menus=menu.query.all())
    else:
        return "Книга не найдена", 404


@app.route("/authors/<int:id_user>/del")
@login_required
def delete_author(id_user):
    users = user.query.get_or_404(id_user)
    if users:
        if current_user.permission == "admin" or current_user == users:
            try:
                db.session.delete(users)
                db.session.commit()
                db.session.close()
                return redirect('/')
            except Exception:
                return "При удалении произошла ошибка"
        else:
            return "вы не автор данной книги"


@app.route("/authors/<int:id_user>/upd", methods=['GET', 'POST'])
@login_required
def update_author(id_user):
    users = user.query.get(id_user)
    if users:
        if current_user.permission == "admin" or current_user == users:
            if request.method=="POST":
                users.email = request.form['email']
                users.surname = request.form['surname']
                users.last_name = request.form['last_name']

                try:
                    db.session.commit()
                    db.session.close()
                    return redirect('/')
                except Exception:
                    return "при редактировании произошла ошибка"
            else:
                return render_template('update_auth.html', users=users, menus=menu.query.all())
        else:
            return "вы не автор данной книги"

