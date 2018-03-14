from django.shortcuts import render


# Create your views here.
def search_page(request):
    return render(request, 'glitter_cms/search/search.html')
