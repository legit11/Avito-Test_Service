from fastapi import HTTPException, status


class BidNotFoundException(HTTPException):
    def __init__(self, detail: str = "Предложение не найдено."):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class TenderNotFoundException(HTTPException):
    def __init__(self, detail: str = "Тендер не существует"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class OrganizationNotFoundException(HTTPException):
    def __init__(self, detail: str = "Организация не существует"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class UserNotFoundException(HTTPException):
    def __init__(self, detail: str = "Пользователь не существует или некорректен."):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class ForbiddenActionException(HTTPException):
    def __init__(self, detail: str = "Недостаточно прав для выполнения действия"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class ServerErrorException(HTTPException):
    def __init__(self, detail: str = "Некоторые проблемы на сервере"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)