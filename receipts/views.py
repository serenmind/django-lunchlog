from datetime import datetime
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from django.contrib.auth import login
from .models import ReceiptImage


from .models import Receipt, PlaceInfo
from .serializers import (
    ReceiptSerializer,
    PlaceInfoSerializer,
    UserSignupSerializer,
    LoginSerializer,
    ReceiptImageSerializer,
)

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serialized_user = UserSignupSerializer(data=request.data)
        serialized_user.is_valid(raise_exception=True)
        user = serialized_user.save()
        return Response(
            {"id": user.id, "username": user.username}, status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_login_data = LoginSerializer(data=request.data)
        user_login_data.is_valid(raise_exception=True)
        user = user_login_data.validated_data["user"]
        login(request, user)
        return Response({"id": user.id, "username": user.username})


class ReceiptViewSet(viewsets.ModelViewSet):
    serializer_class = ReceiptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Receipt.objects.filter(user=self.request.user).order_by("-date")

        # filter queryset by month if month query is provided.
        month = self.request.query_params.get("month")
        if month:
            try:
                m = int(month)
                qs = qs.filter(date__month=m)
            except ValueError:
                pass
        return qs

    def perform_create(self, serializer):
        # This ensures the logged-in user is attached
        serializer.save(user=self.request.user)

    @action(
        detail=True,
        methods=["post"],
        url_path="upload-images",
    )
    def upload_images(self, request, pk=None):
        """bulk upload images to a receipt"""
        receipt = self.get_object()
        files = request.FILES.getlist("images")

        if not files:
            return Response(
                {"detail": "No images provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        created = []
        errors = []

        for idx, f in enumerate(files):
            try:
                # create model instance and let Django storage handle upload to S3
                receipt_image = ReceiptImage(receipt=receipt)
                # assign file to ImageField; saving the model triggers the storage backend
                receipt_image.image = f
                receipt_image.save()
                created.append(ReceiptImageSerializer(receipt_image).data)
            except Exception as exc:  # capture storage/validation errors per-file
                errors.append({"filename": getattr(f, "name", str(idx)), "error": str(exc)})

        if not created:
            return Response(
                {"detail": "Failed to upload any images", "errors": errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        status_code = status.HTTP_201_CREATED
        payload = {"created": created}
        if errors:
            payload["errors"] = errors

        return Response(payload, status=status_code)

        


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
