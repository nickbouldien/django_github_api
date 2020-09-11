# django-github-api

A super basic django app that has endpoints that will call the [github rest api](https://docs.github.com/en/rest) 
to get details about a github user or the user's repos. Can also save a github user's github repo details to a database for later retrieval

## endpoints
### all endpoints
below are the available endpoints (all of the below _only_ accept GET requests)

- `/api/` - show available routes
- `/api/user/<username>` - get github data for a given user
- `/api/user/<username>/repos` - get github repo data for a given user
- `/api/user/<username>/stats` - get github repo stats for a given user
- `/api/user/<username>/trends` - get github repo trends for a given user

### query parameters
there are three available query params you can add to the request url (depending on the endpoint)

- `?json=1` to return json (all endpoints)
- `?save=1` to save the query (only the `/api/user/<username>` endpoint. this will save the data received from the github api into the database)
- `?amount=<number>` to return the `<amount>` of records (only on `/api/user/trends` and `/api/user/stats` endpoints). defaults to `30` (~ days in a month)

### example request
`curl https://django-github-api.herokuapp.com/api/user/nickbouldien?json=1`

## setup
### without docker
```bash
python3.7 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

```bash
python manage.py runserver
```

### with docker
```bash
docker build -t web:latest .
```

```bash
docker run --rm --name django-github-api -e "PORT=8080" -e "DEBUG=1" -p 8080:8080 web:latest
```
