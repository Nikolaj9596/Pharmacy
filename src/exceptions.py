class BadRequestEx(Exception):
    def __init__(self, detail: str):
        self.detail = detail

class NotFoundEx(Exception):
    def __init__(self, detail: str):
        self.detail = detail
