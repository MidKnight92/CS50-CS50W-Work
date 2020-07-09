from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect

import markdown2
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    """Entry Page: Visiting /wiki/TITLE, where TITLE is the title of an encyclopedia entry, should render a page that displays the contents of that encyclopedia entry.
        The view should get the content of the encyclopedia entry by calling the appropriate util function.
        If an entry is requested that does not exist, the user should be presented with an error page indicating that their requested page was not found.
        If the entry does exist, the user should be presented with a page that displays the content of the entry. The title of the page should include the name of the entry."""
    
    # Retrieve the Markdown contents of an Encyclopedia entry by its title, 
    entry = util.get_entry(title)

    if entry:
        
        # Convert the Markdown into HTML
        html = markdown2.markdown(entry)

        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html
        })
    else:
        # return(render, "encyclopedia/entry.html", {
        #     "entry": "Error: Page Not Found"
        # })
        return HttpResponse('<h1>Page not Found<h1>')