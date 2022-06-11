from flask import Flask, render_template, request
from os import getcwd
from config import conf

PATH = f'{getcwd()}/config/config.ini'
app = Flask(__name__)

@app.route("/", methods=['POST','GET'])
def home():
    if request.method == "GET":
        AT = request.headers.get('Oidc-Access-Token')
        if AT == None:
            return render_template("index.html")
        else:
            conf.set_token(filename=PATH,new_token=AT)
            return render_template("redirect.html")
            return f'{request.headers}'
    else:
        return render_template("index.html")

def deploy():
    app.run(host="127.0.0.1", port=8000, debug=False)