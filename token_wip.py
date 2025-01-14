import jwt
import requests
from jwt.algorithms import Algorithm  # Use the general Algorithm class

# Token à vérifier
token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJQOVpLWnkyX2M3Sjh1aTJBcXRnTGk2NTNOTWVQcDBYbjg4Q1pHNjRjLVlnIn0.eyJleHAiOjE3MzY4NTYyNDAsImlhdCI6MTczNjg1NDc0MCwianRpIjoiYmJmM2Y3YzktY2EzYy00MzQ2LWIzYmQtZGIzOGZiY2Q3NjEyIiwiaXNzIjoiaHR0cHM6Ly9pYW0ua2FybmVkLmJ6aC9yZWFsbXMvS2FybmVkIiwiYXVkIjpbImthcm5lZCIsImFjY291bnQiLCJhcGktcmVjaXBlIl0sInN1YiI6ImQzZjQ4YTQyLTBkMWUtNDI3MC04ZThlLTU0OTI1MWNkODIzZCIsInR5cCI6IkJlYXJlciIsImF6cCI6Imthcm5lZCIsInNpZCI6ImJhYTliN2JhLWE0ZTgtNGU1Yi04ZDQyLTVlMTc5MjdmMzE5OCIsImFjciI6IjEiLCJhbGxvd2VkLW9yaWdpbnMiOlsiaHR0cDovL2xvY2FsaG9zdDo4NTAxIiwiaHR0cDovL2xvY2FsaG9zdDo4MDAwIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIiwiZGVmYXVsdC1yb2xlcy1rYXJuZWQiXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJkZWxldGUtYWNjb3VudCIsInZpZXctcHJvZmlsZSJdfSwiYXBpLXJlY2lwZSI6eyJyb2xlcyI6WyJyZWFkIiwidXBkYXRlIiwiY3JlYXRlIiwiZGVsZXRlIl19fSwic2NvcGUiOiJwcm9maWxlIGVtYWlsIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsIm5hbWUiOiJLaWxsaWFuIEtPUFAiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJraWxsaWFuIiwiZ2l2ZW5fbmFtZSI6IktpbGxpYW4iLCJmYW1pbHlfbmFtZSI6IktPUFAiLCJlbWFpbCI6ImtpbGxpYW5rb3BwQGdtYWlsLmNvbSJ9.aWr5p-3EMOsju84qhaYN0AwNSBMMFWedvWHc6dvIQ71QyvfG1Eag5SjbvfJqOqLuYZJCZ_TBdJNMVMV7rVk9L0tJRiFpVM4prWb_vJ4GxpoxhOYgF22kzzjlQDHsfPsdTCmV9V6-EXgnYo1aPWXgFOu6sdYEk8NOzJtNaBtt4ghyR8JoYUeSX1D8E4G-IZx-fGr50Hyki0YSKUuGZvH_m7i3w99TofnXEYfgOq3t3I2MRAFLAU8eH1oRJ3PvmQlgXckxRiehHS6TacMcMNUzUqlK3uTcrVFNt0i5oSGc127Y-rg0Wx_OzDcbpUBhzGV9I1Z5GdCVxpSy6tQIGHPwBw"

jwks_url = "https://iam.karned.bzh/realms/Karned/protocol/openid-connect/certs"

# Récupération des clés publiques
response = requests.get(jwks_url)
if response.status_code == 200:
    jwks = response.json()
else:
    print("Erreur lors de la récupération des clés publiques :", response.text)
    exit()

print("JWKS keys:", jwks['keys'])

# Extraction du 'kid' depuis le header du token
try:
    headers = jwt.get_unverified_header(token)
    kid = headers.get("kid")
    if not kid:
        print("Le token n'a pas de 'kid' dans le header.")
        exit()
except jwt.DecodeError:
    print("Impossible de décoder le header du token.")
    exit()

# Recherche de la clé correspondante
public_key = None
for key in jwks['keys']:
    if key['kid'] == kid:
        public_key = Algorithm.from_jwk(key)
        break

print(jwks['keys'])

if not public_key:
    print(f"Aucune clé correspondante trouvée pour le 'kid' : {kid}")
    exit()

# Vérification du token
try:
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=["RS256"],
        audience="karned",  # Doit correspondre à la valeur de l'audience attendue
        issuer="https://iam.karned.bzh/realms/Karned"  # Doit correspondre à l'émetteur
    )
    print("Le token est valide. Payload :", decoded)
except jwt.ExpiredSignatureError:
    print("Le token a expiré.")
except jwt.InvalidTokenError as e:
    print(f"Le token est invalide : {e}")