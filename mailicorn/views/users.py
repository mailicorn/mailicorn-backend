from mailicorn.services import Users, UsersLogin, UsersLogout
from mailicorn.validators import LoggedIn, ValidJSON


@Users.post(validators=[ValidJSON])
def AddUser(request):
    """
    ->
    {
        username: <>,
        password: <>,
    }
    """
    pass


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


@UsersLogin.post(validators=[ValidJSON])
def LoginUser(requset):
    """
    -> Auth Cookies
    {
        success: <>,
        message: <>,
    }
    """
    pass


@UsersLogout.post(validators=[LoggedIn])
def LogoutUser(request):
    """
    {
        success: <>,
        message: <>,
    }
    """
    pass

