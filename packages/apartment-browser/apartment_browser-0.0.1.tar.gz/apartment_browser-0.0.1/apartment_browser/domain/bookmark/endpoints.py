from sanic import Blueprint
from .services import BookmarkService


bp = Blueprint('bookmark')

@bp.get('/bookmarks')
async def list_bookmarks(request):
    return BookmarkService.search()

@bp.get('/bookmarks/<uid:string>')
def get_bookmark_details(request, uid):
    return BookmarkService.get_details(uid)

@bp.post('/bookmarks')
def create_bookmark(request):
    return BookmarkService.create(request.json)

@bp.put('/bookmarks/<uid:string>')
def create_bookmark(request, uid):
    return BookmarkService.update(uid, request.json)

@bp.delete('/bookmarks/<uid:string>')
def delete_bookmark(request, uid):
    return BookmarkService.delete(uid)
