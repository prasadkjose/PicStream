""" Module that initiates and handles the user session a successful oAuth request."""

import json
import requests
import flask
import webbrowser
from pic_stream.settings import LOGGER, GOOGLE_URLS


class UserSessionHandler:
    """Class to handle photo picker sessions."""

    def __init__(self, session: dict, oauth_params: dict):
        """Takes in the Json Response from the API"""
        self.raw_session = json.loads(session)
        self.oauth_params = oauth_params
        self.sessions = {}

    def parse_session(self, raw_session: str = None):
        """Takes and validates the PickingSession Json Response from the API and parses it into it's components."""

        session_dict = (
            json.loads(raw_session) if raw_session is not None else self.raw_session
        )
        # TODO: validate session with pydantic
        if isinstance(session_dict, dict):
            for k, v in self.raw_session.items():
                setattr(self, k, v)

        LOGGER.info(" - Successfully parsed %s", self.id)

        return flask.redirect(self.pickerUri)
        return True

    def poll_media(self):
        """Checks if mediaItemsSet has been set and polls the service using the PollingConfig object until mediaItemsSet is set."""

        # When within the session expiry time, use GET session to poll.
        # {
        # "pollInterval": string,
        # "timeoutIn": string
        # }

        # If mediaItemsSet
        # if self.mediaItemsSet is False:
        #     polledSessionObj = requests.get(
        #         GOOGLE_URLS["sessions"] + self.id, headers=self.oauth_params
        #     )
        #     self.parse_session(polledSessionObj)
        # else:

        # call the mediaset API
        media_items = requests.get(
            GOOGLE_URLS["media_items"], headers=self.oauth_params
        )
        return "mediaItems" + str(media_items)
