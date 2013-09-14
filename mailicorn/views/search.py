from mailicorn.services import SearchTags, SearchText
from mailicorn.validators import LoggedIn, ValidText


@Search.get(validators=[LoggedIn, ValidText])
def SearchByParams(request):
    """
    ,<-
    {
        "to": "<query>",
        "from": "<query>",
        "cc": "<query>",
        "bcc": "<query>",
        "tags": "<query>",
        "mid": "<query>",
        "hasattachment": "<query>",
        "subject": "<query>",
        "fulltext": "<query>",
    }
    ->
    {
    "query": {input query json}
    "messages": [{ <message> }, ...]
    }
    """
    pass


