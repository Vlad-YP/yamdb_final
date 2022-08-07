from django.urls import path

from api.views import token_generate, signup_user


app_name = 'users'
urlpatterns = [
    path(
        'token/',
        token_generate,
        name='token_generate'
    ),
    path('signup/', signup_user, name='signup'),
]
