from django.shortcuts import render

def post_list(request):
    return render(request, 'yourblog/post_list.html', {})
