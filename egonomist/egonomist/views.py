# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

def hello(request):
    return render(request, 'index.html', {})