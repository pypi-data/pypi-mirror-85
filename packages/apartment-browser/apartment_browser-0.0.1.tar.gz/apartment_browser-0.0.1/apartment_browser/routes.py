"""
Define endpoints blueprints containing app routes.
"""
from .domain.apartment.endpoints import bp as apartments_endpoints
from .domain.bookmark.endpoints import bp as bookmarks_endpoints


def register_routes(asgi_app):
    """
    Function used to register blueprints in app.
    """
    asgi_app.blueprint(apartments_endpoints)
    asgi_app.blueprint(bookmarks_endpoints)
