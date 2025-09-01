from rest_framework import serializers
from .models import Receipt, PlaceInfo, ReceiptImage

class ReceiptImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiptImage
        fields = ["id", "image_url", "uploaded_at"]


class ReceiptSerializer(serializers.ModelSerializer):
    images = ReceiptImageSerializer(many=True, read_only=True)
    # accept both ISO (YYYY-MM-DD) and dotted (MM.DD.YYYY)

    class Meta:
        model = Receipt
        fields = [
            "id",
            "date",
            "price",
            "restaurant_name",
            "address",
            "created_at",
            "images",
        ]
        read_only_fields = ["id", "created_at", "images"]


class PlaceInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceInfo
        fields = ("place_id", "name", "address", "types", "cuisine", "rating", "raw")
