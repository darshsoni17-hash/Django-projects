from django.shortcuts import render
from .models import chaivarity

# Create your views here.
def all_chai(request):
    chais = chaivarity.objects.all()
    return render(request, 'chai/all_chai.html', {'chais': chais})