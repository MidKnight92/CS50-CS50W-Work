from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect

from . import util

from util import get_entry, list_entries, save_entry

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    """Entry Page: Visiting /wiki/TITLE, where TITLE is the title of an encyclopedia entry, should render a page that displays the contents of that encyclopedia entry.
        The view should get the content of the encyclopedia entry by calling the appropriate util function.
        If an entry is requested that does not exist, the user should be presented with an error page indicating that their requested page was not found.
        If the entry does exist, the user should be presented with a page that displays the content of the entry. The title of the page should include the name of the entry."""
    entry = get_entry(title)
    if entry:
        print(entry)
        return(render, "encyclopedia/entry.html", {
            "entry": entry
        })
    else:
        return HttpResponseNotFound('<h1>Page not Found<h1>')