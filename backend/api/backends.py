from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

class EmailOrMobileBackend(BaseBackend):
    def authenticate(self, request, email=None, phone=None, password=None, **kwargs):
        UserModel = get_user_model()
        if email is not None:
            try:
                user = UserModel.objects.get(email=email)
            except UserModel.DoesNotExist:
                return None
        elif phone is not None:
            try:
                user = UserModel.objects.get(phone=phone)
            except UserModel.DoesNotExist:
                return None
        else:
            return None

        if user.check_password(password):
            return user