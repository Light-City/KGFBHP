from django.shortcuts import render
import sys
from kgqa.KB_query import query_main

# Create your views here.

def search_post(request):
    return render(request, "post_from_base.html")

def content_post(request):
    ctx = {}
    if request.POST:
        question = request.POST['q']
        ctx['rlt'] = query_main.query_function(question)
        print(ctx['rlt'])
        ctx['q']=question
        print(ctx['q'])
    return render(request, "con_from_base.html", ctx)

def temp_post(request):
    return render(request, "temp_from_base.html")
