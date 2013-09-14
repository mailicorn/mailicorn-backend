from mailicorn.services import MailID, Mail
from mailicorn.validators import LoggedIn, ValidJSON, ValidFields, JSON
from mailicorn.models import DBSession
from mailicorn.models.users import User
from pyramid.httpexceptions import HTTPForbidden
import pylibmc
import json


@MailID.get(validators=[LoggedIn])
def GetMailByID(request):
    cache = pylibmc.Client([
        request.register.settings['cache.uri'],
    ])
    data = json.loads(cache.get(request.matchdict['id']))
    if data['owner_id'] == request.validated['user'].id:
        return data
    else:
        return HTTPForbidden()


@Mail.get(validators=[LoggedIn])
def GetMailIDs(request):
    mids = [m.id for m in  request.validated['user'].messages]
    return {'mids': mids}

