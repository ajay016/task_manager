from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # # UserModel = User
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None
        
        # UserModel = User
        # try:
        #     user = UserModel.objects.get(
        #         Q(username__iexact=username) | Q(email__iexact=username)
        #     )
        # except UserModel.DoesNotExist:
        #     return None
        # if user.check_password(password) and self.user_can_authenticate(user):
        #     return user
        # return None