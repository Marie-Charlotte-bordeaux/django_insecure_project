# extrait_settings.py
# Lignes ajoutées ou modifiées dans settings.py pour sécuriser le projet
# CF ===> tp_secu_django_py_mcbordeaux pour les explications
# extrait_settings.py
# Lignes ajoutées ou modifiées dans settings.py pour sécuriser le projet
# CF ===> tp_secu_django_py_mcbordeaux pour les explications
# =====================================================================

import os
#===Configuration DEV/PROD===
# -------------------------------------------------------------------
# Clé secrète sécurisée (chargée depuis le .env)
SECRET_KEY = env('SECRET_KEY')

# -------------------------------------------------------------------
# Activation du mode sécurisé (prod/dev)
# Variable pour activer le mode sécurisé en prod
DJANGO_SECURE = os.getenv('DJANGO_SECURE', 'False').lower() == 'true'
# En production DEBUG doit être False pour ne pas exposer d’infos sensibles
DEBUG = not DJANGO_SECURE

# -------------------------------------------------------------------
# Hôtes autorisés
# Liste des hôtes autorisés (protège contre les attaques Host header)
ALLOWED_HOSTS = ['127.0.0.1', 'localhost' ]



#=== SECURITE DES COOKIES ===
# -------------------------------------------------------------------
# Cookies sécurisés

# Cookies envoyés uniquement via HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# Cookies inaccessibles au JavaScript (protège contre le vol)
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
# Restreint l’usage des cookies aux mêmes sites (protège contre CSRF)
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'

# === HTTPS et HSTS ===
# Redirections & HSTS
# Force toutes les requêtes en HTTPS
SECURE_SSL_REDIRECT = True
# Active HSTS : le navigateur impose HTTPS pour 1 an
SECURE_HSTS_SECONDS = 31536000 if DJANGO_SECURE else 0
# Applique HSTS aussi aux sous-domaines
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# Indique aux navigateurs de précharger HSTS
SECURE_HSTS_PRELOAD = True


# -------------------------------------------------------------------
# Origines de confiance pour CSRF
# Liste des domaines de confiance pour le CSRF (doit être en HTTPS en prod)
CSRF_TRUSTED_ORIGINS = [
    'https://127.0.0.1:8000',
    'https://localhost:8000',
    'https://example.com',
]

#=== Headers de sécurité ===
# -------------------------------------------------------------------
# Headers de sécurité
# Empêche l'interprétation incorrecte du type MIME
SECURE_CONTENT_TYPE_NOSNIFF = True
# Politique stricte sur le Referer (protège la vie privée et les tokens CSRF)
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
# Interdit l'affichage du site dans une iframe (protège contre le clickjacking)
X_FRAME_OPTIONS = 'DENY'

#=== CSP ===
# -------------------------------------------------------------------
# Content Security Policy (via django-csp)
# N’autorise que les ressources locales (empêche l’exécution de scripts externes)
CSP_DEFAULT_SRC = ("'self'",)
# Autorise uniquement images locales et data URI
CSP_IMG_SRC = ("'self'", "data:")
# Autorise uniquement scripts locaux
CSP_SCRIPT_SRC = ("'self'",)
# Autorise uniquement feuilles de style locales
CSP_STYLE_SRC = ("'self'",)
