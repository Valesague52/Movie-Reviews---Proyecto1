from django.shortcuts import render

def home(request):
    return render(request, 'home.html', {'name': 'Helen Sanabria'})

def about(request):
    return render(request, 'about.html')