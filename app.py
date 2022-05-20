from __future__ import annotations

import os
import flask
import flask_login
import sirope
from flask_login import login_required
from model import Painting, User
from werkzeug.utils import secure_filename
import json

EXTENSIONS = {'jpg' 'png', 'jpeg', 'gif'}
FOLDER = os.path.join('static', 'images')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in EXTENSIONS


def create_app():
    flapp = flask.Flask(__name__)
    siro = sirope.Sirope()
    lgm = flask_login.login_manager.LoginManager()

    flapp.config.from_file("config.json", json.load)
    lgm.init_app(flapp)
    return flapp, siro, lgm


app, srp, lm = create_app()

app.config['UPLOAD_FOLDER'] = FOLDER


@lm.user_loader
def user_loader(username: str) -> User | None:
    return User.find(srp, username)


@app.route('/login', methods=['GET', 'POST'])
def login():
    username = flask.request.form.get("edUsername")
    password = flask.request.form.get("edPassword")

    if username and password is not None:
        usr = User.find(srp, username)
        if not usr:
            flask.flash("The user doesn't exist or your username is wrong")
            return flask.redirect('/')
        elif not usr.check_password(password):
            flask.flash("Wrong password")
            return flask.redirect('/')
        else:
            flask_login.login_user(usr)
            return flask.redirect('/')
    else:
        flask.redirect('/login')

    sust = {
        "username": username,
        "password": password
    }

    return flask.render_template('login.html', **sust)


@app.route('/register', methods=['GET', 'POST'])
def register():
    username = flask.request.form.get("edUsername")
    password = flask.request.form.get("edPassword")

    usr = User.find(srp, username)

    if not usr:
        if username and password is not None:
            usr = User(username, password)
            srp.save(usr)
            flask.flash("Registered successfully")
            flask_login.login_user(usr)
            return flask.redirect('/')
    else:
        flask.flash("This user already exists")

    sust = {
        "username": username,
        "password": password
    }

    return flask.render_template('register.html', **sust)


@app.route('/logout')
@login_required
def logout():
    flask_login.logout_user()
    return flask.redirect('/')


@app.route('/', methods=['GET', 'POST'])
# pagina principal (home)
def index():
    usr = User.current_user()
    # en el home se cargan las ultimas 30 publicaciones
    last_paintings = list(srp.load_last(Painting, 30))

    sust = {
        "usr": usr,
        "last_paintings": last_paintings,
        # necesario para saber a que publicacion en concreto afectan ciertas acciones
        "paintings_oids": {painting.__oid__: srp.safe_from_oid(painting.__oid__) for painting in last_paintings}
    }

    return flask.render_template("index.html", **sust)


@app.route('/punctuate/', methods=['POST'])
@login_required
# para puntuar una publicacion
def punctuate():
    safe_oid = flask.request.args.get('oid')
    points = int(flask.request.form.get("edPunctuate"))

    if not safe_oid:
        return flask.flash("OID not found")

    # se carga desde el almacenamiento
    painting = srp.load(srp.oid_from_safe(safe_oid))

    if not painting:
        return flask.flash("obj not found")

    if 1 <= points <= 10:
        painting.add_points(points)
        srp.save(painting)
    else:
        flask.flash("Punctuation must be between 1 and 10 points!")

    return flask.redirect('/')


@app.route('/post_painting', methods=['GET', 'POST'])
@login_required
# para publicar
def post_painting():
    usr = User.current_user()
    title = flask.request.form.get("edTitle")
    f = flask.request.files.get("edPainting")

    if flask.request.method == 'POST':

        if not title:
            flask.flash("You must write a title for the painting")
        if f.filename == '':
            flask.flash("You must choose an image to upload")
        if not f and allowed_file(f.filename):
            flask.flash("Unsupported file type")
        else:

            # guardar en la carpeta de imagenes la imagen subida por el usuario

            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            path = os.path.join(filename)

            # Guardar en el almacenamiento el nuevo objeto Painting

            p = Painting(title, path, usr.username)
            p_oid = srp.save(p)
            usr.add_painting_oid(p_oid)
            srp.save(usr)

            return flask.redirect('/')

    sust = {
        "usr": usr,
        "f": f
    }

    return flask.render_template('post_painting.html', **sust)


@app.route('/view_painting/', methods=['GET'])
# para ver una publicacion
def view_painting():
    safe_oid = flask.request.args.get('oid')
    usr = User.current_user()

    if not safe_oid:
        return flask.flash("OID not found")

    # se carga desde el almacenamiento
    painting = srp.load(srp.oid_from_safe(safe_oid))

    if not painting:
        return flask.flash("obj not found")

    sust = {
        "painting": painting,
        "usr": usr
    }

    return flask.render_template('view_painting.html', **sust)


@lm.unauthorized_handler
def unauthorized():
    return "Unauthorized", 401


if __name__ == '__main__':
    app.run()
