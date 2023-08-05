import json
import sanic
from bson import ObjectId
from datetime import datetime
from .exceptions import APIError


async def _rest_error_handler(request, exception):
    return exception.to_response()


class _APIEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return float(o.strftime('%s'))*1000
        elif isinstance(o, ObjectId):
            return str(o)
        return super(_APIEncoder, self).default(o)


class RestEncoder:
    @staticmethod
    def init_app(app):
        # register rest error handler responsible to serialize custom exceptions
        app.error_handler.add(APIError, _rest_error_handler)

        @app.middleware('response')
        async def jsonify_response(request, response):
            # return original response if object is a response
            if isinstance(response, sanic.response.HTTPResponse):
                return response
            
            # if object is of unknown type, use custom api encoder
            return sanic.response.HTTPResponse(
                json.dumps(response, cls=_APIEncoder),
                content_type="application/json"
            )
