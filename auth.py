#from requests_oauthlib import OAuth2Session
from authlib.integrations.requests_client import OAuth2Session
from flask.json import jsonify
from flask import request, redirect, session, url_for
import requests
import sys
import os

client_id = os.environ.get("GITHUB_ID")
client_secret = os.environ.get("GITHUB_SECRET")
redirect_uri = 'http://localhost:5000/callback'
auth_uri = 'https://github.com/login/oauth/authorize'
token_uri = 'https://github.com/login/oauth/access_token'

def githubAuth():
    #params = {'client_id': client_id, 'redirect_uri': redirect_uri}   
    scope = '&scope=user%20repo'
    github = OAuth2Session(client_id, client_secret)
    auth_endpoint, state = github.create_authorization_url(auth_uri)

    session['state'] = state
    auth_endpoint += scope
    return redirect(auth_endpoint)


def githubCallback():
    auth_response = request.url
    code = request.args.get('code')
    state = request.args.get('state')

    params = {'client_id': client_id, 'client_secret': client_secret, 'code': code, 'redirect_uri': redirect_uri, 'state': state}
    headers = {'Accept': 'application/json'}

    response = requests.post(token_uri, params=params, headers=headers)
    jsonresp = response.json()
    session['token'] = jsonresp['access_token']
    return jsonresp['access_token']
