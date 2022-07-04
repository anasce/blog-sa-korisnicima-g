from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL,Email
from flask_ckeditor import CKEditorField
from wtforms.fields import EmailField


##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Наслов", validators=[DataRequired()])
    subtitle = StringField("Поднаслов", validators=[DataRequired()])
    img_url = StringField("Слика", validators=[DataRequired(), URL()])
    body = CKEditorField("Садржај", validators=[DataRequired()])
    submit = SubmitField("Сачувај пост")

class  RegisterForm(FlaskForm):
    email = EmailField("Ел. пошта", validators=[DataRequired(),Email()])

    password = PasswordField('Шифра', validators=[DataRequired()])
    # [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")]
    #password = PasswordField('Шифра', validators=[DataRequired("Please enter your email address."), validators.Email("Please enter your email address.")])
    name = StringField("Име", validators=[DataRequired()])
    submit = SubmitField("Сачувај корисника")
    # email = db.Column(db.String(250), nullable=False)
    # password = db.Column(db.String(250), nullable=False)
    # name = db.Column(db.String(250), nullable=False)

class  LoginForm(FlaskForm):
    email = EmailField("Ел. пошта", validators=[DataRequired(),Email()])
    password = PasswordField('Шифра', validators=[DataRequired()])
    # [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")]
    #password = PasswordField('Шифра', validators=[DataRequired("Please enter your email address."), validators.Email("Please enter your email address.")])
    #name = StringField("Име", validators=[DataRequired()])
    submit = SubmitField("Логовање")
    # email = db.Column(db.String(250), nullable=False)
    # password = db.Column(db.String(250), nullable=False)
    # name = db.Column(db.String(250), nullable=False)

class FormaZaKomentar(FlaskForm):

    body = CKEditorField("Коментар", validators=[DataRequired()])
    submit = SubmitField("Сачувај коментар")
