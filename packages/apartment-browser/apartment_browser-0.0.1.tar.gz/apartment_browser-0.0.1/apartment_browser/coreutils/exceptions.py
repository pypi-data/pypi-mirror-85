import sanic
import json

class APIError(Exception):
    def __init__(self, message, status=500, **info):
        self._json = dict(message=message, **info)
        self._status = status

    def to_response(self):
        return sanic.response.json(
            self._json, status=self._status
        )
