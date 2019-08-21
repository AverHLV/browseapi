from .containers import ErrorDetailV3


class BrowseAPIError(Exception):
    """ Browse API base exception """

    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg


class BrowseAPIRequestError(BrowseAPIError):
    """ Browse API request exception """

    def __init__(self, msg: str, uri: str):
        super().__init__(msg)
        self.uri = uri

    def __str__(self):
        return '{0}, uri: {1}'.format(self.msg, self.uri)


class BrowseAPIResponseError(BrowseAPIError):
    """ Browse API response exception """

    def __init__(self, error: dict, msg='Response error'):
        super().__init__(msg)
        self.error = ErrorDetailV3(error)

    def __str__(self):
        return '{0}, details: {1}'.format(self.msg, self.error)


class BrowseAPIOAuthError(BrowseAPIError):
    """ Browse API OAuth response error """

    def __init__(self, request_body: dict, msg='Response has an unexpected format'):
        super().__init__(msg)
        self.response_body = request_body

    def __str__(self):
        return '{0}, response body: {1}'.format(self.msg, self.response_body)


class BrowseAPIParamError(BrowseAPIError):
    def __init__(self, param: str, msg='Wrong parameter value'):
        super().__init__(msg)
        self.param = param

    def __str__(self):
        return '{0}: {1}'.format(self.msg, self.param)


class BrowseAPIMethodError(BrowseAPIError):
    pass


class BrowseAPIInvalidUri(BrowseAPIRequestError):
    pass


class BrowseAPIMimeTypeError(BrowseAPIRequestError):
    pass


class BrowseAPITimeoutError(BrowseAPIRequestError):
    pass


class BrowseAPIConnectionError(BrowseAPIRequestError):
    pass


class BrowseAPIRequestOAuthError(BrowseAPIResponseError):
    pass


class BrowseAPIAccessError(BrowseAPIResponseError):
    pass


class BrowseAPIRoutingError(BrowseAPIResponseError):
    pass


class BrowseAPIInternalError(BrowseAPIResponseError):
    pass


class BrowseAPIRequestParamError(BrowseAPIResponseError):
    pass


class BrowseAPIBusinessError(BrowseAPIResponseError):
    pass
