from mailicorn.services import SearchTags, SearchText
from mailicorn.validators import LoggedIn, ValidText


@SearchTags.get(validators=[LoggedIn, ValidText])
def SearchByTags(request):
    """
    ->
    {
        messages: []
    }
    """
    pass


@SearchText.get(validators=[LoggedIn, ValidText])
def SearchByFullText(request):
    """
    ,<-
    {
        text: ""
    }
    ->
    {
        messages: []
    }
    """
    pass


