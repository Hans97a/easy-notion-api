class APICallLimitExceed(Exception):
    def __str__(self):
        return "The rate limit for incoming requests per integration is an average of three requests per second.\nwait few minutes..."


class APIKeyNotFound(Exception):
    pass


class UserNotFound(Exception):
    pass


class InvalidData(Exception):
    pass


class PageNotFound(Exception):
    pass


class APIErrorCore(Exception):
    pass
