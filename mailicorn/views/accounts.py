from mailicorn.services import Users, UsersLogin, UsersLogout
from mailicorn.validators import LoggedIn, ValidJSON, ValidFields, JSON
from mailicorn.models import DBSession
from mailicorn.models.users import User
from mailicorn.models.accounts import Account
from pyramid.security import remember, forget
from webob import Response


@Users.post(validators=[LoggedIn,
                        ValidJSON,
                        ValidFields('username',
                                    'password',
                                    'host',
                                    'port',
                                    'imap_root',
                                    'seperator',
                                    'sync_int',
                                    'ssl')])
def AddAccount(request):
    """
    ->
    {
        'username',
        'password',
        'host',
        'port',
        'imap_root',
        'seperator',
        'sync_int',
        'ssl'
    }
    <-
    {
        success: '',
        account_id: '',
        message: '',
    }
    """
    uid = request.validated['user'].id
    new_acc = Account(
        owner_id=uid,
        username=request.validated['json']['username'],
        password=request.validated['json']['password'],
        host=request.validated['json']['host'],
        port=request.validated['json']['port'],
        imap_root=request.validated['json']['imap_root'],
        seperator=request.validated['json']['seperator'],
        sync_int=request.validated['json']['sync_int'],
        ssl=request.validated['json']['ssl'],
    )
    DBSession.add(new_acc)
    DBSession.commit()
    return {
        'success': True,
        'account_id': new_acc.id,
        'message': 'Account created',
    }
