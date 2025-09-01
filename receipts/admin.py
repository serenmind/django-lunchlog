from django.contrib import admin
from .models import Receipt, PlaceInfo, ReceiptImage


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ("user", "restaurant_name", "date", "price")


@admin.register(PlaceInfo)
class PlaceInfoAdmin(admin.ModelAdmin):
    list_display = ("name", "place_id", "rating")


@admin.register(ReceiptImage)
class ReceiptImageAdmin(admin.ModelAdmin):
    list_display = ("receipt", "image_url", "image")