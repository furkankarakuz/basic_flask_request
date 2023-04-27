from flask import Flask, render_template, redirect,url_for ,request ,Response  , flash , session
from wtforms import Form, TextAreaField, StringField, PasswordField, EmailField, validators
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
from flask_jwt_extended import JWTManager
from flask_login import LoginManager,login_required,login_user,UserMixin,logout_user,current_user
from datetime import datetime
from functools import wraps


app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/furkan/Desktop/GithubProjects/basic_flask_request/database.db"
db.init_app(app)

jwt = JWTManager(app)

app.secret_key = "blog"
app.config["JWT_SECRET_KEY"] = "scret-key"


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique = True, nullable = False)
    email = db.Column(db.String)
    password = db.Column(db.String)

class Article(db.Model):
    article_id = db.Column(db.Integer , primary_key = True)
    username = db.Column(db.String , nullable = False )
    title = db.Column(db.String)
    content = db.Column(db.String)
    created_date = db.Column(db.String , default = datetime.now().strftime("%d.%m.%Y %H:%M:%S") )


class RegisterForm(Form):
    username = StringField("username", validators=[validators.Length(validators.Length(min=4, max=25))])
    email = EmailField("email", validators=[validators.Email(message="Please , write email type")])
    password = PasswordField("Password",validators=[
        validators.DataRequired(message="Testaaa"),
        validators.EqualTo("confirm",message="Test")])
    confirm = PasswordField("Confirm Password")

class LoginForm(Form):
    username = StringField("username")
    password = PasswordField("password")

class ArticleForm(Form):
    title = StringField("Title")
    content = TextAreaField("Content")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized_callback():
    flash("Login","danger")
    return redirect(url_for("login"))



def is_authenticated(self):
    return self.is_authenticated

@app.route("/",methods=["GET"])
def index():
    if "username" in session:
        user = session["username"]
    else:
        user=None
    return render_template("index.html",user=user)


with app.app_context():
    db.create_all()


@app.route("/register",methods=["GET","POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST":
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)

        user = User(username=username,email=email,password=password)
        db.session.add(user)
        db.session.commit()

        flash("Account succesfully created","success")
        return redirect(url_for("index"))
    else:
        return render_template("register.html", form=form)


@app.route("/login",methods=["GET","POST"])
def login():
    if not current_user.is_authenticated:
        form = LoginForm(request.form)
        if request.method == "POST":
            username = form.username.data
            password = form.password.data
            result = User.query.filter_by(username=username).first()
            if result:
                if sha256_crypt.verify(password,result.password):
                    login_user(result, remember=True)
                    session["username"] = username
                    flash("Account succesfully","success")
                    return redirect(url_for("index"))
            flash("Not found account","danger")
            return redirect(url_for("login"))
        else:
            return render_template("login.html",form=form)
    else:
        return redirect(url_for("index"))
       
@app.route("/dashboard",methods=["GET","POST"])
@login_required
def dashboard():
    if request.method=="POST":
        return redirect(url_for("addarticle"))
    else:
        articles = Article.query.filter_by(username=session["username"]).all()
        if articles:
            return render_template("dashboard.html",articles=articles)
        else:
            return render_template("dashboard.html")
@login_required
@app.route("/addarticle",methods=["GET","POST"])
def addarticle():
    form = ArticleForm(request.form)
    title = form.title.data
    content = form.content.data
    username = session["username"]
    if request.method=="POST":
        now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        article = Article (title=title,content=content,username=username,created_date=now)
        db.session.add(article)
        db.session.commit()

        flash("Success , added new article","success")
        return redirect(url_for("dashboard"))
    else:
        return render_template("addarticle.html",form=form)


@app.route("/article-detail/<string:id>")
def articledetail(id):
    article = Article.query.filter_by(article_id=id).first()
    if article:
        return render_template("articledetail.html",article=article)

@app.route("/delete-article/<string:id>")
def deletearticle(id):
    article = Article.query.filter_by(article_id=id).first()
    if article:
        db.session.delete(article)
        db.session.commit()
    return redirect(url_for("dashboard"))

@app.route("/update-article/<string:id>",methods=["GET","POST"])
def updatearticle(id):
    if request.method=="GET":
        article = Article.query.filter_by(article_id=id).first()
        if article:
            form = ArticleForm()
            form.title.data = article.title
            form.content.data = article.content

            return render_template("updatearticle.html",form=form)
    else:
        form = ArticleForm(request.form)
        title = form.title.data
        content = form.content.data

        article = Article.query.filter_by(article_id=id).first()
        article.title = title
        article.content = content
        db.session.commit()

        return redirect(url_for("dashboard"))
        

@app.route("/logout")
def logout():
    session.clear()
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)