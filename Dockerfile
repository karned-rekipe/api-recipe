FROM python:3.12-slim

ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
ENV PORT 8000
ENV WORKERS 1

ENV API_NAME api-recipe
ENV API_TAG_NAME recipes

ENV KEYCLOAK_URL https://iam.karned.bzh/realms/Karned/protocol/openid-connect
ENV KEYCLOAK_HOST https://iam.karned.bzh
ENV KEYCLOAK_REALM Karned
ENV KEYCLOAK_CLIENT_ID karned
ENV KEYCLOAK_CLIENT_SECRET chut!

ENV REDIS_HOST redis
ENV REDIS_PORT 6379
ENV REDIS_DB 0
ENV REDIS_PASSWORD chut!

WORKDIR $APP_HOME
COPY . ./
EXPOSE $PORT

RUN pip install --no-cache-dir -r requirements.txt

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT} --workers ${WORKERS}"]
