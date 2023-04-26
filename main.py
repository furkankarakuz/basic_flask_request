from flask import Flask, render_template, redirect,url_for ,request ,Response ,jsonify
from wtforms import Form, StringField, PasswordField, EmailField, validators
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

app = Flask(__name__)

db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/furkan/Desktop/GithubProjects/basic_flask_request/database.db"
db.init_app(app)

jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = "scret-key" 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String)
    password = db.Column(db.String)


class RegisterForm(Form):
    username = StringField("username", validators=[validators.Length(validators.Length(min=4, max=25))])
    email = EmailField("email", validators=[validators.Email(message="Please , write email type")])
    password = PasswordField("password", validators=[validators.Length(min=5, max=15),
                                                     validators.DataRequired(message="Not null"),
                                                     validators.EqualTo(fieldname="confirm_password",message="Test")])
    confirm_password = PasswordField("confirm_password")


class LoginForm(Form):
    username = StringField("username")
    password = PasswordField("password")

@app.route("/",methods=["GET"])
def index():
    return render_template("index.html")


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
        return redirect(url_for("index")) , 201
    else:
        return render_template("register.html", form=form)

@app.route("/login",methods=["GET","POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        username = form.username.data
        password = form.password.data
        result = User.query.filter_by(username=username).first()
        if result:
            if sha256_crypt.verify(password,result.password):
                return redirect(url_for("index")) , 200
    else:
        return render_template("login.html",form=form)
        


if __name__ == "__main__":
    app.run(debug=True)