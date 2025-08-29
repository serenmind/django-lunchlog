from django.conf import settings
from django.db import models


class Receipt(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receipts"
    )
    date = models.DateField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    restaurant_name = models.CharField(max_length=255)
    address = models.CharField(max_length=512)
    image = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.restaurant_name} - {self.date} - {self.user.username}"


class PlaceInfo(models.Model):
    place_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=512, blank=True)
    types = models.JSONField(default=list, blank=True)
    cuisine = models.CharField(max_length=255, blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    raw = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
