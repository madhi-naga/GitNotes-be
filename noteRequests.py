from flask.json import jsonify
from flask import request, redirect, session, url_for
import requests
import sys

base_url = 'https://api.github.com'


def user(token):
    headers = {'Accept': 'application/vnd.github.v3+json', 'Authorization': 'bearer ' + token}
    response = requests.get(f'{base_url}/user', headers=headers)
    jsonresp = response.json()
    session['user'] = jsonresp['login']
    session['name'] = jsonresp['name']

    if not response.ok:
        return response.status_code
    return jsonify(response.json())

def repos(token):
    headers = {'Accept': 'application/vnd.github.v3+json', 'Authorization': 'bearer ' + token}
    response = requests.get(f"{base_url}/user/repos", headers=headers)
    return jsonify(response.json())

def repo(token, user, reponame):
    headers = {'Accept': 'application/vnd.github.v3+json', 'Authorization': 'bearer ' + token}
    response = requests.get(f"{base_url}/repos/{user}/{reponame}", headers=headers)

    if not response.ok:
        return response.status_code
    return jsonify(response.json())

def getBranches(token, user, reponame):
    headers = {'Accept': 'application/vnd.github.v3+json', 'Authorization': 'bearer ' + token}
    response = requests.get(f"{base_url}/repos/{user}/{reponame}/branches", headers=headers)
    return jsonify(response.json())

def getBranch(token, user, reponame, branch):
    headers = {'Accept': 'application/vnd.github.v3+json', 'Authorization': 'bearer ' + token}
    #print(f'https://api.github.com/repos/{user}/{reponame}', file=sys.stderr)
    response = requests.get(f"{base_url}/repos/{user}/{reponame}/branches/{branch}", headers=headers)

    if not response.ok:
        return response.status_code
    return jsonify(response.json())

def getFiles(token, user, reponame, path):
    headers = {'Accept': 'application/vnd.github.v3+json', 'Authorization': 'bearer ' + token}
    #print(f"{base_url}/repos/{user}/{reponame}/contents/{path}/{filename}", file=sys.stderr)
    if path == '':
        response = requests.get(f"{base_url}/repos/{user}/{reponame}/contents/", headers=headers)
    else:
        response = requests.get(f"{base_url}/repos/{user}/{reponame}/contents/{path}", headers=headers)

    if not response.ok:
        return response.status_code
    return jsonify(response.json())

def getFile(token, user, reponame, filename, path):
    headers = {'Accept': 'application/vnd.github.v3+json', 'Authorization': 'bearer ' + token}
    #print(f"{base_url}/repos/{user}/{reponame}/contents/{path}/{filename}", file=sys.stderr)
    if path == '':
        response = requests.get(f"{base_url}/repos/{user}/{reponame}/contents/{filename}", headers=headers)
    else:
        response = requests.get(f"{base_url}/repos/{user}/{reponame}/contents/{path}/{filename}", headers=headers)

    if not response.ok:
        return response.status_code
    return jsonify(response.json())

def createFile(token, user, reponame, filename, path, filecontent, msg, branch):
    print(path, file=sys.stderr)

    headers = {'Accept': 'application/vnd.github.v3+json', 'Authorization': 'bearer ' + token}
    if branch:
        data = {'message': f"{msg} (GitNotes)", 'content': filecontent, 'branch': branch}
    else:
        data = {'message': f"{msg} (GitNotes)", 'content': filecontent}

    if path == '':
        response = requests.put(f"{base_url}/repos/{user}/{reponame}/contents/{filename}", headers=headers, json=data)
    else:
        response = requests.put(f"{base_url}/repos/{user}/{reponame}/contents/{path}/{filename}", headers=headers, json=data)

    if not response.ok:
        return response.status_code
    return jsonify(response.json())

def updateFile(token, user, reponame, filename, path, filecontent, msg, branch, sha):
    headers = {'Accept': 'application/vnd.github.v3+json', 'Authorization': 'bearer ' + token}
    branch = 'main'
    if branch:
        data = {'message': f"{msg} (GitNotes)", 'content': filecontent, 'sha': sha, 'branch': branch}
    else:
        data = {'message': f"{msg} (GitNotes)", 'content': filecontent, 'sha': sha}

    if path == '':
        response = requests.put(f"{base_url}/repos/{user}/{reponame}/contents/{filename}", headers=headers, json=data)
    else:
        response = requests.put(f"{base_url}/repos/{user}/{reponame}/contents/{path}/{filename}", headers=headers, json=data)

    if not response.ok:
        return response.status_code
    return jsonify(response.json())
