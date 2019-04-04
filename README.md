# django_github_api

a super basic django app that I can hit that will save a user's github repo details (created for my blog site which is currently WIP)

### example request

`curl https://django-github-api.herokuapp.com/api/user/nickbouldien?json=1&save=1`

### endpoints

below are the available endpoints (all of the below _only_ accept GET requests)

- `/api/`
- `/api/user/<username>`
- `/api/user/<username>/repos`
- `/api/user/<username>/trends`
- `/api/user/<username>/stats`

### query params

there are two available query params you can add to the request url

- `json=1` or `?json=true` to return json (all endpoints)
- `?save=1` or `?save=true` to save the query (only the `/api/user/<username>` endpoint. this will save the data received from the github api into the database)
