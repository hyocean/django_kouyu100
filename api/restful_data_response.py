import traceback
import json
from kouyu100_managent import settings


class RestFulObject:
    def __init__(self):
        self.retObj = settings.responseMessage
        self.retObj.clear()

    def success(self, data):
        self.retObj['code'] = 20000
        self.retObj['status'] = True
        self.retObj['data'] = data

    def error(self, message):
        self.retObj['code'] = 404
        self.retObj['status'] = False
        self.retObj['message'] = message

    def ret(self):
        return self.retObj
