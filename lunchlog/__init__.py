"""lunchlog package initialiser.

Expose the Celery app as ``celery_app`` so `celery -A lunchlog worker` can discover it.
"""

from .celery import app as celery_app  # noqa

__all__ = ("celery_app",)
