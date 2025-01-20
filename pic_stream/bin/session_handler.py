""" Module that initiates and handles the user session a successful oAuth request."""


class UserSessionHandler:
    """Class to handle photo picker sessions."""

    def __init__(self, session: dict):
        """Takes in the Json Response from the API"""
        self.raw_session = session
        self.sessions = {}

    def parse_session(self):
        """Takes and validates the PickingSession Json Response from the API and parses it into it's components."""
        # TODO: validate session with pydantic
        if isinstance(self.raw_session, dict):
            for k, v in self.raw_session.items():
                setattr(self, k, v)

        self.sessions[self.id] = self.raw_session

    def poll_media(self):
        """Checks if mediaItemsSet has been set and polls the service using the PollingConfig object until mediaItemsSet is set."""

        # When within the session expiry time, use GET session to poll.
        # {
        # "pollInterval": string,
        # "timeoutIn": string
        # }

        # If mediaItemsSet

    def Picker_uri_handler(self):
        """ Parses the picker URI and shows it in a QR code"""
