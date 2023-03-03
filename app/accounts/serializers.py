from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class UserInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "alert_email",
            "full_name",
            "city",
            "state",
            "gender",
            "sector",
        ]


class UserCreateInputSerializer(serializers.ModelSerializer):
    jwt = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "alert_email",
            "password",
            "full_name",
            "city",
            "state",
            "gender",
            "sector",
            "jwt",
        ]

        extra_kwargs = {
            "id": {"read_only": True},
            "password": {"write_only": True},
        }

    def validate_password(self, value: str) -> str:
        return make_password(value)

    def get_jwt(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class UserOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "alert_email",
            "full_name",
            "city",
            "state",
            "gender",
            "sector",
            "last_login",
            "date_joined",
        ]


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password1 = serializers.CharField(
        max_length=128, write_only=True, required=True
    )
    new_password2 = serializers.CharField(
        max_length=128, write_only=True, required=True
    )

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                _("Your old password was entered incorrectly. Please enter it again.")
            )
        return value

    def validate(self, data):
        if data["new_password1"] != data["new_password2"]:
            raise serializers.ValidationError(
                {"new_password2": _("The two password fields didn't match.")}
            )
        password_validation.validate_password(
            data["new_password1"], self.context["request"].user
        )
        return data

    def save(self, **kwargs):
        password = self.validated_data["new_password1"]
        user = self.context["request"].user
        user.set_password(password)
        user.save()
        return user
