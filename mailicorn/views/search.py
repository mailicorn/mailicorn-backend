from mailicorn.services import Search
from mailicorn.validators import LoggedIn, ValidJSON

import boto

cloudsearch = boto.connect_cloudsearch()
mail_search = cloudsearch.lookup('mailicorn-2')
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
    "folder": "<query>"
    }
    ->
    {
    "query": {input query json}
    "messages": [{ <message> }, ...]
    }
    """
    facets = [
        "owner",
        "folder",
        "hasattachment",
    ]
    fields = [
        "mid",
        "from",
        "to",
        "cc",
        "bcc",
        "tags",
        "subject",
        "fulltext",
    ]
    querydict = request.validated['json']
    query_params = {
        'return_fields': ['mid', 'subject', 'tags', 'from'],
    }
    if any([querydict.get(f, None) is not None for f in facets]):
        print ("Got some facets")
        for facet, constraint in [(f, querydict.get(f, None)) for f in facets
                                  if querydict.get(f, None) is not None]:
            query_params['facet'] = query_params.get('facet', []) + [facet]
            f = query_params.get('facet_constraints', {})
            f[facet] = constraint
            query_params['facet_constraints'] = f

    for t in fields:
        if querydict.get(t, None) is not None:
            # add it to the query
            query_params['q'] = query_params.get('q', '') + querydict[t] + ' '

    query_params['bq'] = "(and '%s' (field owner '%s' ))" %(query_params.pop('q').strip(), request.validated['user'].name)
    result = search_service.search(**query_params)
    return result.docs

if __name__ == '__main__':
    class fakeuser(object):
        name = 'rad'

    class FakeRequest(object):
        validated = {
            'json': {
                'fulltext': 'Glass',
            },
            'user': fakeuser(),
        }
    from pprint import pprint
    pprint(SearchByParams(FakeRequest()))
