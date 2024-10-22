from models import env


def requires_auth(f):
    """
    Determines if the Access Token is valid
    """
    import os
    import json
    import flask
    from functools import wraps
    import six
    from jose import jwt
    from .get_token_auth_header import get_token_auth_header
    from .Auth_Error import Auth_Error
    from service.GCP_Secret_Manager_Service import GCP_Secret_Manager_Service

    @wraps(f)
    def decorated(*args, **kwargs):
        audience = os.getenv(
            "AUTH0_AUDIENCE"
        ) or GCP_Secret_Manager_Service().get_secret(f"{env.upper()}_AUTH0_AUDIENCE")
        auth0_domain = os.getenv(
            "AUTH0_DOMAIN"
        ) or GCP_Secret_Manager_Service().get_secret(f"{env.upper()}_AUTH0_DOMAIN")
        token = get_token_auth_header()
        jsonurl = six.moves.urllib.request.urlopen(
            "https://" + auth0_domain + "/.well-known/jwks.json"
        )
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=os.getenv("ALGORITHMS"),
                    audience=audience,
                    issuer="https://" + auth0_domain + "/",
                )
            except jwt.ExpiredSignatureError:
                raise Auth_Error(
                    {"code": "token_expired", "description": "token is expired"}, 401
                )
            except jwt.JWTClaimsError:
                raise Auth_Error(
                    {
                        "code": "invalid_claims",
                        "description": "incorrect claims,"
                        "please check the audience and issuer",
                    },
                    401,
                )
            except Exception:
                raise Auth_Error(
                    {
                        "code": "invalid_header",
                        "description": "Unable to parse authentication" " token.",
                    },
                    401,
                )

            flask._request_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)
        raise Auth_Error(
            {"code": "invalid_header", "description": "Unable to find appropriate key"},
            401,
        )

    return decorated
