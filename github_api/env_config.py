import os

ENVIRONMENT = os.getenv("ENVIRONMENT")

IS_PROD = ENVIRONMENT == "production" or ENVIRONMENT == "prod"

# setup local (non-secret env vars)
SECRET = os.getenv("LOCAL_SECRET")
DATABASE_NAME = os.getenv("LOCAL_DATABASE_NAME")
DATABASE_PASSWORD = os.getenv("LOCAL_DB_PW")
DATABASE_USER = os.getenv("LOCAL_DB_USER")

# override for prod
if IS_PROD:
    SECRET = os.getenv("SECRET")
    DATABASE_NAME = os.getenv("DATABASE_NAME")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
    DATABASE_USER = os.getenv("DATABASE_USER")
