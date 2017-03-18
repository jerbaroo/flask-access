import flask
import flask_access
import flask_login
import user

app = flask.Flask(__name__)
app.secret_key = "TODO change this"
login_manager = flask_login.LoginManager(app)
app.config[flask_access.CURRENT_USER] = flask_login.current_user


@login_manager.user_loader
def load_user(username):
    return user.User(username)


@app.route("/login/<username>")
def login(username):
    flask_login.login_user(user.User(username))
    return flask.redirect(flask.url_for("home"))


@app.route("/")
@flask_login.login_required
def home():
    return "Welcome %s" % flask_login.current_user.username


@app.route("/secret-code")
@flask_access.require("top-secret")
def secret_code():
    return "1234"


@app.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return "Logged out"
