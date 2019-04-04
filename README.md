# django_github_api

a super basic django app that has endpoints that will call the github rest api to get details about a github user or the github user's repos. can save a github user's github repo details (created for my blog site which is currently WIP)

### example request

`curl https://django-github-api.herokuapp.com/api/user/nickbouldien?json=1&save=1`

### endpoints

below are the available endpoints (all of the below _only_ accept GET requests)

- `/api/` - show available routes
- `/api/user/<username>` - get github data for a given user
- `/api/user/<username>/repos` - get github repo data for a given user
- `/api/user/<username>/stats` - get github repo stats for a given user
- `/api/user/<username>/trends` - get github repo trends for a given user

### query params

there are three available query params you can add to the request url (depending on the endpoint)

- `?json=1` or `?json=true` to return json (all endpoints)
- `?save=1` or `?save=true` to save the query (only the `/api/user/<username>` endpoint. this will save the data received from the github api into the database)
- `?amount=<number>` to return the `<amount>` of records (only on `/api/user/trends` and `/api/user/stats` endpoints). defaults to `30` (~ days in a month)
