import base64
import json
import time

from google.appengine.api import app_identity

DEFAULT_SERVICE_ACCOUNT = app_identity.get_service_account_name()


def generate_jwt():
    """Generates a signed JSON Web Token using the Google App Engine default
    service account."""
    now = int(time.time())

    header_json = json.dumps({
        "typ": "JWT",
        "alg": "RS256"
    })

    payload_json = json.dumps({
        'iat': now,
        "exp": now + 3600,
        'iss': DEFAULT_SERVICE_ACCOUNT,
        'sub': DEFAULT_SERVICE_ACCOUNT,
        'aud': 'ingestion_pipeline',
        "email": DEFAULT_SERVICE_ACCOUNT
    })

    headerAndPayload = '{}.{}'.format(base64.urlsafe_b64encode(header_json), base64.urlsafe_b64encode(payload_json))
    (key_name, signature) = app_identity.sign_blob(headerAndPayload)
    signed_jwt = '{}.{}'.format(headerAndPayload, base64.urlsafe_b64encode(signature))

    return signed_jwt
