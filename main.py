from flask import Flask, render_template, redirect, url_for, flash,abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreatePostForm,RegisterForm,LoginForm,FormaZaKomentar
from flask_gravatar import Gravatar
import werkzeug
from flask_login import LoginManager
from functools import wraps
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import os
Base = declarative_base()

login_manager = LoginManager()
app = Flask(__name__)

#SECRET_KEY = os.urandom(32)
#app.config['SECRET_KEY'] = SECRET_KEY
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog1.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL",'sqlite:///blog1.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return RegUser.query.get(int(user_id))
##CONFIGURE TABLES

class RegUser(UserMixin, db.Model,Base):
#class RegUser( Base):
        __tablename__ = "reguser"
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(250), unique=True, nullable=False)
        password = db.Column(db.String(250), nullable=False)
        name = db.Column(db.String(250), nullable=False)
        blogposts = relationship("BlogPost")
        komentari = relationship("Komentar")
class BlogPost(db.Model,Base):
#class BlogPost( Base):
    __tablename__ = "blogpost"
    id = db.Column(db.Integer, primary_key=True)
    #author = db.Column(db.String(250), nullable=False)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    reguser_id = Column(Integer, ForeignKey('reguser.id'))
    komentari = relationship("Komentar")
class Komentar(db.Model,Base):
    __tablename__ = "komentar"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    reguser_id = Column(Integer, ForeignKey('reguser.id'))
    blogpost_id = Column(Integer, ForeignKey('blogpost.id'))


db.create_all()

def admin_neophodan(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if bool(current_user.is_authenticated):
            sikor = RegUser.query.filter_by(name=current_user.name).first()
            print(f"аааа  {sikor.id} аааа")
            if sikor.id != 1:
                abort()
        return f(*args, **kwargs)
    return decorated_function
@app.route('/')

def get_all_posts():
    print(bool(RegUser.is_active))
    #print(int(RegUser.id))
    #print(RegUser)
    if bool(current_user.is_authenticated):
         #print(current_user.name)
         pass
    if bool(current_user.is_authenticated):
       sikor = RegUser.query.filter_by(name=current_user.name).first()
       #print(sikor.id)
       if sikor.id==1:
           jap=True
       else:
           jap=False
    else:
        jap=False
    #print(int(RegUser.id))
    posts = BlogPost.query.all()
    #print(posts)
    #jap=False
    for post in posts:
        print(post.reguser_id)
        aut = RegUser.query.filter_by(id=post.reguser_id).first()
        print(aut.name)
        post.au_i=aut.name
    return render_template("index.html", all_posts=posts,jl=bool(current_user.is_authenticated),ja=jap)


@app.route('/register',methods=["POST","GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():


        elad = RegUser.query.filter_by(email=form.email.data).first()
        if elad==None:
            new_user = RegUser(
                name=form.name.data,
                email=form.email.data,
                password=werkzeug.security.generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)
                #password=form.password.data
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("get_all_posts"))
        else:
            flash('Korisnik sa navedenom adresom el pošte već postoji u bazi.')
            return redirect(url_for("login"))

    return render_template("register.html", form=form, jl = bool(current_user.is_authenticated))


@app.route('/login',methods=["POST","GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        ea=form.email.data
        es=form.password.data
        uname = RegUser.query.filter_by(email=ea).first()
        if uname!=None and werkzeug.security.check_password_hash(uname.password, es) == True:
          login_user(uname)
          return redirect(url_for("get_all_posts"))
        else:
            flash('Неки од података за логовање није добар. Покушајте поново.')
            return redirect(url_for("login"))
    return render_template("login.html",form=form, jl = bool(current_user.is_authenticated))


@app.route('/logout',methods=["POST","GET"])
def logout():
    logout_user()
    # , jl = bool(current_user.is_authenticated)
    return redirect(url_for('get_all_posts', jl = bool(current_user.is_authenticated)))
#return redirect(url_for('details', form=form))




@app.route("/post/<int:post_id>",methods=["GET","POST"])

def show_post(post_id):
    requested_post = BlogPost.query.get(post_id)
    if bool(current_user.is_authenticated):
        print(current_user.name)
    if bool(current_user.is_authenticated):
        sikor = RegUser.query.filter_by(name=current_user.name).first()
        print(sikor.id)
        if sikor.id == 1:
            jap = True
        else:
            jap = False
    else:
        jap = False

    print(requested_post.reguser_id)
    aut = RegUser.query.filter_by(id=requested_post.reguser_id).first()
    print(aut.name)
    requested_post.au_i=aut.name
    sibp = BlogPost.query.filter_by(id=requested_post.id).first()
    #if bool(current_user.is_authenticated):
    form = FormaZaKomentar()
    if form.validate_on_submit():
           sikor = RegUser.query.filter_by(name=current_user.name).first()

           new_komentar = Komentar(
               body=form.body.data,
               reguser_id=sikor.id,
               blogpost_id = sibp.id
           )
           db.session.add(new_komentar)
           db.session.commit()
           #return redirect(url_for("get_all_posts"))
           return redirect(url_for("show_post",post_id=sibp.id))
    #else:
        #flash ("Корисник који није улогован не може оставити коментар.")
        #return redirect(url_for("login"))
    svi_bp_komentari = Komentar.query.filter_by(blogpost_id=sibp.id).all()
    # print(posts)
    # jap=False

    for kom in svi_bp_komentari:
        autk = RegUser.query.filter_by(id=kom.reguser_id).first()
        kom.au_k_i = autk.name
        kom.elp=autk.email

    gravatar = Gravatar(app,
                        size=100,
                        rating='g',
                        default='retro',
                        force_default=False,
                        force_lower=False,
                        use_ssl=False,
                        base_url=None)
    return render_template("post.html", post=requested_post, jl = bool(current_user.is_authenticated),ja=jap,form=form,komentari=svi_bp_komentari,np=False)


@app.route("/about")
def about():
    return render_template("about.html", jl = bool(current_user.is_authenticated))


@app.route("/contact")
def contact():
    return render_template("contact.html", jl = bool(current_user.is_authenticated))


@app.route("/new-post",methods=["POST","GET"])
@admin_neophodan
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        sikor = RegUser.query.filter_by(name=current_user.name).first()
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,


            date=date.today().strftime("%B %d, %Y"),
            reguser_id=sikor.id
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form, jl = bool(current_user.is_authenticated),np=True)


@app.route("/edit-post/<int:post_id>",methods=["POST","GET"])
@admin_neophodan
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        #author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        #post.author = edit_form.author.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id, jl = bool(current_user.is_authenticated)))

    return render_template("make-post.html", form=edit_form, jl = bool(current_user.is_authenticated))


@app.route("/delete/<int:post_id>")
@admin_neophodan
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts', jl = bool(current_user.is_authenticated)))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
