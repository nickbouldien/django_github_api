import os

ENVIRONMENT = os.getenv("ENVIRONMENT")

IS_PROD = ENVIRONMENT == "production" or ENVIRONMENT == "prod"

# setup local (non-secret env vars)
SECRET = os.getenv("LOCAL_SECRET")
DATABASE_NAME = os.getenv("LOCAL_DATABASE_NAME")


# override for prod
if IS_PROD:
    SECRET = os.getenv("SECRET")
    DATABASE_NAME = os.environ.get("DATABASE_URL")
