from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from .models import Receipt, PlaceInfo, ReceiptImage


User = get_user_model()


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"],
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data.get("username"), password=data.get("password")
        )
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        data["user"] = user
        return data


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
