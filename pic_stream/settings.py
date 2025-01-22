"""Global settings for the tool."""

import json
import os
import sys
import logging
import pic_stream.constants as constants

# setup configuration for logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
)

LOGGER = logging.getLogger(__name__)

HOST_NAME = "pony-safe-stag.ngrok-free.app"

GOOGLE_URLS = {
    "sessions": "https://photospicker.googleapis.com/v1/sessions/",
    "photospicker_ro_scope": "https://www.googleapis.com/auth/photospicker.mediaitems.readonly",
    "oAuth": "https://accounts.google.com/o/oauth2/v2/auth",
    "media_items": "https://photospicker.googleapis.com/v1/mediaItems",
}

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(ROOT_DIR, os.pardir))

# Open and read the secrets JSON file
try:
    with open(os.path.join(PROJECT_DIR, "secrets.json"), "r", encoding="utf-8") as file:
        secrets_json_raw = json.load(file)
except Exception as ex:
    raise ex


def parse_secrets(secrets_dict: dict):
    """
    Parses a dictionary of secrets and separates them into two categories:
    individual key-value pairs and nested structures.

    Args:
        secrets_dict (dict): A dictionary containing secrets, which may include
                             both flat key-value pairs and nested dictionaries.

    Returns:
        list[dict] | dict:
            - A dictionary of flat key-value pairs extracted from `secrets_dict`.
            - A list of dictionaries representing nested structures in `secrets_dict`.
    """

    secret_list = list(secrets_dict.values())
    return secret_list[0] if len(secret_list) == 1 else secret_list


# Util method to exit the tool gracefully
def exit_gracefully(error):
    """
    Exits the tool gracefully, logging the error and performing cleanup if needed.

    Args:
        error (Exception or str): The error that caused the exit, or a descriptive message.

    Returns:
        None
    """
    try:
        # Log the error details
        if isinstance(error, Exception):
            LOGGER.error(" - Exiting due to an exception: %s", str(error))
        else:
            LOGGER.error(" - Exiting due to an error: %s", error)

        # Perform any cleanup operations if necessary
        LOGGER.info(" - Performing cleanup operations...")

        # Exit the program with a non-zero status code to indicate failure
        sys.exit(1)
    except Exception as cleanup_error:
        LOGGER.critical(" - An error occurred during cleanup: %s", str(cleanup_error))
        sys.exit(1)


config = parse_secrets(secrets_json_raw)


def get_constant(name):
    """
    Retrieve the value of a constant from the constants module.

    :param name: The name of the constant to retrieve.
    :return: The value of the constant.
    :raises AttributeError: If the constant is not defined in constants.py.
    """
    try:
        return getattr(constants, name)
    except AttributeError as e:
        raise AttributeError(f"Constant '{name}' not found in constants.py") from e
