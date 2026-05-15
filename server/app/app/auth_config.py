from django.contrib.auth.apps import AuthConfig


class BigAuthConfig(AuthConfig):
    default_auto_field = "django.db.models.BigAutoField"
