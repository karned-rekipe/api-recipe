J'ai un user_id Keycloak : d3f48a42-0d1e-4270-8e8e-549251cd823
il va me servir d'id utilisateur partout

Nous vendons des licences 
Un utilisateur ou une entreprise achète donc un ou des licences.
Ces licences sont bornées dans le temps. Elles ont un iat et un exp (sur le principe d'un token)
Une licence est unique et peut être affectée à un utilisateur ou "à affecter"

Un utilisateur possède des licences d'utilisations.

Une licence est donnée pour un service. Un service (produit) liste les accès qu'il autorise.

Ex : service api-recipe pour une licence qui ne donne accès qu'à cela
'api-recipe-admin': {'roles': ['read','update','create','delete']}

Ex : app-recipe-admin pour une licence qui donne accès à toute l'application de cuisine
'api-recipe': {'roles': ['read','update','create','delete']}},
'api-ingredient': {'roles': ['read','update','create','delete']}},
'api-ustensile': {'roles': ['read','update','create','delete']}},
'api-planning': {'roles': ['read','update','create','delete']}}

Si l'utilisateur possède plusieurs licences, il devra en choisir une pour utiliser le service.

Une licence définit les credentials à utiliser.
Les données sont stockés dans des bases de données et bucket.
Les données sont manipulées par les API.
Les credentials peuvent donc être définis de la manière suivante
default : c'est celui utilisé en l'absence de credentials particulier
api-recipe : celui spécifique à API Recipe

Soit les éléments suivants : 
- type = mongodb
- host = 'localhost'
- port = 27017
- db = "local" (optionnel  si non défini)
- collection = "recipes" (optionnel recipes si non défini)

une licence c'est : 
- une période : iat / exp
- un produit
- un user
- des credentials

un mécanisme se charge de modifier keycloak pour le faire correspondre à ce que les licences représentent

il faut un outil de gestion de licence
un outil de gestion utilisateur