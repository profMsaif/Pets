"""
define custom authintication method
in the project config we have an API_KEY parameter
all request handlers accept header X-API-KEY
matchin the api_key with the existing api_key

the key is intended to be away of accessing 
regradless of the user who is accessing 
the end point
"""

from typing import Tuple
from django.utils.translation import gettext_lazy as _
from pets.settings import API_KEY
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from rest_framework.authentication import BaseAuthentication


def get_authorization_header(request) -> bytes:
    """
    Return request's 'X-API-KEY:' header, as a bytestring.
    Hide some test client ickyness where the header can be unicode.
    """
    # get the X-API-KEY from the header encode it and return
    auth = request.META.get("HTTP_X_API_KEY", b"")
    if isinstance(auth, str):
        # Work around django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth


class ApiKeyAuthentication(BaseAuthentication):
    """
    Simple api-key based authentication.

    Clients should authenticate by passing the api key in the "X-API-KEY"
    HTTP header.  For example:

        X-API-KEY: 401f7ac837da42b97f613d789819ff93537bee6a
    """

    def authenticate(self, request) -> Tuple[None, str]:
        """check if the provided api_key is equal to the
        api_key in the project config
        raise Unauthorized error 401
        """
        api_key = get_authorization_header(request)

        try:
            api_key = api_key.decode()
        except UnicodeError:
            msg = _(
                "Invalid x-api-key header. x-api-key string should not contain invalid characters."
            )
            raise exceptions.AuthenticationFailed(msg)
        # if the keys are not the same raise Unauthorized error
        if API_KEY != api_key:
            raise exceptions.AuthenticationFailed(_("Unauthorized"))
        # else pass
        # if the key is generated to each user
        # then the first index of the returned value must be the user
        # who own this token
        return (None, API_KEY)
