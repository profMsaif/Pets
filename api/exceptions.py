from  rest_framework import exceptions, status
from django.utils.translation import gettext_lazy as _


class FileNameWithoutExtension(Exception):
    ...


class UnAuthorizedAccess(exceptions.APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _("Incorrect API KEY.")
    default_code = "Unauthorized"
