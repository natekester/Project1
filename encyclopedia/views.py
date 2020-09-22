from django.shortcuts import render
import markdown2
from . import util
from django import forms
from pathlib import Path

class NewEntryForm(forms.Form):
    entry_name = forms.CharField(label="New Page Name", max_length=100)
    text = forms.CharField(label="Description", max_length=100)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def get_entry(request, name):
    entry = util.get_entry(name)
    if( entry == None):
        entry = f"***Error!*** <br></br> There is no wiki page with the title of *{name}*."
    return render(request, "encyclopedia/get_entry.html", {
        "entry_name" : name ,
        "entry" : markdown2.markdown(entry)
    })

def make_entry(request):
     if (request.method == "POST"):

        
        form = NewEntryForm(request.POST)  
        print(form)          
        if form.is_valid():


                
            name = form.cleaned_data["entry_name"]
            text = form.cleaned_data["text"]
            print(name)

            try:

                open(f'entries/{name}.md',"x").write(text)
                #TODO make this redicrect to new page.
                return render(request, "encyclopedia/make_entry.html", { "response": " new entry created.", 
                "form": form
                })
            except FileExistsError:


                return render(request, "encyclopedia/make_entry.html", { "response": "Please input a valid entry, that item has already been created.", 
                "form": form
                })     
            



        else:
            return render(request, "encyclopedia/make_entry.html", { "response": "Please input a valid entry", 
            "form": form
            })     
     
     else:
         form = NewEntryForm()
         return render(request, "encyclopedia/make_entry.html", { "response": "Please add an entry", 
            "form": form
            })     