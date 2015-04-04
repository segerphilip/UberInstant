Boilerplate from: 
[![TravisCI](https://travis-ci.org/uber/Python-Sample-Application.svg?branch=master)](https://travis-ci.org/uber/Python-Sample-Application)

How To Use This
---------------

1. Navigate over to https://developer.uber.com/, and sign up for an Uber developer account.
2. Register a new Uber application and make your Redirect URI `http://localhost:3000/submit` - ensure that both the `profile` and `history` OAuth scopes are checked.
3. Fill in the relevant information in the `config.json` file in the root folder and add your client id and secret as the environment variables `UBER_KEY` and `UBER_SECRET`.
4. Run `pip install -r requirements.txt` to install dependencies
5. Run `python app.py`
6. Navigate to http://localhost:3000 in your browser