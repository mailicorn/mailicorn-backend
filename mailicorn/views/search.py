from mailicorn.services import Search
from mailicorn.validators import LoggedIn, ValidJSON

import boto

cloudsearch = boto.connect_cloudsearch()
mail_search = cloudsearch.lookup('mailicorn-1')
search_service = mail_search.get_search_service()


@Search.get(validators=[LoggedIn, ValidJSON])
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
    tags = ["owner",
            "to",
            "from",
            "cc",
            "bcc",
            "tags",
            "mid",
            "hasattachment",
            "subject",
            "fulltext"]
    query = request.validated['json']
    result = search_service.search(
        q=query['fulltext'],
        facet=['owner'],
        facet_constraints={'owner': request.validated['user'].name})
    return result.docs
