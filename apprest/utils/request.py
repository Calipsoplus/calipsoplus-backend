from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer

import logging


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class ErrorFormatting:
    """
    An ErrorFormatting that renders its content into a comma separated string.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def format(self, error):

        error_string = str(error)

        return error_string
