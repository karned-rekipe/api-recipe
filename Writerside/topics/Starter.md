# Starter

## Base de données

L'API des ingrédients nécessite une base de données MongoDB. 
Pour simplifier le développement, il est possible de lancer une instance de MongoDB en local avec Docker.
Nous partons du principe que Docker est installé sur votre machine.
Pour lancer une instance de MongoDB en local, il suffit de lancer les commandes suivantes :

**Télécharger l'image de MongoDB**
```shell
docker pull mongo
```

**Lancer une instance de MongoDB**
```shell
docker run -d -p 27017:27017 --name mongodb mongo
```

Le port 27017 est le port par défaut. Une redirection de port est faite pour que vous puisiez vous connecter avec MongoDB Compass. 
Pour télécharger l'app : [https://www.mongodb.com/products/tools/compass](https://www.mongodb.com/products/tools/compass)  
Pour vous connecter, il faudra utiliser l'adresse suivante : `mongodb://localhost:27017`

Un jeu de données est disponible dans le repo dataset. [https://github.com/karned-rekipe/dataset/blob/main/databases/recipe/recipe_final.csv](https://github.com/karned-rekipe/dataset/blob/main/databases/recipe/recipe_final.csv)
Il est posssible de l'importer dans la base de données avec Compass.

## API 
A la racine du projet se trouve un Dockerfile qui permet de lancer l'API en local.

**Création de l'image Docker de l'API**
```shell
docker build -t rekipe-api-recipe .
```

**Lancement de l'API**
```shell
docker run -d --name rekipe-api-recipe -p 8002:8002 rekipe-api-recipe
```

Le port 8002 a été choisi pour éviter les conflits avec d'autres services, il est arbitraire et peut être changé.
Se rendre sur son naviguateur à l'adresse [http://localhost:8002/recipe/docs](http://localhost:8002/recipe/docs) pour voir la documentation de l'API.