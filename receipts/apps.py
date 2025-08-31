from django.apps import AppConfig


class ReceiptsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'receipts'

    def ready(self):
        # import signals to register them
        try:
            from . import signals  # noqa: F401
        except Exception:
            # avoid breaking startup if signals can't be imported during migrations
            pass
