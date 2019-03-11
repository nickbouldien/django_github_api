from django.shortcuts import render
from django.http import (
    HttpResponse,
    JsonResponse,
    HttpResponseNotAllowed,
    HttpResponseServerError,
)
from .models import User
import requests
import json

def index(request):
    routes = {
        "/api/": "'help' - shows available routes",
        "/api/ping": "test availability",
        "/api/user/<github_username>/": "get github data for a given user",
        "/api/user<github_username>/repos": "get github repo data for a given user"
    }
    return JsonResponse(routes)

def test(request):
    return HttpResponse("pong")

# github api # https://developer.github.com/v3/
def user_repos(request, username = "nickbouldien"):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    url = 'https://api.github.com/users/' + username + '/repos'
    headers = {'Accept': 'application/vnd.github.v3+json'}
    r = requests.get(url, headers = headers)
    print(r.status_code)

    return JsonResponse(r.json(), safe=False)

def user(request, username = "nickbouldien"):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    save_param = request.GET.get('save', False)
    json_param = request.GET.get('json', False)

    save_data = save_param == "true" or save_param == "1"
    render_json = json_param == "true" or json_param == "1"

    url = 'https://api.github.com/users/' + username

    headers = {'Accept': 'application/vnd.github.v3+json'}
    r = requests.get(url, headers = headers)
    print(r.status_code)

    json_data = r.json()
    user_data = {}

    if r.status_code == requests.codes.ok:
        user_data['avatar_url'] = json_data.get('avatar_url', "")
        user_data['blog'] = json_dataget('blog', "")
        user_data['bio'] = json_data.get('bio', "")
        user_data['company'] = json_data.get('company', "")
        user_data['location'] = json_data.get('location', "")
        user_data['login'] = json_data.get('login', "")
        user_data['followers'] = json_data.get('followers', 0)
        user_data['following'] = json_data.get('following', 0)
        user_data['name'] = json_data.get('name', "")
        user_data['public_gists'] = json_data.get('public_gists', 0)
        user_data['public_repos'] = json_data.get('public_repos', 0)
        user_data['url'] = json_data.get('url', "")
        user_data['account_created_at'] = json_data.get('created_at')
        user_data['account_updated_at'] = json_data.get('updated_at')
    else:
        return HttpResponseServerError("There was an error with the response from the github api.")

    user = {'user': user_data}

    if render_json:
        return JsonResponse(user)
    
    return render(request, 'gh_api/user.html', user)
