from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django import forms
import operator
import markdown2
from . import util
# from .forms import EntryForm

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    text = forms.CharField(label="Text", widget=forms.Textarea)

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
    """ Create New Encyclopedia Entries. Enter a title for the page and content in the form of Markdown."""
    
    # User submited an entry most process data
    if request.method == "POST":

        # Create Form instance containg data from the request
        form = NewEntryForm(request.POST)

        # Check Validity of data
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            
            title = title.upper()

            # Check if entry exist by title
            entry = util.get_entry(title)

            print(title)

            # Entry exists
            if entry:
                return render(request, "encyclopedia/error.html")
            else:
                # Save new entry
                util.save_entry(title, text)

                # Retrieve the Markdown contents of an Encyclopedia entry by its title, 
                page = util.get_entry(title)
        
                # Convert the Markdown into HTML
                html = markdown2.markdown(page)

                # Redirect to new entry page
                return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": html
                })

    # User made a GET request 
    else: 
        # Create Blank Form
        form = NewEntryForm()

        return render(request, "encyclopedia/new.html", {
                "form": form
            })