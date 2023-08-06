class BaseError(Exception):

    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return f'<{self.__class__.__name__}({self.reason})>'


class NotFoundError(BaseError):
    pass


class DataError(BaseError):
    pass


class ValidationError(BaseError):
    pass
