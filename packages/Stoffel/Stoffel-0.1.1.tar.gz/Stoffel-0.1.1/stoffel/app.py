from flask import Flask, render_template, g, request, redirect, make_response, jsonify
import json 
import os
import urllib
from pathlib import Path
import requests as r
import webbrowser

from stoffel.settings import *
from stoffel.core.ggl import Google
from stoffel.core.connect import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)

def read_json(file_path):
    if not os.path.isfile(CONNECTIONS_PATH):
        with open(CONNECTIONS_PATH, 'w+') as f:
            json.dump({}, f, indent=4)

    with open(CONNECTIONS_PATH, "rb+") as f:
        data = json.load(f)
    return data

def write_json(file_path, data):
    with open(CONNECTIONS_PATH, 'w+') as f:
        json.dump(data, f, indent=4)

@app.context_processor
def context_processor():
    data = read_json(CONNECTIONS_PATH)
    return dict(data=data)

@app.before_request
def load_data():
    data = read_json(CONNECTIONS_PATH)
    g.data = data

@app.route('/')
def home():
    if not os.path.exists(GOOGLE_TOKEN_PATH):
        Google()
    return render_template("home.html")

@app.route('/<source_destination>/<tp>')
def html_file(source_destination, tp):
    with open(f"templates/connections/{source_destination}/{tp}.html", "r") as file:
        data = file.read()
    return jsonify({"data" : data})

@app.route("/callback")
def callback():
    return redirect("/")

@app.route('/<name>', methods=["GET", "POST"])
def project(name):
    home = str(Path.home())
    if request.method == "POST":
        data = request.form.to_dict()
        project = dict()
        for key, value in data.items():
            connection_src_dest = key.split("_")[0]
            connection_id = key.split("_")[len(key.split("_"))-1]
            project.update({connection_id : {"source"  : dict(), "destination" : dict()}}) if connection_id not in project else None
            connection_key = "_".join(key.split("_")[1:-1])
            floats = ["w", "h", "x", "y"]
            if not value and connection_key in floats:
                value = 0
            project[connection_id][connection_src_dest][connection_key] = value if connection_key not in floats else float(value)
        g.data[name] = project
        write_json(CONNECTIONS_PATH, g.data)
        return redirect(f"/{name}")
    else:
        name = urllib.parse.unquote_plus(name)
        args = request.args.to_dict()
        errors = list()
        if name not in g.data:
            error = [f"Project {name} does not exist."]
        return render_template("project.html", project=name, errors=errors, args=args, home=home.replace("\\", "/").replace("C:", ""))

@app.route('/add-project/<name>', methods=['GET', 'POST'])
def add_project(name):
    name = urllib.parse.unquote_plus(name)
    if name in g.data.keys():
        name = name +  "(" + str(len([i for i in g.data.keys() if name in i])) + ")"
    g.data[name] = {}
    write_json(CONNECTIONS_PATH, g.data)
    return redirect(f"/{urllib.parse.quote_plus(name)}")

@app.route('/delete-project/<name>', methods=['GET', 'POST'])
def delete_project(name):
    name = urllib.parse.unquote_plus(name)
    g.data.pop(name, None)
    write_json(CONNECTIONS_PATH, g.data)
    return redirect(f"/")

@app.route('/run-project/<name>', methods=["GET"])
def run_project(name):
    name = urllib.parse.unquote_plus(name)
    project = Project(name)
    project.run()
    return redirect(f"/{name}")

@app.route('/open-file/<file_path>', methods=["GET"])
def open_file(file_path):
    name = urllib.parse.unquote_plus(file_path)
    os.startfile(name)
    return redirect(f"/")

@app.route('/google-url/<file_id>', methods=["GET"])
def google_url(file_id):
    ggl = Google()
    api_key = GOOGLE_PICKER_KEY
    headers = {
        "Authorization" : "Bearer " + ggl.creds.token, 
        "Accept" : "application/json" 
    }
    url = f"https://www.googleapis.com/drive/v3/files/{file_id}?key={GOOGLE_PICKER_KEY}&fields=webViewLink"
    response = r.get(url, headers=headers)
    return response.json()

@app.route("/file-tree", methods=["POST"])
def dirlist():
   r=['<ul class="jqueryFileTree" style="display: none;">']
   try:
       r=['<ul class="jqueryFileTree" style="display: none;">']
       d=urllib.parse.unquote(request.form.to_dict().get('dir','c:\\temp'))
       for f in os.listdir(d):
           ff=os.path.join(d,f)
           if os.path.isdir(ff):
               r.append('<li class="directory collapsed"><a href="#" rel="%s/">%s</a></li>' % (ff,f))
           else:
               e=os.path.splitext(f)[1][1:] # get .ext and remove dot
               r.append('<li class="file ext_%s"><a href="#" rel="%s">%s</a></li>' % (e,ff,f))
       r.append('</ul>')
   except Exception as e:
       r.append('Could not load directory: %s' % str(e))
   r.append('</ul>')
   return make_response(''.join(r))

if __name__=="__main__":
    url = "http://localhost:5500"
    webbrowser.open_new(url)
    app.run(port=5500, debug=False)