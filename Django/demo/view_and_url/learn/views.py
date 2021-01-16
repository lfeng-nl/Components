from django.shortcuts import render
from datetime import datetime
# Create your views here.

def home(request):
    time = str(datetime.now())[:-7]
    return render(request, 'home.html', {'time':time})

