FROM python:3.12-slim

ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
ENV PORT 8000
ENV WORKERS 1

ENV API_NAME api-recipe
ENV API_TAG_NAME recipes

WORKDIR $APP_HOME
COPY . ./
EXPOSE $PORT

RUN pip install --no-cache-dir -r requirements.txt

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT} --workers ${WORKERS}"]
