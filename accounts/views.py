from django.shortcuts import render
from rest_framework import status, generics
from dj_rest_auth.registration.views import RegisterView as DJRegisterView
from dj_rest_auth.registration.views import LoginView as DJLoginView
from dj_rest_auth.views import UserDetailsView, PasswordChangeView
from accounts.models import UserProfile
from accounts.serializers import LibrarianRegisterSerializer, RegisterSerializer, UpdatePasswordSerilaizer, ChangePasswordSerilaizer
from django.contrib.auth import get_user_model
from rest_framework.response import Response


# Create your views here.
class RegisterView(DJRegisterView):
    model = get_user_model()
    serializer_class = RegisterSerializer


class LibrarianRegisterView(DJRegisterView):
    model = get_user_model()
    serializer_class = LibrarianRegisterSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        generated_password = get_user_model().objects.make_random_password(length=8)
        data["password"] = generated_password

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = {**self.get_response_data(user), "password": generated_password}

        if data:
            response = Response(
                data,
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        else:
            response = Response(status=status.HTTP_204_NO_CONTENT, headers=headers)

        return response


class LoginView(DJLoginView):
    pass


class UpdatePasswordView(UserDetailsView):
    serializer_class = UpdatePasswordSerilaizer


class ChangePasswordView(PasswordChangeView):
    pass

