import functools


class KEError(Exception):
    def __init__(self, error_message="", response_code=None, response_body=None):

        Exception.__init__(self, error_message)
        # Http status code
        self.response_code = response_code
        self.response_body = response_body

    def __str__(self):
        if self.response_code is not None:
            return "{0}: {1}".format(self.response_code, self.error_message)
        else:
            return "{0}".format(self.error_message)


class ResourceUnavailable(Exception):
    """Exception representing a failed request to a resource"""

    def __init__(self, msg, http_response):
        Exception.__init__(self)
        self._msg = msg
        self._status = http_response.status_code

    def __str__(self):
        return "%s (HTTP status: %s)" % (self._msg, self._status)


class AuthenticationError(KEError):
    pass
