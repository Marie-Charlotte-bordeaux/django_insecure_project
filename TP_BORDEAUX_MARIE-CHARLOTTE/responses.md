
# TP : Durcir un projet Django  
**Auteur :** BORDEAUX Marie-Charlotte

---

## Etape 1 : Création du projet de test
- ✔️ ok

---

## Etape 2 : Page web de test
- Création de la page `home` + CSS + URL afin d'afficher un template basique à l'écran  
- ✔️ ok

---

## Etape 3 : Diagnostic de sécurité initial
Identifier les problèmes de sécurité actuels du projet.  

Après avoir lancé la commande :  
```bash
python manage.py check --deploy > baseline.txt 2>&1


* Cela génère un fichier `baseline.txt` pour visualiser les avertissements/erreurs de sécurité détectés par Django.
* Cette étape permet de durcir l'application en repérant les failles de sécurité.
```
### Résultats : 6 WARNINGS

* `(security.W004)`, `(security.W008)`, `(security.W009)`, `(security.W012)`, `(security.W016)`, `(security.W018)`

#### Exemples :

* `(security.W018)` You should not have DEBUG set to True in deployment.

  * `DEBUG=True` → Django tourne en mode debug.
  * En production, il faudra `DEBUG=False`.

* `(security.W018)` SESSION\_COOKIE\_SECURE non activé

  * Les cookies de session ne sont pas marqués “Secure”.
  * Correction : `SESSION_COOKIE_SECURE = True` (en prod).

* `(security.W009)` SECRET\_KEY faible

  * Django a généré une clé par défaut : `django-insecure-xxxx`.
  * Il faut remplacer la clé par une valeur longue et aléatoire, stockée dans `.env`.

---

## Etape 4 : Configuration DEV/PROD

Dans `settings.py` :

```python
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# Variable pour activer le mode sécurisé
DJANGO_SECURE = os.getenv('DJANGO_SECURE', 'False').lower() == 'true'

# En production, DEBUG doit être FALSE
DEBUG = not DJANGO_SECURE
# DEBUG = env('DEBUG')

# Domaines autorisés
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
# ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['127.0.0.1', 'localhost'])

# Pour HTTPS local sur port 8443
CSRF_TRUSTED_ORIGGINS = [
    'https://127.0.0.1',
    'http://localhost',
    'http://localhost:8443',
]
```

* `DEBUG` doit être à `FALSE` en production pour protéger les données sensibles.
* Il est recommandé de stocker ce paramètre dans `.env`.

---

## Etape 5 : Sécurisation des cookies

Protéger les cookies contre le vol et les attaques.

```python
# Redirige tout le trafic vers HTTPS
SECURE_SSL_REDIRECT = True

# Cookies uniquement via HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Cookies non accessibles par JavaScript côté client
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# Protection contre les requêtes intersites
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'
```

---

## Etape 6 : HTTPS et HSTS

Forcer l'utilisation d'HTTPS et activer HSTS (HTTP Strict Transport Security).
Documentation : [Django HSTS Middleware](https://docs.djangoproject.com/en/5.2/ref/middleware/#http-strict-transport-security)

```python
# Redirections & HSTS (uniquement en prod derrière HTTPS)
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000 if True else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

* HSTS informe le navigateur que toutes les futures connexions doivent utiliser HTTPS.
* Associé à la redirection HTTP→HTTPS, cela renforce la sécurité SSL.

---

## Etape 7 : Headers de sécurité

Ajouter des headers HTTP pour protéger contre diverses attaques.

### ClickJacking

* Attaque où un site malveillant incite l'utilisateur à cliquer sur un élément caché d'un autre site (iframe).

### X-Frame-Options

* `SAMEORIGIN` → seulement le même site peut charger la ressource.

* `DENY` → aucun site ne peut charger la ressource.

* Django propose de définir ce header via :

  1. Middleware global
  2. Décorateurs de vue spécifiques

---

## Etape 8 : Content Security Policy (CSP)

Implémenter une CSP pour bloquer l'exécution de code malveillant.

* Exemple d’erreur navigateur :

```
Refused to execute inline script because it violates the following Content Security Policy directive: "script-src 'self'".
```

* Les tests CSP (ex. `alert('Test XSS')`) ne s’exécutent pas, comportement attendu.

---

## Etape 9 : Validation des configurations

* Vérifier que toutes les protections sont actives.

Exemple `after.txt` :

```
System check identified no issues (0 silenced).
```

Exemple `header_after.txt` :

```
HTTP/1.1 301 Moved Permanently
Date: Tue, 26 Aug 2025 13:53:07 GMT
Server: WSGIServer/0.2 CPython/3.13.4
Content-Type: text/html; charset=utf-8
Location: https://127.0.0.1:8000/
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Cross-Origin-Opener-Policy: same-origin
Content-Security-Policy: style-src 'self'; default-src 'self'; img-src 'self' data:; script-src 'self'
```

* Remarque : HSTS n’apparaît pas en HTTP, uniquement en HTTPS.

---

## Etape 10 : Documentation de vos changements

* Documenter toutes les modifications effectuées pour sécuriser le projet.

---

