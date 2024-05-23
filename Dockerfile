FROM python:3.11-slim

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

ENV PORT 8002

RUN pip install --no-cache-dir -r requirements.txt

ENV PBL_JWKS_REMOTE_URI=https://api.pebble.solutions/keys/jwks.json

# As an example here we're running the web service with one worker on uvicorn.
CMD exec uvicorn recipe.main:app --host 0.0.0.0 --port ${PORT} --workers 1
