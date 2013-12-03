#!/usr/bin/env python
"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

import os

import requests
from flask import Flask, jsonify, request, abort


app = Flask(__name__)


###############################################################################
# Configuration
###

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'supersecret')
app.config['TUMBLR_ENDPOINT'] = os.environ.get(
    'TUMBLR_ENDPOINT',
    'api.tumblr.com/v2/user/dashboard')
app.config['FOAUTH_LOGIN'] = os.environ.get('FOAUTH_LOGIN', 'email')
app.config['FOAUTH_PASSWORD'] = os.environ.get('FOAUTH_PASSWORD', 'password')


###############################################################################
# Main site
###

@app.route('/')
def fetch_feed():
    """Fetch the feed and respond."""

    secret = request.args.get('secret', '')
    if secret != app.config['SECRET_KEY']:
        abort(401)

    auth = (app.config['FOAUTH_LOGIN'], app.config['FOAUTH_PASSWORD'])

    r = requests.get(
        'https://foauth.org/{}'.format(app.config['TUMBLR_ENDPOINT']),
        auth=auth,
    )
    r.raise_for_status()

    return jsonify(r.json())


###############################################################################
# Main
###

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)
