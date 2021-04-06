from datetime import timedelta
import sys
from flask import Flask, redirect, url_for, render_template, session, request
from flask.json import jsonify
import requests
from auth import githubAuth, githubCallback
from noteRequests import user, repos, repo, getFile, getFiles, createFile, updateFile, getBranch, getBranches
import os
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://gitnotes-app.web.app"}})
app.permanent_session_lifetime = timedelta(hours=2)
redirect_frontend = "https://gitnotes-app.web.app/dashboard"

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["GET"])
def userLogin():
    return githubAuth()

@app.route("/callback", methods=["GET"])
def callback():
    token = githubCallback()
    session['token'] = token
    #return redirect(f"/user?token={token}")
    return redirect(f"{redirect_frontend}?token={token}", code=301)


#parameters to pass: token
@app.route("/refresh", methods=["GET"])
def refresh():
    token = request.args.get('token')
    return "to do"

#parameters to pass: token
@app.route("/user", methods=["GET"])
def userData():
    token = request.args.get('token')
    jsonuser = user(token)

    if isinstance(jsonuser, int):
        return 'User Authentication Failed', 401

    #print("state: " + session['name'], file=sys.stderr)
    return jsonuser

#parameters to pass: token
@app.route("/repos", methods=["GET"])
def reposData():
    token = request.args.get('token')
    jsonrepos = repos(token)

    if isinstance(jsonrepos, int):
        return 'User Authentication Failed', 401

    return jsonrepos

#parameters to pass: token
@app.route("/repo/<user>/<reponame>", methods=["GET"])
def repoData(user, reponame):
    token = request.args.get('token')
    jsonrepo = repo(token, user, reponame)

    if isinstance(jsonrepo, int):
        return 'Repo not Found', 400

    return jsonrepo

#parameters to pass: token
@app.route("/branches/<user>/<reponame>", methods=["GET"])
def branchesData(user, reponame):
    token = request.args.get('token')
    jsonbranch = getBranches(token, user, reponame)

    if isinstance(jsonbranch, int):
        return 'Repo not Found', 400

    return jsonbranch

#parameters to pass: token
@app.route("/branch/<user>/<reponame>/<branch>", methods=["GET"])
def branchData(user, reponame, branch):
    token = request.args.get('token')
    jsonbranch = getBranch(token, user, reponame, branch)

    if isinstance(jsonbranch, int):
        return 'Branch not Found', 400

    return jsonbranch


#parameters to pass: token, path
@app.route("/getfiles/<user>/<reponame>/", methods=["GET"])
def getFilesData(user, reponame):
    token = request.args.get('token')
    path = request.args.get('path')

    if path is None:
        path = ''

    jsonfile = getFiles(token, user, reponame, path)

    if isinstance(jsonfile, int):
        return 'Files not Found', 400

    return jsonfile

#parameters to pass: token, path
@app.route("/getfile/<user>/<reponame>/<filename>", methods=["GET"])
def getFileData(user, reponame, filename):
    token = request.args.get('token')
    path = request.args.get('path')

    if path is None:
        path = ''
    if not filename[-3:] == '.md':
        return 'Incorrect File Type', 400

    jsonfile = getFile(token, user, reponame, filename, path)

    if isinstance(jsonfile, int):
        return 'File not Found', 400

    return jsonfile

#parameters to pass: token, message, path, content, branch
@app.route("/newfile/<user>/<reponame>/<filename>", methods=["GET", "POST"])
def setNewFileData(user, reponame, filename):
    data = request.get_json()
    token = data.get('token', None)
    msg = data.get('message', None)
    path = data.get('path', None)
    filecontent = data.get('content', None)
    branch = data.get('branch', None)

    if msg is None or msg == '':
        msg = f"Created {filename}"
    if filecontent is None or filecontent == '':
        msg = ''
    if path is None:
        path = ''
    if not filename[-3:] == '.md':
        return 'Incorrect File Type', 400

    jsonNewFile = createFile(token, user, reponame, filename, path, filecontent, msg, branch)

    if isinstance(jsonNewFile, int):
        return 'Creating File Failed', 400

    return jsonNewFile

#parameters to pass: token, message, path, content, sha, branch
@app.route("/setfile/<user>/<reponame>/<filename>", methods=["GET", "POST"])
def setFileData(user, reponame, filename):
    data = request.get_json()
    token = data.get('token', None)
    msg = data.get('message', None)
    path = data.get('path', None)
    filecontent = data.get('content', None)
    branch = data.get('branch', None)
    sha = data.get('sha', None)

    if msg is None or msg == '':
        msg = f"Updated {filename}"
    if path is None:
        path = ''
    if not filename[-3:] == '.md':
        return 'Updating File Failed', 400

    jsonUpdate = updateFile(token, user, reponame, filename, path, filecontent, msg, branch, sha)

    if isinstance(jsonUpdate, int):
        return 'Updating File Failed', 400

    return jsonUpdate

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.run(threaded=True)
    #app.run()
