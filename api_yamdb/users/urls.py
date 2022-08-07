from api.views import signup_user, token_generate
from django.urls import path

app_name = 'users'
urlpatterns = [
    path(
        'token/',
        token_generate,
        name='token_generate'
    ),
    path('signup/', signup_user, name='signup'),
]
