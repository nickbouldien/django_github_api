from django.core.serializers import serialize
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
from .utils.math_utils import safe_div


def index(request):
    routes = {
        "/api/": "'help' - shows available routes",
        "/api/ping": "test availability",
        "/api/user/<github_username>/": "get github data for a given user",
        "/api/user<github_username>/repos": "get github repo data for a given user",
        "/api/user<github_username>/trends": "get github repo trends for a given user",
    }
    return JsonResponse(routes)


def test(request):
    return HttpResponse("pong")


# github api # https://developer.github.com/v3/
def user_repos(request, username):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    url = "https://api.github.com/users/" + username + "/repos"
    headers = {"Accept": "application/vnd.github.v3+json"}
    r = requests.get(url, headers=headers)

    return JsonResponse(r.json(), safe=False)


def user(request, username):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    save_param = request.GET.get("save", False)
    json_param = request.GET.get("json", False)

    save_data = save_param == "true" or save_param == "1"
    render_json = json_param == "true" or json_param == "1"

    url = "https://api.github.com/users/" + username

    headers = {"Accept": "application/vnd.github.v3+json"}
    r = requests.get(url, headers=headers)

    json_data = r.json()
    user_data = {}

    if r.status_code == requests.codes.ok:
        user_data["avatar_url"] = json_data.get("avatar_url", "")
        user_data["blog"] = json_data.get("blog", "")
        user_data["bio"] = json_data.get("bio", "")
        user_data["company"] = json_data.get("company", "")
        user_data["location"] = json_data.get("location", "")
        user_data["login"] = json_data.get("login", "")
        user_data["followers"] = json_data.get("followers", 0)
        user_data["following"] = json_data.get("following", 0)
        user_data["name"] = json_data.get("name", "")
        user_data["public_gists"] = json_data.get("public_gists", 0)
        user_data["public_repos"] = json_data.get("public_repos", 0)
        user_data["api_url"] = json_data.get("url", "")
        user_data["html_url"] = json_data.get("html_url", "")
        user_data["account_created_at"] = json_data.get("created_at")
        user_data["account_updated_at"] = json_data.get("updated_at")
    else:
        return HttpResponseServerError(
            "There was an error with the response from the github api."
        )

    user = {"user": user_data}

    if save_data:
        created_user = User.objects.create(**user_data)
        print("created_user: ", created_user)

    if render_json:
        return JsonResponse(user)

    return render(request, "gh_api/user.html", user)


def user_stats(request, username):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    json_param = request.GET.get("json", False)
    render_json = json_param == "true" or json_param == "1"

    amount_param = request.GET.get("amount", 30)  # defaulting to 30 for a month
    user_entries = User.objects.filter(login=username)[: int(amount_param)]

    followers = 0
    following = 0
    public_gists = 0
    public_repos = 0

    amount = len(user_entries)

    for entry in user_entries:
        followers += entry.followers
        following += entry.following
        public_gists += entry.public_gists
        public_repos += entry.public_repos

    user_data = {
        "login": username,
        "followers": safe_div(followers, amount),
        "following": safe_div(following, amount),
        "public_gists": safe_div(public_gists, amount),
        "public_repos": safe_div(public_repos, amount),
    }

    if render_json:
        return JsonResponse(user_data)

    return render(request, "gh_api/stats.html", user_data)


def user_trends(request, username):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    json_param = request.GET.get("json", False)
    amount_param = request.GET.get("amount", 30)  # defaulting to 30 for a month

    render_json = json_param == "true" or json_param == "1"

    json_res = []

    user_entries = User.objects.filter(login=username).order_by("-id")[
        : int(amount_param)
    ]
    for entry in user_entries:
        json_obj = dict(
            id=entry.id,
            company=entry.company,
            location=entry.location,
            login=entry.login,
            followers=entry.followers,
            following=entry.following,
            public_gists=entry.public_gists,
            public_repos=entry.public_repos,
            created_date=entry.created_date,
            account_updated_at=entry.account_updated_at,
        )
        json_res.append(json_obj)

    if render_json:
        return JsonResponse(json_res, safe=False)

    return render(request, "gh_api/trends.html", {"user_data": json_res})
