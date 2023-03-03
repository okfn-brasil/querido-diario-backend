from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import (
    PasswordChangeSerializer,
    UserCreateInputSerializer,
    UserOutputSerializer,
)


class UsersMeView(UpdateAPIView, RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserOutputSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UsersView(CreateAPIView):
    authentication_classes = []
    serializer_class = UserCreateInputSerializer


class UsersEmailVerify(APIView):
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        email = kwargs.get("email", None)
        if email is None:
            raise ValidationError(
                {"email": ["empty email"]},
            )

        try:
            User.objects.get(email=email)
            return Response(status=status.HTTP_200_OK)
        except User.DoesNotExist:
            raise NotFound()


class UserPasswordChangeView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordChangeSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  # noqa
        return Response(status=status.HTTP_200_OK)
