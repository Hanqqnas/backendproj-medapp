from rest_framework_simplejwt.tokens import AccessToken

def create_custom_access_token(user):
    token = AccessToken.for_user(user)
    token['role'] = user.role
    return token
