from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
import requests

def index(request):
    routes = {
        "/api/": "'help' - shows available routes",
        "/api/ping": "est availability",
        "/api/user/<github_username>/": "get github data for a given user",
        "/api/user<github_username>/repos": "get github repo data for a given user"
    }
    return JsonResponse(routes)

def test(request):
    return HttpResponse("pong")

# github api # https://developer.github.com/v3/

def user_repos(request, username):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    url = 'https://api.github.com/users/' + username + '/repos'
    r = requests.get(url)
    print(r.status_code)

    return JsonResponse(r.json(), safe=False)

def user(request, username = "nickbouldien"):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    save_param = request.GET.get('save', False)
    json_param = request.GET.get('json', False)

    save_data = True if save_param == "true" or save_param == "1" else False
    render_json = True if json_param == "true" or json_param == "1" else False

    url = 'https://api.github.com/users/' + username
    r = requests.get(url)
    print(r.status_code)

    return JsonResponse(r.json())
