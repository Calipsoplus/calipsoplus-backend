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
        try:
            # hrzmkr
            error_string = str(error.message)
        except Exception as e:
            error_string = ''
            self.logger.error(e)

        if not error_string:
            try:
                for error_key in error:
                    if error_string:
                        error_string += '; '
                    for error_value in error.get(error_key):
                        error_string += '%s, %s' % (error_key, error_value)
            except Exception as e:
                error_string = ''
                self.logger.error(e)

        if not error_string:
            error_string = str(error)

        return error_string
