from mailicorn.services import Accounts
from mailicorn.validators import LoggedIn, ValidJSON, ValidFields
from mailicorn.models import DBSession
from mailicorn.models.accounts import Account


@Accounts.post(validators=[LoggedIn,
                           ValidJSON,
                           ValidFields('username',
                                       'password',
                                       'host',
                                       'port',
                                       'imap_root',
                                       'seperator',
                                       'folders',
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
        'folders',
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
    folders = request.validated['json']['folders']
    if isinstance(folders, list):
        new_acc.folders = folders
    else:
        new_acc.folders = [folders, ]
    print new_acc.owner_id
    DBSession.add(new_acc)
    DBSession.commit()
    return {
        'success': True,
        'account_id': new_acc.id,
        'message': 'Account created',
    }
