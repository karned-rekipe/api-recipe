# README (please)

## How to publish ?
```gcloud builds submit --tag gcr.io/ace-charter-310713/recipe```

## How to deploy ?
```gcloud run deploy recipe --image gcr.io/ace-charter-310713/recipe --platform managed --region=europe-west1 --allow-unauthenticated --cpu-boost```

## How to update revision
```
gcloud run deploy recipe \
--image=gcr.io/ace-charter-310713/recipe \
--region=europe-west1 \
--project=ace-charter-310713 \
 && gcloud run services update-traffic recipe --to-latest
```

Cette solution est transitoire. 

# En local
```
sudo docker build -t rekipe-api-ingredient .
sudo docker run -d --name rekipe-api-ingredient -p 1234:8000 rekipe-api-ingredient
```