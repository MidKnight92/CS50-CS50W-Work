from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect

import markdown2
from . import util

def index(request):
    """ Index Page: Users can click on any entry name to be taken directly to that entry page"""
    # Check for query in search bar
    query = request.GET.get("q")
    if query:
        print(query)   
        return HttpResponse("todo")
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })

def entry(request, title):
    """Entry Page: Visiting /wiki/TITLE, where TITLE is the title of an encyclopedia entry, should render a page that displays the contents of that encyclopedia entry."""
    
    # Retrieve the Markdown contents of an Encyclopedia entry by its title, 
    entry = util.get_entry(title)

    # Entry exists
    if entry:
        
        # Convert the Markdown into HTML
        html = markdown2.markdown(entry)

        return render(request, "encyclopedia/entry.html", {
            "title": title.upper(),
            "content": html
        })
    # Entry does not exists 
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": "Error",
            "content": "<h1>Error: Page Not Found<h1>"
        })
        