# """ Pydantic data classes for oAuth"""

# from pydantic import BaseModel, Field

# CLIENT_ID_DESC = "Get client ID, client secret, scope, redirectURI. To get these credentials (CLIENT_ID CLIENT_SECRET) and for your application, visit: https://console.cloud.google.com/apis/credentials."


# class GoogleAuth(BaseModel):
#     client_id: Field(description=CLIENT_ID_DESC)
#     client_secret: str
#     session_secret: str
