from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse

import operator
import markdown2
from . import util


def index(request):
    """ Index Page: Users can click on any entry name to be taken directly to that entry page"""

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

def search(request):
    """ User can type a query into search box returns links to matches or redirects to match if applicable"""
    
    # Query was sent
    if request.POST.get("q"):

        # Check for query in search bar
        query = request.POST.get("q")
         # Upper case query
        query = query.upper()
        
        # Retrieve the Markdown contents of an Encyclopedia entry
        entry = util.get_entry(query)

        # Entry exist in encyclopedia
        if entry:
            
            return redirect(f"wiki/{query}")

        # Entry does not exist in encyclopedia run search
        else:

            # Query full list of entries
            entries = util.list_entries()

            # Uppercasee all entry name
            entries = [word.upper() for word in entries]
           
            # Check if query is a substring to entries
            match = [word for word in entries if query in word]

            return render(request, "encyclopedia/search.html", {
        "content": match
    })
    else:
        return render(request, "encyclopedia/search.html", {
"content": None
})


def new(request):
    return render(request, "encyclopedia/new.html")