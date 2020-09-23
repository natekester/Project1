from django.shortcuts import render,redirect
import markdown2
from . import util
from django import forms
from django.urls import reverse
import numpy as np
from pathlib import Path
from django.http import *

class NewEntryForm(forms.Form):
    entry_name = forms.CharField(label="New Page Name", max_length=100)
    text = forms.CharField(label="Description", max_length=100)

class SearchForm(forms.Form):
    search_field = forms.CharField(label="search", max_length=100)

def index(request):
    
    Search_form = SearchForm()
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_form": Search_form
    })

def search_redirect(request):
    print("starting redirect")
    if request.method == "POST" :
        search = request.POST.get("search_field")
        print(search)
    

        
        return redirect(f"search/{search}")
    else:
        search_form = SearchForm()
        return render(request, "encyclopedia/search.html", {
            
            "search_form": search_form
        })


    #redirect to /seach/{searched}

def search(request, search):
    #find the seach criteria stuff.
    
    search_form = SearchForm()
    all_entries = util.list_entries()
    all_entries = np.asarray(all_entries)
    print("perm resp redi")
    print(HttpResponsePermanentRedirect(''))
    if search.upper() in (page.upper() for page in all_entries):
        return redirect(f'/wiki/{search}')
    else:
        search_results = []
        for item in all_entries:
            print(item.lower)
            if search.lower() in item.lower():
                search_results.append(item)

    
    return render(request, "encyclopedia/search.html", {
        "entries": search_results,
        "search_form": search_form
    })


# def search(request,search):
        
#         return render(request, "encyclopedia/search.html")

def get_entry(request, name):
    if request.method == "POST":
        #alrighty - now let's get the editing moving
        
        
        return redirect(f"/edit/{name}")
        
    else:
        search_form = SearchForm()
        entry = util.get_entry(name)
        if( entry == None):
            entry = f"***Error!*** <br></br> There is no wiki page with the title of *{name}*."
        
        return render(request, "encyclopedia/get_entry.html", {
            "entry_name" : name ,
            "entry" : markdown2.markdown(entry),
            "search_form": search_form
        })

def edit_redirect(request):
    print("starting redirect")
    if request.method == "POST" :
        name = request.POST.get("id")
        print("redirecting to edit: "+ name)
    

        
        return redirect(f"edit/{name}")
    else:
        search_form = SearchForm()
        return render(request, "encyclopedia/index.html", {
            
            "search_form": search_form
        })


def make_entry(request):
     search_form = SearchForm()
     if (request.method == "POST"):

        
        form = NewEntryForm(request.POST)  
                 
        if form.is_valid():


                
            name = form.cleaned_data["entry_name"]
            text = form.cleaned_data["text"]
            

            try:

                open(f'entries/{name}.md',"x").write(f"#{name} \n" + text)
                
                entry = util.get_entry(name)
                return render(request, "encyclopedia/get_entry.html", {"entry_name" : name ,
                    "entry" : markdown2.markdown(entry),
                    "search_form": search_form
                    })

            except FileExistsError:


                return render(request, "encyclopedia/make_entry.html", { "response": "Please input a valid entry, that item has already been created.", 
                "form": form
                , "search_form": search_form
                })     
            



        else:
            return render(request, "encyclopedia/make_entry.html", { "response": "Please input a valid entry", 
            "form": form,
            "search_form": search_form
            })     
     
     else:
         form = NewEntryForm()
         return render(request, "encyclopedia/make_entry.html", { "response": "Please add an entry", 
            "form": form,
            "search_form": search_form
            })     


def random_entry(request):
    name = util.get_random_entry()
    
    return redirect(f"wiki/{name}")

def edit_wiki(request, wiki_name):
    
    if(request.method == "POST"):
        #TODO edit the actual .md file
         print('we just recieved the POST method to edit the page')
         for key, value in request.POST.items():
            print('Key: %s' % (key) ) 
  
            print('Value: %s' % (value) )

         text = str(request.POST.get("Text"))
         print("the text we recovered: "+ str(text))
         
         with open(f'entries/{wiki_name}.md',"w") as filetowrite:
            filetowrite.write(text)
            filetowrite.close()

         
         print(wiki_name + " is the name of the edited wiki before redirect")
         

         return redirect(f'/wiki/{wiki_name}')

    else:
        search_form = SearchForm()
        print(wiki_name + " is the name for this page.")
        text = util.get_entry(wiki_name)

        return render(request, "encyclopedia/edit_wiki.html", {
            "search_form": search_form,
            "wiki_name": wiki_name,
            "text": text
        })