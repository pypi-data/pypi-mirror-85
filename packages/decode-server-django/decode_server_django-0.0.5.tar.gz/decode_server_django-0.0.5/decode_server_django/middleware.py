from django.conf import settings
from jose import jwt, JWTError, ExpiredSignatureError
from jose.exceptions import JWTClaimsError
from django.http import JsonResponse
from rsa import pem


class DecodeAuthMiddleware(object):
    """
    Decode Auth middleware. Authenticates incoming requests from Decode Auth.
    """

    def __init__(self, get_response):
        self.get_response = get_response

        decodePublicKey = settings.DECODE_PUBLIC_KEY

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

    def __call__(self, request):

        # if the token isn't in the header, we assume that
        # the call wasn't made from Decode Auth
        if "decode-token" not in request.headers:
            error = ValueError(
                "This endpoint must be called through the Decode Auth proxy."
            )
            return self.returnError(error)

        decodeToken = request.headers["decode-token"]

        try:
            self.validateToken(decodeToken, self.decodePublicKey)
            return self.get_response(request)
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
        return JsonResponse({
            "ok": False,
            "error": {
                "summary": f"Authorization failed: {error}"
            }
        }, status=401)
