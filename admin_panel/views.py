from django.shortcuts import render
from admin_panel.models import Blog

# Create your views here.

def index(request):
    model = Blog.objects.all()
    
    context = {
        "model": model
    }
    
    return render(request, 'info/info.html', context)
    
