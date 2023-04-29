from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
from wtforms import Form, TextAreaField, StringField, PasswordField, EmailField, validators
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
from flask_jwt_extended import JWTManager
from flask_login import LoginManager, login_required, login_user, UserMixin, logout_user, current_user
from datetime import datetime


app = Flask(__name__)


login_manager = LoginManager()
login_manager.init_app(app)

# SQL Alchemy Import
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/furkan/Desktop/GithubProjects/basic_flask_request/database.db"
db.init_app(app)

with app.app_context():
    db.create_all()

jwt = JWTManager(app)


# Create Screet Keys
app.secret_key = "blog"
app.config["JWT_SECRET_KEY"] = "secret-key"


# Create User Table With SQL Alchemy
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String)
    password = db.Column(db.String)


# Create Article Table With SQL Alchemy
class Article(db.Model):
    article_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    title = db.Column(db.String)
    content = db.Column(db.String)
    created_date = db.Column(
        db.String, default=datetime.now().strftime("%d.%m.%Y %H:%M:%S"))


# Create Form for Register Process
class RegisterForm(Form):
    username = StringField("Username", validators=[
                           validators.Length(validators.Length(min=4, max=25))])
    email = EmailField("Email", validators=[
                       validators.Email(message="Please , write email type")])
    password = PasswordField("Password", validators=[
                             validators.DataRequired(message="Testaaa")])


# Create Form for Login Process
class LoginForm(Form):
    username = StringField("Username")
    password = PasswordField("Password")


# Create Form for Article Process
class ArticleForm(Form):
    title = StringField("Title")
    content = TextAreaField("Content")


# Login Control Processes
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized_callback():
    flash("Login", "danger")
    return redirect(url_for("login"))


def is_authenticated(self):
    return self.is_authenticated


##########   With Web Process on Flask   ##########


@app.route("/", methods=["GET"])
def index():
    if "username" in session:
        user = session["username"]
    else:
        user = None
    return render_template("index.html", user=user)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST":
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)

        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        flash("Account succesfully created", "success")
        return redirect(url_for("index"))
    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if not current_user.is_authenticated:
        form = LoginForm(request.form)
        if request.method == "POST":
            username = form.username.data
            password = form.password.data
            result = User.query.filter_by(username=username).first()
            if result:
                if sha256_crypt.verify(password, result.password):
                    login_user(result, remember=True)
                    session["username"] = username
                    flash("Login success", "success")
                    return redirect(url_for("index"))
            flash("Account not found", "danger")
            return redirect(url_for("login"))
        else:
            return render_template("login.html", form=form)
    else:
        return redirect(url_for("index"))


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    if request.method == "POST":
        return redirect(url_for("add_article"))
    else:
        articles = Article.query.filter_by(username=session["username"]).all()
        if articles:
            return render_template("dashboard.html", articles=articles)
        else:
            return render_template("dashboard.html")


@login_required
@app.route("/add-article", methods=["GET", "POST"])
def add_article():
    form = ArticleForm(request.form)
    title = form.title.data
    content = form.content.data
    username = session["username"]
    if request.method == "POST":
        now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        article = Article(title=title, content=content,
                          username=username, created_date=now)
        db.session.add(article)
        db.session.commit()

        flash("Article successfully added", "success")
        return redirect(url_for("dashboard"))
    else:
        return render_template("add_article.html", form=form)


@app.route("/article-detail/<string:id>")
def article_detail(id):
    article = Article.query.filter_by(article_id=id).first()
    if article:
        return render_template("article_detail.html", article=article)


@app.route("/delete-article/<string:id>")
def delete_article(id):
    article = Article.query.filter_by(article_id=id,username=session["username"]).first()
    if article:
        db.session.delete(article)
        db.session.commit()
    return redirect(url_for("dashboard"))


@app.route("/update-article/<string:id>", methods=["GET", "POST"])
def update_article(id):
    if request.method == "GET":
        article = Article.query.filter_by(article_id=id,username=session["username"]).first()
        if article:
            form = ArticleForm()
            form.title.data = article.title
            form.content.data = article.content

            return render_template("update_article.html", form=form)
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


##########   With Request Process on Flask   ##########

@app.route("/register/request", methods=["POST"])
def register_request():
    try:
        form = RegisterForm(request.form)

        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)

        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "Account succesfully created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@app.route("/login/request", methods=["GET", "POST"])
def login_request():
    try:
        form = LoginForm(request.form)
        username = form.username.data
        password = form.password.data

        result = User.query.filter_by(username=username).first()
        if result:
            if sha256_crypt.verify(password, result.password):
                login_user(result, remember=True)
                session["username"] = username
                return jsonify({"message": "Login success"}), 200
        return jsonify({"error": "Account not found"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@login_required
@app.route("/dashboard/request", methods=["GET"])
def dashboard_request():
    try:
        data_dictionary = dict()
        articles = Article.query.filter_by(username=session["username"]).all()
        if articles:
            dictionary = {"message": "Success Get Articles"}
            for article in articles:
                data_dictionary[str(article.article_id)] = {
                    "Title": article.title, "Created Date": article.created_date}
            dictionary["data"] = data_dictionary
            return jsonify(dictionary)
        else:
            return jsonify({"message": "Articles not found"})
    except:
        return jsonify({"message": "hata"})


@login_required
@app.route("/add-article/request", methods=["POST"])
def add_article_request():
    try:
        form = ArticleForm(request.form)
        title = form.title.data
        content = form.content.data
        username = session["username"]
        now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        article = Article(title=title, content=content,
                          username=username, created_date=now)
        db.session.add(article)
        db.session.commit()

        return jsonify({"message": "Article successfully added"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@app.route("/article-detail/request/<string:id>", methods=["GET"])
def article_detail_request(id):
    try:
        article = Article.query.filter_by(article_id=id).first()
        data_dictionary = {}
        if article:
            data_dictionary[str(article.article_id)] = {
                "Title": article.title, "Content": article.content, "Created Date": article.created_date}
            return jsonify({"message": data_dictionary})
        else:
            return jsonify({"error": "Article not found"})
    except Exception as e:
        return jsonify({"error":str(e)})


@login_required
@app.route("/delete-article/request/<string:id>", methods=["POST"])
def delete_article_request(id):
    try:
        article = Article.query.filter_by(article_id=id,username=session["username"]).first()
        if article:
            db.session.delete(article)
            db.session.commit()
            return jsonify({"message": "Article deleted"}), 200
        return jsonify({"message": "Article not found"}), 401
    except Exception as e:
        return jsonify({"message": str(e)}), 404

@login_required
@app.route("/update-article/request/<string:id>", methods=["PUT"])
def update_article_request(id):
    try:
        article = Article.query.filter_by(article_id=id,username=session["username"]).first()
        if article:
            form = ArticleForm(request.form)
            title = form.title.data
            content = form.content.data

            article.title = title
            article.content = content
            db.session.commit()

            return jsonify({"message": "Article updated"}), 200
        else:
            return jsonify({"message": "Article not updated"}), 401
    except Exception as e:
        return jsonify({"message": str(e)}), 404


@app.route("/logout/request", methods=["GET"])
def logout_request():
    try:
        session.clear()
        logout_user()
        return jsonify({"message": "Logout success"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 404


if __name__ == "__main__":
    app.run(debug=True)
