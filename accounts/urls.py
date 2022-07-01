from django.urls import path
from accounts.views import RegisterView, LibrarianRegisterView, LoginView, UpdatePasswordView, ChangePasswordView



urlpatterns = [
    path('register/', RegisterView.as_view(), name='RegisterView'),
    path('create_librarian/', LibrarianRegisterView.as_view(), name='LibrarianRegisterView'),
    path('login/',LoginView.as_view(), name='LoginView'),
    path('update_password/', UpdatePasswordView.as_view(), name='UpdatePasswordView'),
    path('change_password/', ChangePasswordView.as_view(), name='ChangePasswordView'),
]