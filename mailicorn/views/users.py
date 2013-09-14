from mailicorn.services import Users, UsersLogin, UsersLogout
from mailicorn.validators import UserValidator, LoggedIn, ValidText


@Users.post(validators=[UserValidator])
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


@UsersLogin.post(validators=[ValidText])
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

