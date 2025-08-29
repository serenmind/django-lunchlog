from datetime import datetime
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from django.contrib.auth import login

from .models import Receipt, PlaceInfo
from .serializers import (
    ReceiptSerializer,
    PlaceInfoSerializer,
    UserSignupSerializer,
    LoginSerializer,
)


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        ser = UserSignupSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = ser.save()
        return Response(
            {"id": user.id, "username": user.username}, status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        ser = LoginSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = ser.validated_data["user"]
        login(request, user)
        return Response({"id": user.id, "username": user.username})


class ReceiptViewSet(viewsets.ModelViewSet):
    serializer_class = ReceiptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Receipt.objects.filter(user=self.request.user).order_by("-date")
        month = self.request.query_params.get("month")
        if month:
            try:
                m = int(month)
                qs = qs.filter(date__month=m)
            except ValueError:
                pass
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RecommendationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        location = request.query_params.get("location")
        # naive recommendation: select top-rated places in DB that match location in address
        qs = PlaceInfo.objects.all()
        if location:
            qs = qs.filter(address__icontains=location)
        qs = qs.order_by("-rating")[:10]
        ser = PlaceInfoSerializer(qs, many=True)
        return Response(ser.data)
