import os
from typing import Optional

ENVIRONMENT: Optional[str] = os.getenv("ENVIRONMENT")

IS_PROD: bool = ENVIRONMENT == "production" or ENVIRONMENT == "prod"

# setup local (non-secret env vars)
SECRET: Optional[str] = os.getenv("LOCAL_SECRET")
DATABASE_NAME: Optional[str] = os.getenv("LOCAL_DATABASE_NAME")


# override for prod
if IS_PROD:
    SECRET = os.getenv("SECRET")
    DATABASE_NAME = os.environ.get("DATABASE_URL")
