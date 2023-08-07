from django.shortcuts import render
from django.http import HttpResponse
from .models import Advertisements81

def index(request):
    advertisements = Advertisements81.objects.all()
    context = {'advertisements':advertisements}
    return render(request, 'index.html', context)

def top_sellers(request):
    return render(request, 'top-sellers.html')