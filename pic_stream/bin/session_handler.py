""" Module that initiates and handles the user session a successful oAuth request."""


class UserSessionHandler:
    """Class to handle photo picker sessions."""

    def __init__(self, session: dict):
        """Takes in the Json Response from the API"""
        self.raw_session = session

    def parse_session(self):
        """Takes and validates the PickingSession Json Response from the API and parses it into it's components."""
        # TODO: validate session with pydantic
        for k, v in self.raw_session.items():
            setattr(self, k, v)
