from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import ReceiptImage


from .models import Receipt, PlaceInfo
from .serializers import (
    ReceiptSerializer,
    PlaceInfoSerializer,
    ReceiptImageSerializer,
)

class ReceiptViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Receipt objects.
    Provides CRUD operations and image upload for receipts.
    """
    serializer_class = ReceiptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Returns a queryset of Receipt objects belonging to the authenticated user,
        optionally filtered by the 'month' query parameter.

        Query Params:
            - month (int, optional): Filters receipts by the given month (1-12).
        """
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
        """
        Associates the created Receipt object with the authenticated user.
        """
        serializer.save(user=self.request.user)

    @action(
        detail=True,
        methods=["post"],
        url_path="upload-images",
    )
    def upload_images(self, request, pk=None):
        """
        Bulk uploads images to a specific receipt.

        Request:
            - images (list of files): Multiple image files to be uploaded.

        Responses:
            - 201 Created: Returns serialized data of successfully uploaded images.
            - 400 Bad Request: If no images are provided or all uploads fail, returns error details.
        """
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
                receipt_image = ReceiptImage(receipt=receipt)
                receipt_image.image = f
                receipt_image.save()
                created.append(ReceiptImageSerializer(receipt_image).data)
            except Exception as exc:
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
    """
    API view to provide top 10 recommended places, optionally filtered by location.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        location = request.query_params.get("location")
        qs = PlaceInfo.objects.all()
        if location:
            qs = qs.filter(address__icontains=location)
        qs = qs.order_by("-rating")[:10]
        ser = PlaceInfoSerializer(qs, many=True)
        return Response(ser.data)
