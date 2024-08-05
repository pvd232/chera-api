import jwt


class JWTTokenService(object):
    def __init__(self, jwt_secret: str):
        self.secret: str = jwt_secret

    def issue_token(self, identifier):
        jwt_token = jwt.encode({"sub": identifier}, key=self.secret, algorithm="HS256")
        return jwt_token

    def validate_token(self, session_token: str):
        return jwt.decode(session_token, self.secret, algorithms=["HS256"])
