from django.db import models

class User(models.Model):
    avatar_url = models.CharField(max_length = 50)
    blog = models.CharField(max_length = 50)
    bio = models.TextField(max_length = 200)
    company = models.CharField(max_length = 50)
    location = models.CharField(max_length = 50)
    login = models.CharField(max_length = 50)
    followers = models.IntegerField(default = 0)
    following = models.IntegerField(default = 0)
    name = models.CharField(max_length = 50)
    public_gists = models.IntegerField(default = 0)
    public_repos = models.IntegerField(default = 0)
    url = models.CharField(max_length = 50)
    account_created_at = models.DateTimeField()
    account_updated_at = models.DateTimeField()

    def __repr__(self):
        return "User('{}', '{}', '{}')".format(self.login, self.name, self.url)

    def __str__(self):
        return "'{}' - '{}'".format(self.login, self.name)
