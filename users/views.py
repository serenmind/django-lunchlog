from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .serializers import UserSignupSerializer


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serialized_user = UserSignupSerializer(data=request.data)
        serialized_user.is_valid(raise_exception=True)
        user = serialized_user.save()
        return Response({"id": user.id, "username": user.username}, status=status.HTTP_201_CREATED)
