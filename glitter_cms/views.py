from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'glitter_cms/index.html')
