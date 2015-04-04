from __future__ import absolute_import

import json import unicodedata
import os
from urlparse import urlparse

from flask import Flask, render_template, request, redirect, session
from flask_sslify import SSLify
from rauth import OAuth2Service
import requests

# speech recognition
from SpeechRecog import SpeechRecog

# Setting up serial
import serial
from time import sleep
s = serial.Serial('/dev/ttyACM0', 9600, timeout = None)

app = Flask(__name__, static_folder='static', static_url_path='')
app.requests_session = requests.Session()
app.secret_key = os.urandom(24)

sslify = SSLify(app)

# global used for ride id, so we can track requests with request-details tag
RIDE = ''
CAR = ['uberX' , 'uberXL', 'UberSUV', 'UberBLACK']
LOC = ''
TIME = ''
ESTIMATE = ''
REQUEST = ''

def pick_car():
    car = s.readline()
    return CAR[car]

def get_loc():
    sr = SpeechRecog()
    return sr.speechToCoord()


with open('config.json') as f:
    config = json.load(f)


def generate_oauth_service():
    """Prepare the OAuth2Service that is used to make requests later."""
    return OAuth2Service(
        client_id=os.environ.get('UBER_KEY'),
        client_secret=os.environ.get('UBER_SECRET'),
        name=config.get('name'),
        authorize_url=config.get('authorize_url'),
        access_token_url=config.get('access_token_url'),
        base_url=config.get('base_url'),
    )


def generate_ride_headers(token):
    """Generate the header object that is used to make api requests."""
    return {
        'Authorization': 'bearer %s' % token,
        'Content-Type': 'application/json',
    }


@app.route('/health', methods=['GET'])
def health():
    """Check the status of this application."""
    return ';-)'


@app.route('/', methods=['GET'])
def signup():
    """The first step in the three-legged OAuth handshake.

    You should navigate here first. It will redirect to login.uber.com.
    """
    params = {
        'response_type': 'code',
        'redirect_uri': get_redirect_uri(request),
        'scopes': ','.join(config.get('scopes')),
    }
    url = generate_oauth_service().get_authorize_url(**params)
    return redirect(url)


@app.route('/submit', methods=['GET'])
def submit():
    """The other two steps in the three-legged Oauth handshake.

    Your redirect uri will redirect you here, where you will exchange
    a code that can be used to obtain an access token for the logged-in use.
    """
    params = {
        'redirect_uri': get_redirect_uri(request),
        'code': request.args.get('code'),
        'grant_type': 'authorization_code'
    }
    response = app.requests_session.post(
        config.get('access_token_url'),
        auth=(
            os.environ.get('UBER_KEY'),
            os.environ.get('UBER_SECRET')
        ),
        data=params,
    )
    session['access_token'] = response.json().get('access_token')

    return render_template(
        'success.html',
        token=response.json().get('access_token')
    )


@app.route('/demo', methods=['GET'])
def demo():
    """Demo.html is a template that calls the other routes in this example."""
    return render_template('demo.html', token=session.get('access_token'))


@app.route('/products', methods=['GET'])
def products():
    """Example call to the products endpoint.

    Returns all the products currently available in San Francisco.
    """
    global RIDE
    url = config.get('base_uber_url') + 'products'
    params = {
        'latitude': config.get('start_latitude'),
        'longitude': config.get('start_longitude'),
    }

    response = app.requests_session.get(
        url,
        headers=generate_ride_headers(session.get('access_token')),
        params=params,
    )

    if response.status_code != 200:
        return 'There was an error', response.status_code
    RIDE = json.loads(response.text)
    i = 0
    CAR = pick_car()
    while True:
        try:
            if RIDE['products'][i]['display_name'] != CAR:
                i = i + 1
            else:
                RIDE = RIDE['products'][i]['product_id']
                break
        except:
            return render_template(
                'error.html'
            )
    return render_template(
        'demo.html',
        token=session.get('access_token'),
        info=RIDE
    )


@app.route('/time', methods=['GET'])
def time():
    """Example call to the time estimates endpoint.

    Returns the time estimates from the given lat/lng given below.
    """
    global TIME
    url = config.get('base_uber_url') + 'estimates/time'
    params = {
        'start_latitude': config.get('start_latitude'),
        'start_longitude': config.get('start_longitude')
    }

    response = app.requests_session.get(
        url,
        headers=generate_ride_headers(session.get('access_token')),
        params=params,
    )

    if response.status_code != 200:
        return 'There was an error', response.status_code
    # find specific car by id in list
    newRide = json.loads(response.text)
    i = 0
    while True:
        try:
            if newRide['times'][i]['product_id'] != RIDE:
                print 'nope'
                i = i + 1
            else:
                TIME = newRide['times'][i]['estimate'] / 60
                break
        except:
            return render_template(
                'error.html'
            )
    return render_template(
        'demo.html',
        token=session.get('access_token'),
        info=TIME
    )


@app.route('/price', methods=['GET'])
def price():
    """Example call to the price estimates endpoint.

    Returns the time estimates from the given lat/lng given below.
    """
    global LOC
    global ESTIMATE

    LOC = get_loc()

    url = config.get('base_uber_url') + 'estimates/price'
    params = {
        'start_latitude': config.get('start_latitude'),
        'start_longitude': config.get('start_longitude'),
        'end_latitude': LOC[0],
        'end_longitude': LOC[1]
    }
    LOC = (config.get('start_latitude'), config.get('start_longitude'),
                LOC[0], LOC[1])

    response = app.requests_session.get(
        url,
        headers=generate_ride_headers(session.get('access_token')),
        params=params,
    )

    if response.status_code != 200:
        return 'There was an error', response.status_code
    estimate = json.loads(response.text)
    i = 0
    while True:
        try:
            if estimate['prices'][i]['product_id'] != RIDE:
                i = i + 1
            else:
                ESTIMATE = (estimate['prices'][i]['high_estimate'] + 
                                     estimate['prices'][i]['low_estimate']) / 2
                break
        except:
            return render_template(
                'error.html'
            )
    return render_template(
        'demo.html',
        token=session.get('access_token'),
        info=ESTIMATE
    )

# not sure why this breaks everything when uncommented
# @app.route('/request', methods=['POST'])
# def request():
#     """Call a car."""
#     global REQUEST
    
#     url = config.get('sandbox_uber_url') + 'request'
#     params = {
#         'product_id': RIDE,
#         'start_latitude': LOC[0],
#         'start_longitude': LOC[1],
#         'end_latitude': LOC[2],
#         'end_longitude': LOC[3] 
#     }
#     response = app.requests_session.get(
#         url,
#         headers=generate_ride_headers(session.get('access_token')),
#         params=params
#     )

#     REQUEST = json.loads(response.text)
#     REQUEST = ['request_id']

#     if response.status_code != 200:
#         return 'There was an error', response.status_code
#     return render_template(
#         'demo.html',
#         token=session.get('access_token'),
#         info=REQUEST
#     )

# should be DELETE request, though not easy in flask
@app.route('/cancel', methods=['POST'])
def cancel():
    """Cancel a currently called uber product."""
    url = config.get('base_uber_url') + 'cancel'
    params = {
        request_id: REQUEST
    }
    response = app.requests_session.get(
        url,
        headers=generate_ride_headers(session.get('access_token')),
    )
    if response.status_code != 204:
        return 'There was an error', response.status_code
    return render_template(
        'demo.html',
        token=session.get('access_token'),
        info='Cancelled'
    )

def get_redirect_uri(request):
    """Return OAuth redirect URI."""
    parsed_url = urlparse(request.url)
    if parsed_url.hostname == 'localhost':
        return 'http://{hostname}:{port}/submit'.format(
            hostname=parsed_url.hostname, port=parsed_url.port
        )
    return 'https://{hostname}/submit'.format(hostname=parsed_url.hostname)

if __name__ == '__main__':
    app.debug = os.environ.get('FLASK_DEBUG', True)
    app.run(port=3000)
