from werkzeug.wrappers import Request
from jose import jwt, JWTError, ExpiredSignatureError
from jose.exceptions import JWTClaimsError
from flask import abort
from rsa import pem


class decode_server_flask():
    """
    Decode Auth middleware. Authenticates incoming requests from Decode Auth.
    """

    def __init__(self, app, decodePublicKey):
        self.app = app
        if decodePublicKey is None:
            raise ValueError(
                "Configuration error: You didn't suply a decode public key")

        # try to parse the key, throws if it doesn't work
        try:
            pem.load_pem(decodePublicKey, "RSA PUBLIC KEY")
            self.decodePublicKey = decodePublicKey
        except ValueError as e:
            raise ValueError(
                f"Configuration error: the public key is malformed: {e}")

    def __call__(self, environ, start_response):
        request = Request(environ)
        decodeToken = request.headers.get("decode-token")

        # if the token isn't in the header, we assume that
        # the call wasn't made from Decode Auth
        if decodeToken is None:
            error = ValueError(
                "This endpoint must be called through the Decode Auth proxy."
            )
            return self.returnError(error)

        try:
            self.validateToken(decodeToken, self.decodePublicKey)
            return self.app(environ, start_response)
        except JWTError as error:
            return self.returnError(error)
        except ExpiredSignatureError as error:
            return self.returnError(error)
        except JWTClaimsError as error:
            return self.returnError(error)

    def validateToken(self, decodeToken, decodePublicKey):
        jwt.decode(decodeToken, decodePublicKey, algorithms="RS256",
                   audience="Decode", issuer="Decode")

    def returnError(self, error):
        response = {
            "ok": False,
            "error": {
                "summary": f"Authorization failed {error}"
            }
        }
        return abort(401, response)
