"""
Instanciate sanic asgi app to expose an API,
and register middleware and endpoints.
"""
import sanic
from .coreutils.middlewares import RestEncoder
from .routes import register_routes

asgi_app = sanic.Sanic()

# register middlewares
RestEncoder.init_app(asgi_app)

# register routes in current app
register_routes(asgi_app)
