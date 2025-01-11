""" Start"""

import json
import flask
import requests
import uuid

app = flask.Flask(__name__)

# Open and read the JSON file
with open(
    "/Users/prasadkoshyjose/personalProjects/PicStream/secrets.json", "r"
) as file:
    config = json.load(file)["installed"]

# Get client ID, client secret, scope, redirectURI
# To get these credentials (CLIENT_ID CLIENT_SECRET) and for your application, visit
# https://console.cloud.google.com/apis/credentials.
CLIENT_ID = config["client_id"]
CLIENT_SECRET = config["client_secret"]
# Access scopes for two non-Sign-In scopes: Read-only Drive activity and Google Calendar.
SCOPE = "profile https://www.googleapis.com/auth/photospicker.mediaitems.readonly"


# Indicate where the API server will redirect the user after the user completes
# the authorization flow. The redirect URI is required. The value must exactly
# match one of the authorized redirect URIs for the OAuth 2.0 client, which you
# configured in the API Console. If this value doesn't match an authorized URI,
# you will get a 'redirect_uri_mismatch' error.
REDIRECT_URI = "http://localhost/oauth2callback"


@app.route("/")
def index():
    if "credentials" not in flask.session:
        return flask.redirect(flask.url_for("oauth2callback"))

    credentials = json.loads(flask.session["credentials"])

    if credentials["expires_in"] <= 0:
        return flask.redirect(flask.url_for("oauth2callback"))
    else:
        # User authorized the request. Now, check which scopes were granted.
        if (
            "https://www.googleapis.com/auth/photospicker.mediaitems.readonly"
            in credentials["scope"]
        ):
            # User authorized read-only Drive activity permission.
            params = {"Authorization": "Bearer {}".format(credentials["access_token"])}
            req_uri = "https://photospicker.googleapis.com/v1/sessions/"
            r = requests.post(req_uri, headers=params).text
        else:
            # User didn't authorize read-only Drive activity permission.
            # Update UX and application accordingly
            r = "User did not authorize photo permission."

    return r


@app.route("/oauth2callback")
def oauth2callback():
    if "code" not in flask.request.args:
        state = str(uuid.uuid4())
        flask.session["state"] = state
        # Generate a url that asks permissions for the Drive activity
        # and Google Calendar scope. Then, redirect user to the url.
        auth_uri = (
            "https://accounts.google.com/o/oauth2/v2/auth?response_type=code"
            "&client_id={}&redirect_uri={}&scope={}&state={}"
        ).format(CLIENT_ID, REDIRECT_URI, SCOPE, state)
        return flask.redirect(auth_uri)
    else:
        if (
            "state" not in flask.request.args
            or flask.request.args["state"] != flask.session["state"]
        ):
            return "State mismatch. Possible CSRF attack.", 400

        auth_code = flask.request.args.get("code")
        data = {
            "code": auth_code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        # Exchange authorization code for access and refresh tokens (if access_type is offline)
        r = requests.post("https://oauth2.googleapis.com/token", data=data)
        flask.session["credentials"] = r.text
        return flask.redirect(flask.url_for("index"))


def main():
    app.secret_key = str(uuid.uuid4())
    app.debug = False
    app.run(host="localhost", port="80")


if __name__ == "__main__":

    main()
