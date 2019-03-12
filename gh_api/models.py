from django.db import models
from django.utils import timezone


class User(models.Model):
    avatar_url = models.CharField(max_length=100)
    blog = models.CharField(max_length=100)
    bio = models.TextField(max_length=200)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    login = models.CharField(max_length=100)
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    public_gists = models.IntegerField(default=0)
    public_repos = models.IntegerField(default=0)
    api_url = models.CharField(max_length=100)
    html_url = models.CharField(max_length=100, default="")
    account_created_at = models.DateTimeField()
    account_updated_at = models.DateTimeField()
    created_date = models.DateTimeField(default=timezone.now)

    def __repr__(self):
        return "User('{}', '{}', '{}')".format(self.login, self.name, self.html_url)

    def __str__(self):
        return "'{}': '{}' - '{}'".format(self.id, self.login, self.name)
