from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, EqualTo, Length, Regexp

from .models import User


class RegisterForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=4, max=25), Regexp("^[a-zA-Z0-9_]+$")]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=4, max=25)]
    )
    confirm = PasswordField(
        "Confirm",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match")],
    )

    def validate(self, extra_validators=None):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False

        user = User.query.filter_by(username=self.username.data).first()

        if user:
            self.username.errors.append("User already registered")
            return False

        if self.password.data != self.confirm.data:
            self.password.errors.append("Passwords must match")
            return False

        return True
    

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])