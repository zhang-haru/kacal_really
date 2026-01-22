from django.apps import AppConfig

class TestappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "testApp"

    def ready(self):
        from . import signals  # noqa: f401
