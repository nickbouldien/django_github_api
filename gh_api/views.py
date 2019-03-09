from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def test(request):
    return HttpResponse("pong")


# github api # https://developer.github.com/v3/

def user_repos(request, username):
    url = 'https://api.github.com/users/' + username + '/repos'
    r = requests.get(url)
    print(r.status_code)

    return JsonResponse(r.json(), safe=False)

def user(request, username):
    url = 'https://api.github.com/users/' + username
    r = requests.get(url)
    print(r.status_code)

    return JsonResponse(r.json())
