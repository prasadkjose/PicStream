""" Authorisation module for 3rd party APIs"""

import json
import flask
import requests
import uuid
from pic_stream.settings import config, HOST_NAME, GOOGLE_URLS

# from pic_stream.models.oauth_models import GoogleAuth
from pic_stream.bin.session_handler import UserSessionHandler

# Validate the auth model
auth_config = config
CLIENT_ID = auth_config["client_id"]
CLIENT_SECRET = auth_config["client_secret"]

# Access scopes.
SCOPE = "profile https://www.googleapis.com/auth/photospicker.mediaitems.readonly"
auth_bp = flask.Blueprint("auth", __name__)


# Indicate where the API server will redirect the user after the user completes
# the authorization flow. The redirect URI is required. The value must exactly
# match one of the authorized redirect URIs for the OAuth 2.0 client, which you
# configured in the API Console. If this value doesn't match an authorized URI,
# you will get a 'redirect_uri_mismatch' error.
REDIRECT_URI = "https://" + HOST_NAME + "/oauth2callback"


@auth_bp.route("/")
def index():
    if "credentials" not in flask.session:
        return flask.redirect(flask.url_for("auth.oauth2callback"))

    credentials = json.loads(flask.session["credentials"])
    print("credentials loaded")

    if credentials["expires_in"] <= 0:
        return flask.redirect(flask.url_for("auth.oauth2callback"))
    else:
        # User authorized the request. Now, check which scopes were granted.
        print("request session")
        if GOOGLE_URLS["photospicker_ro_scope"] in credentials["scope"]:
            # User authorized read-only Photos activity permission.
            oauth_params = {
                "Authorization": "Bearer {}".format(credentials["access_token"])
            }
            req_uri = GOOGLE_URLS["sessions"]
            response_session_dict = requests.post(req_uri, headers=oauth_params).text

            # Take the PickingSession object and get session ID, redirect URL for picker, pollingConfig, expiry time
            session = UserSessionHandler(response_session_dict, oauth_params)
            # parse_result = session.parse_session()
            r = session.parse_session()

        else:
            # User didn't authorize read-only Photo activity permission.
            r = "User did not authorize photo permission."

    return r


@auth_bp.route("/media")
def media():
    credentials = json.loads(flask.session["credentials"])
    oauth_params = {"Authorization": "Bearer {}".format(credentials["access_token"])}

    media_items = requests.get(GOOGLE_URLS["media_items"], headers=oauth_params)
    return "mediaItems" + str(media_items)


@auth_bp.route("/oauth2callback")
def oauth2callback():
    print("oauth2callback")
    if "code" not in flask.request.args:
        state = str(uuid.uuid4())
        flask.session["state"] = state
        # Generate a url. Then, redirect user to the url.
        auth_uri = (
            GOOGLE_URLS["oAuth"]
            + f"?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope={SCOPE}&state={state}"
        )

        return flask.redirect(auth_uri)
    else:
        if (
            "state" not in flask.request.args
            or flask.request.args["state"] != flask.session["state"]
        ):
            return "State mismatch. Possible CSRF attack.", 400

        auth_code = flask.request.args.get("code")
        print("request credentials")

        data = {
            "code": auth_code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        # Exchange authorization code for access and refresh tokens (if access_type is offline)
        r = requests.post("https://oauth2.googleapis.com/token", data=data)
        print(f"request successful: {r.text}")

        flask.session["credentials"] = r.text
        return flask.redirect(flask.url_for("auth.index"))
