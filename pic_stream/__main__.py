""" Start"""

import flask
import uuid
from pic_stream.settings import HOST_NAME
from pic_stream.bin.auth import auth_bp

app = flask.Flask(__name__)
app.register_blueprint(auth_bp)


def main():
    app.secret_key = str(uuid.uuid4())
    app.debug = True
    app.run(host=HOST_NAME, port="80")


if __name__ == "__main__":
    main()
