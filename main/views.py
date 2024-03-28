from django.shortcuts import render
from django.http import HttpResponse
from .models import Director, Administrator, Performer
from .forms import CreateNewAccount

# Create your views here.
def index(response):
    return render(response, 'main/index.html', {})   

def login(response):
    return render(response, 'main/login.html', {})

def signup(response):  
    return render(response, 'main/signup.html', {})                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
