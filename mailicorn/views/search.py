from mailicorn.services import Search
from mailicorn.validators import LoggedIn, ValidText

import boto

cs_conn = boto.cloudsearch.connect_to_region('us-east-1')


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
