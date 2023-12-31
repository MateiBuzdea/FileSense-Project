from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

from .models import Document
from app.accounts.models import User


class UploadForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()])
