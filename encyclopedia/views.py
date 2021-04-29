from django.shortcuts import render
from django.shortcuts import redirect
from . import util
import markdown2
import random


def index(request):

    if request.method == "POST":
        name = request.POST.get("name")
        entry = util.get_entry(name)
        
        if entry is None:
            entries = util.list_entries()
            results = [entry for entry in entries if (name.lower() in entry.lower())]
            return render(request, "encyclopedia/results.html", {
                "entries": results,
            })

        return redirect('entry', name)
    else:
        randomCheck = request.GET.get('q', '')

        if randomCheck == '':
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries()
            })            

        else:
            entries = util.list_entries()
            numberPage = len(entries)
            pageIndex = random.randint(3, numberPage) - 1

            name = entries[pageIndex]
            return redirect('entry', name)

def entry(request, name):
    entry = util.get_entry(name)

    if entry is None:
        return render(request, "encyclopedia/error.html")

    entry_html = markdown2.markdown(entry)
    title = entry_html.split("\n")[0].replace("<h1>", "").replace("</h1>", "")

    return render(request, "encyclopedia/entry.html", {
        "entries": util.list_entries(),
        "content": entry_html,
        "title": title,
        "name": name
    })

def new(request):

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        entry = util.get_entry(title)
     
        if entry is not None:
            return render(request, "encyclopedia/new.html", {
                "message": 'Page already exists'
            })

        else:
            util.save_entry(title, content)
            return redirect('entry', title)
        
    else:
        return render(request, "encyclopedia/new.html")

def edit(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        
        util.save_entry(title, content)
        return redirect('entry', title)

    else:
        name = request.GET.get('q', '')
        entry = util.get_entry(name)

        if entry is None:
            return render(request, "encyclopedia/error.html")

        entry_html = markdown2.markdown(entry)
        title = entry_html.split("\n")[0].replace("<h1>", "").replace("</h1>", "")

        return render(request, "encyclopedia/edit.html", {
            "content": entry,
            "title": title, 
            "name": name
        })

def error(request, name):
    return render(request, "encyclopedia/error.html")