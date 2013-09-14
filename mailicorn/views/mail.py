from mailicorn.services import MailID, Mail, Sync
from mailicorn.validators import LoggedIn, ValidJSON, ValidFields, JSON
from mailicorn.models import DBSession
from mailicorn.models.users import User
from pyramid.httpexceptions import HTTPForbidden
from boto.sqs.message import Message
import boto
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


@Sync.post(validators=[LoggedIn])
def ForceSync(request):
    user = request.validated['user']
    sqs = boto.connect_sqs()
    sync_queue = sqs.get_queue(
        request.registry.settings['queue.sync'])
    msg = Message()
    msg.set_body(json.dumps({'uid': user.id, 'forced': True}))
    sync_queue.write(msg)



