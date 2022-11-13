class BaseResponse(object):
    def __init__(self):
        self.status = False
        self.error = None
        self.data = None

    @property
    def dict(self):
        return self.__dict__
