import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES = (
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN),
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Логин',
        help_text='Имя пользователя',
    )
    email = models.EmailField(unique=True, max_length=254)
    role = models.CharField(
        max_length=20,
        choices=ROLES,
        default=USER,
        verbose_name='Роль',
        help_text='Права пользователя',
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография',
        null=True,
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Имя',
        help_text='Имя',
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Фамилия',
        help_text='Фамилия',
    )
    password = models.CharField(max_length=100, null=True)
    confirmation_code = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email',)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    def code_check(self, confirmation_code):
        return self.confirmation_code == confirmation_code
