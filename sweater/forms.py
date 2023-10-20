from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[Email("Некорректный email")])
    psw = PasswordField("Пароль: ", validators=[DataRequired(),
                                                Length(min=4, max=100, message="Пароль должен быть от 4 до 100 символов")])
    remember = BooleanField("Запомнить", default=False)
    submit = SubmitField("Войти")

class RegisterForm(FlaskForm):
    surname = StringField("Фамилия: ", validators=[Length(min=4, max=100, message="Имя должно быть от 4 до 100 символов")])
    last_name = StringField("Имя: ", validators=[Length(min=4, max=100, message="Имя должно быть от 4 до 100 символов")])
    email = StringField("Email: ", validators=[Email("Некорректный email")])
    psw = PasswordField("Пароль: ", validators=[DataRequired(),
                                                Length(min=4, max=100, message="Пароль должен быть от 4 до 100 символов")])

    psw2 = PasswordField("Повтор пароля: ", validators=[DataRequired(), EqualTo('psw', message="Пароли не совпадают")])
    submit = SubmitField("Регистрация")

class EdditForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(EdditForm, self).__init__(*args, **kwargs)
        user = kwargs.get("user")
        if user:
            self.surname.data = user.surname
            self.last_name.data = user.last_name
            self.email.data = user.email

    surname = StringField("Фамилия: ",
                              validators=[Length(min=4, max=100, message="Имя должно быть от 4 до 100 символов")])
    last_name = StringField("Имя: ",
                                validators=[Length(min=4, max=100, message="Имя должно быть от 4 до 100 символов")])
    email = StringField("Email: ", validators=[Email("Некорректный email")])
    submit = SubmitField("Изменить")