from mailicorn.services import Users, UsersLogin, UsersLogout
from mailicorn.validators import LoggedIn, ValidJSON, ValidFields, JSON
from mailicorn.models import DBSession
from mailicorn.models.users import User
from pyramid.httpexceptions import HTTPConflict, HTTPUnauthorized
from pyramid.security import remember, forget
from webob import Response
import hashlib


@Users.post(validators=[ValidJSON, ValidFields('username', 'password', 'email')])
def AddUser(request):
    """
    ->
    {
        username: <>,
        password: <>,
    }
    <-
    {
        success: '',
        message: '',
    }
    """
    username = request.validated['json']['username']
    password= request.validated['json']['password']
    email = request.validated['json']['email']
    hashed_pass = hashlib.sha512(password).hexdigest()
    if DBSession.query(User).filter(User.name==username).count() > 0:
        return HTTPConflict()
    new_user = User(name=username,
                    password=hashed_pass,
                    email=email
                    )
    DBSession.add(new_user)
    DBSession.commit()
    return LoginUser(request)




@Users.delete(validators=[LoggedIn])
def RemoveUser(request):
    """
    ->
    {
        username: <>,
        password: <>,
    }
    """
    pass


@Users.get(validators=[LoggedIn])
def GetUserInfo(request):
    """
    <-
    {
        username: <>,
        accounts: [],
        rules: []
    }
    """
    pass


@UsersLogin.post(validators=[JSON, ValidFields('username', 'password')])
def LoginUser(request):
    """
    -> Auth Cookies
    {
        success: <>,
        message: <>,
    }
    """
    username = request.validated['json']['username']
    password = request.validated['json']['password']
    hashed_pass = hashlib.sha512(password).hexdigest()

    user_query = DBSession.query(User).filter(User.name==username)
    if user_query.count() == 0:
        return HTTPUnauthorized()
    user = user_query.one()
    if user.password == hashed_pass:
        headers = remember(request, user.email)
        resp = Response()
        resp.headerlist.extend(headers)
        return resp
    else:
        return HTTPUnauthorized()


@UsersLogout.post(validators=[LoggedIn])
def LogoutUser(request):
    """
    {
        success: <>,
        message: <>,
    }
    """
    pass

