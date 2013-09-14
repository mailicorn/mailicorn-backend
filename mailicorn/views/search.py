from mailicorn.services import Search
from mailicorn.validators import LoggedIn, ValidText

import boto


@Search.get(validators=[LoggedIn, ValidText])
def SearchByParams(request):
    """
    ,<-
    {
        "owner": "<query>"
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
