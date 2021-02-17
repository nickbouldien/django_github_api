from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseServerError
from django.views.decorators.http import require_GET
import requests
from .models import User
from .utils.math_utils import safe_div

# TODO - GET /users/:username/starred


@require_GET
def index(request):
    json_param = request.GET.get("json", False)
    render_json = json_param == "true" or json_param == "1"

    routes = {
        "/": "'help' - shows available routes",
        "/user/<github_username>/": "get github data for a given user",
        "/user/<github_username>/repos": "get github repo data for a given user",
        "/user/<github_username>/stats": "get github stats for a given user",
        "/user/<github_username>/trends": "get github repo trends for a given user",
    }
    if render_json:
        return JsonResponse({"routes": routes})

    return render(request, "gh_api/index.html", {"routes": routes})


# github api # https://developer.github.com/v3/
@require_GET
def user(request: WSGIRequest, username: str):
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

    if save_data:
        created_user = User.objects.create(**user_data)
        print("created_user: ", created_user)

    if render_json:
        return JsonResponse({"user": user_data})

    return render(request, "gh_api/user.html", {"user": user_data})


@require_GET
def user_repos(request, username):
    json_param = request.GET.get("json", False)
    render_json = json_param == "true" or json_param == "1"

    url = "https://api.github.com/users/" + username + "/repos"
    headers = {"Accept": "application/vnd.github.v3+json"}
    r = requests.get(url, headers=headers)

    repos = []

    if r.status_code == requests.codes.ok:
        for repo in r.json():
            repo_obj = dict(
                id=repo["id"],
                name=repo["name"],
                archived=repo["archived"],
                description=repo["description"],
                forks=repo["forks"],
                forks_count=repo["forks_count"],
                html_url=repo["html_url"],
                open_issues=repo["open_issues"],
                open_issues_count=repo["open_issues_count"],
                owner=repo["owner"],
                stargazers_count=repo["stargazers_count"],
                watchers=repo["watchers"],
                watchers_count=repo["watchers_count"],
            )
            repos.append(repo_obj)
    else:
        return HttpResponseServerError(
            "There was an error with the response from the github api."
        )

    if render_json:
        return JsonResponse({"repos": repos})

    return render(request, "gh_api/repos.html", {"repos": repos})


@require_GET
def user_stats(request, username):
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
        return JsonResponse({"user_data": user_data})

    return render(request, "gh_api/stats.html", {"user_data": user_data})


@require_GET
def user_trends(request, username):
    json_param = request.GET.get("json", False)
    amount_param = request.GET.get("amount", 30)  # defaulting to 30 for a month

    render_json = json_param == "true" or json_param == "1"

    user_data = []

    user_entries = User.objects.filter(login=username).order_by("-id")[
        : int(amount_param)
    ]
    for entry in user_entries:
        user_obj = dict(
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
        user_data.append(user_obj)

    if render_json:
        return JsonResponse({"user_data": user_data})

    return render(request, "gh_api/trends.html", {"user_data": user_data})
