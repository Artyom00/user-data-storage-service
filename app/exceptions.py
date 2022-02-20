class BadRequestResponse(Exception):
    def __init__(self, message: str):
        self.message = message


class ErrorResponse(BadRequestResponse):
    def __init__(self, message, status_code: int):
        super().__init__(message)
        self.status_code = status_code
