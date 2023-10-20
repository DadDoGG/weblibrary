from flask import request, redirect, url_for, render_template, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from sweater import app, db
from sweater.models import book, user, book_user, menu
from .forms import LoginForm, RegisterForm, EdditForm


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', current_user=current_user, menus=menu.query.all())


@app.route('/add-book', methods=['GET', 'POST'])
@login_required
def add_book():
    title = request.form['title']
    year_created = request.form['year_created']
    second_user = request.form.getlist('type[]')

    User = user.query.filter_by(id=current_user.id).first()
    books = book.query.filter_by(title=title).first()

    if not books:
        books = book(title=title, year_created=year_created)
        db.session.add(books)
        db.session.commit()

    association = book_user(book_id=books.id, user_id=User.id)
    db.session.add(association)
    db.session.commit()

    if second_user != 0:
        for i in second_user:
            second_association = book_user(book_id=books.id, user_id=i)
            db.session.add(second_association)
            db.session.commit()


    if current_user.permission == "User":
        current_user.permission = "author"
        db.session.commit()

    db.session.close()
    return redirect('/')


@app.route("/book/<int:id_book>")
def show_book(id_book):
    books = book.query.get(id_book)
    if books:
        authors = books.user
        author_ids = [user.id for user in authors]
        return render_template('book.html', books=books, authors=authors, author_ids=author_ids, current_user=current_user, menus=menu.query.all(), title=books.title)
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

    form = LoginForm()
    if form.validate_on_submit():
        User = user.query.filter_by(email=form.email.data).first()
        if User and check_password_hash(User.password, form.psw.data):
            rm = form.remember.data
            login_user(User, remember=rm)
            return redirect('/profile')
        else:
            flash("Неверная пара логин/пароль", "error")
    return render_template('login.html', menus=menu.query.all(), title='Авторизация', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("Вы успешно вышли из аккаунта", "success")
    return redirect('/login')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
            hash = generate_password_hash(form.psw.data)
            res = user(email=form.email.data, surname=form.surname.data, last_name=form.last_name.data, password=hash)
            db.session.add(res)
            db.session.commit()
            if res:
                flash("Вы успешно зарегистрированы", "success")
                return redirect(url_for('login'))
            else:
                flash("Ошибка при добавлении в БД", "error")

    return render_template("register.html", menus=menu.query.all(), form=form)


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
                    return "При редактировании произошла ошибка"
            else:
                return render_template('update.html', books=books, menus=menu.query.all())
        else:
            return "Вы не автор данной книги"


@app.route('/profile')
@login_required
def profile():
    authors = user.query.filter(user.permission == 'author', user.id != current_user.id).all()
    return render_template('profile.html', current_user=current_user, menus=menu.query.all(), authors=authors)

@app.route('/books')
def books():
    per_page = 10
    page = request.args.get('page', type=int, default=1)
    books = book.query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('all_books.html', menus=menu.query.all(), books=books, title="Книги")

@app.route('/search_book', methods=['GET', 'POST'])
def search_book():
    name = request.form['title']
    if request.method == 'POST' and name:

        return render_template('all_books.html', books=book.query.filter_by(title=name))


@app.route('/authors')
def authors_list():
    if current_user.is_anonymous or current_user.permission == "author" or current_user.permission == "User":
        authors = user.query.filter_by(permission='author')
    else:
        authors = user.query.all()
    return render_template('authors_list.html', menus=menu.query.all(), authors=authors, current_user=current_user)

@app.route("/authors/<int:id_user>")
def show_user(id_user):
    users = user.query.get(id_user)
    if users:
        books = users.book
        return render_template('author.html', users=users, books=books, current_user=current_user, menus=menu.query.all(), title="Автор")
    else:
        return "Книга не найдена", 404


@app.route("/authors/<int:id_user>/del")
@login_required
def delete_author(id_user):
    users = user.query.get_or_404(id_user)
    if users:
        if current_user.permission == "admin" or current_user == users:
            try:
                books = users.book
                books_to_delete = []
                for book in books:
                    authors = book.user
                    if len(authors) == 1 and users in authors:
                        books_to_delete.append(book)
                for book in books_to_delete:
                    db.session.delete(book)

                db.session.delete(users)
                db.session.commit()
                db.session.close()
                flash("Вы успешно удалили профиль", "success")
                return redirect('/')
            except Exception:
                return "При удалении произошла ошибка"
        else:
            return "Вы не автор данной книги"


@app.route("/authors/<int:id_user>/upd", methods=['GET', 'POST'])
@login_required
def update_author(id_user):
    users = user.query.get(id_user)
    if request.method == 'GET':
        form = EdditForm(user=users)
    elif request.method == 'POST':
        form = EdditForm()
    else:
        return 405
    if users:
        if current_user.permission == "admin" or current_user == users:
            if form.validate_on_submit():
                users.email = form.email.data
                users.surname = form.surname.data
                users.last_name = form.last_name.data

                try:
                    db.session.commit()
                    db.session.close()
                    return redirect('/')
                except Exception:
                    return "При редактировании произошла ошибка"
            else:
                return render_template('update_auth.html', users=users, menus=menu.query.all(), form=form)
        else:
            return "Вы не пользователь данного профиля"