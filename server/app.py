from flask import Flask, g
from os import getcwd
from config import conf

app = Flask(__name__)
app.secret_key = "change_me"
app.config["OIDC_CLIENT_SECRETS"] = f"{getcwd()}/server/oidc-config.json"
app.config["OIDC_COOKIE_SECURE"] = False
from flask_oidc import OpenIDConnect

oidc = OpenIDConnect(app)

PATH = f"{getcwd()}/config/config.ini"


@app.route("/")
@oidc.require_login
def index():
    if oidc.user_loggedin:
        conf.set_token(filename=PATH, new_token=oidc.get_access_token())
        return f"<h1>{'Autorizando acceso a %s' % oidc.user_getfield('preferred_username')}<h1>\n<h2>Puede cerrar esta ventana<h2>"
    else:
        return "<h3>No ingresó un usuario correcto<h3>"


def deploy():
    app.run(host="127.0.0.1", port=8765, debug=False)
