from django.shortcuts import render
from django.shortcuts import render

def index(request):
    return render(request, "librarycore/index.html")

