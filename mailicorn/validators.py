import json
from mailicorn.models import DBSession, User
from pyramid.security import authenticated_userid
from pyramid.httpexceptions import HTTPUnauthorized, HTTPExpectationFailed
from re import compile


def LoggedIn(request):
    """
    Make sure we have a valid user
    """
    email = authenticated_userid(request)
    valid = False
    if email:
        user_query = DBSession.query(User).filter(User.email==email)
        if user_query.count() > 0:
            user = user_query.first()
            request.validated['user'] = user
            valid = True
    if not valid:
        return HTTPUnauthorized()


def _html_replace(text):
    """
    Replace html tags from the given text
    """
    html_tags = compile("(?'tag_start'</?)(?'tag'\w+)((\s+(?'attr'(?'attr_name'\w+)(\s*=\s*(?:"".*?""|'.*?'|[^'"">\s]+)))?)+\s*|\s*)(?'tag_end'/?>)")
    return html_tags.sub('', text)


def ValidFields(*fields):
    """
    Give a list of keys make sure they are all
    in the json blob given in the body
    """
    def validator(request):
        data = json.loads(request.body)
        for key in fields:
            if key not in data:
                return HTTPExpectationFailed()


def ValidJSON(request):
    """
    Strip any html from a json blob
    """
    data = json.loads(request.body)
    for key, value in data.items():
        data[key] = _html_replace(value)
    request.validated['json'] = data


def ValidText(request):
    """
    Strip html from the matchdict values
    """
    for key, value in request.matchdict.items():
        request.matchdict[key] = _html_replace(value)
