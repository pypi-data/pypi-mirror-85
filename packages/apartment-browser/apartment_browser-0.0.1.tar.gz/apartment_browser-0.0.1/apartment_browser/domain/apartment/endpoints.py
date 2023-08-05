from sanic import Blueprint
from .services import ApartmentService


bp = Blueprint('apartment')

@bp.get('/apartments')
async def list_apartments(request):
    return ApartmentService.search()

@bp.get('/apartments/<uid:string>')
def get_apartment_details(request, uid):
    return ApartmentService.get_details(uid)

@bp.post('/apartments')
def create_apartment(request):
    return ApartmentService.create(request.json)

@bp.put('/apartments/<uid:string>')
def create_apartment(request, uid):
    return ApartmentService.update(uid, request.json)

@bp.delete('/apartments/<uid:string>')
def delete_apartment(request, uid):
    return ApartmentService.delete(uid)
