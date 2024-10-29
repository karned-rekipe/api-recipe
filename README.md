# api-recipe

## Description
Simple API to manage recipes.

## Requirements
Install requirements:
```bash
pip install -r requirements.txt
```

## Docs
Visit [url]/docs to see the API documentation.

## References
https://fastapi.tiangolo.com/fr/tutorial/first-steps/

## lancer un MongoDB en local
```sh 
docker run -d --name mongodb-api-recipe -p 27017:27017 -v ./_mongo_data:/data/db mongo
```