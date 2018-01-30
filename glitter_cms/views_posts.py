from django.shortcuts import render


# Create your views here.
def view_page(request):
    return render(request, 'glitter_cms/post/view_post.html')
