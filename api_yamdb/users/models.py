from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    USER_ROLES = (
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Admin')
    )

    bio = models.TextField(
        'Биография',
        blank=True,
        null=True
    )
    role = models.CharField(
        'Роль',
        default=USER,
        choices=USER_ROLES,
        max_length=55,
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=155,
        null=True
    )
    email = models.EmailField(
        'email',
        max_length=254,
        unique=True
    )

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser
