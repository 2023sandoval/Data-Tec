from django.shortcuts import render
from django.http import HttpResponseNotFound


def index(request):
    return render(request, 'index.html')

def acerca(request):
    return render(request, 'acerca.html')

def pagina_404(request, exception):
    return HttpResponseNotFound('<h1>Página no encontrada</h1>')