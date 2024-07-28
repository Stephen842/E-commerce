from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from datetime import datetime

# Create your views here.

def home(request):
    context = {
            'title': 'Rinx Venture: Your One-Stop Store for Phones, Gadgets & Repairs'
    }
    return render(request, 'pages/home.html', context)
