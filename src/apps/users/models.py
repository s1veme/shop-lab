from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username: str, password: str) -> 'User':
        if not username:
            raise TypeError('The "username" field is required')
        if not password:
            raise TypeError('The "password" field is required')

        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username: str, password: str) -> 'User':
        user = self.create_user(username, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Имя пользователя', max_length=254, unique=True)

    is_active = models.BooleanField(verbose_name='Активен ли пользователь?', default=True)
    is_staff = models.BooleanField(verbose_name='Пользователь является администратором?', default=False)

    USERNAME_FIELD = 'username'

    objects = UserManager()

    def __str__(self) -> str:
        return str(self.username)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
