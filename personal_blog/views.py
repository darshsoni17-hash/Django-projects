from django.http import HttpResponse
from django.shortcuts import render


def home(request):
   # return HttpResponse("Hello, World. you at the Django project home page")
   return render(request, 'Website/index.html')

def About(request):
    return HttpResponse("Hello, World. you at the Django project About page")

def contact(request):
    return HttpResponse("Hello, World. you at the Django project contact page")    