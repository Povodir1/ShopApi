class BaseDomainException(Exception):
    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(self.detail)


class ObjectNotFoundError(BaseDomainException):
    pass

class ObjectAlreadyExistError(BaseDomainException):
    pass

class InvalidDataError(BaseDomainException):
    pass

class NoMoneyError(BaseDomainException):
    pass

class UnauthorizedError(BaseDomainException):
    pass

class NoPermissionsError(BaseDomainException):
    pass