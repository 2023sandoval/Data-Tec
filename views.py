from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def acerca(request):
    return render(request, 'acerca.html')