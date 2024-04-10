from django.contrib.auth import get_user_model
from knox.auth import TokenAuthentication

User = get_user_model()

class SuperuserTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, token):
        user, token = super().authenticate_credentials(token)
        if not user.is_superuser:
            raise AuthenticationFailed('User is not a superuser.')
        return user, token