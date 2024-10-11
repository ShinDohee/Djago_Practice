from django.http import HttpResponse

def index(request):
    return HttpResponse("heelo, wolrld!")

def some_url(request):
    return HttpResponse("some url 구현함")