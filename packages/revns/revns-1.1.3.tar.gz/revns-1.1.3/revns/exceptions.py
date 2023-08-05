class NtfnException(Exception):
    def __init__(self, code, detail):
        self.code = code
        self.detail = detail
        msg = f'{code}: {detail}'
        super().__init__(self, msg)

class PublishError(NtfnException):
    pass

class UserAddError(NtfnException):
    pass
