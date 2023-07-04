from constants import (EMAIL_MAX_LENGTH, PASSWORD_MAX_LENGTH,
                       USERNAME_MAX_LENGTH)
from django.contrib.auth.models import AbstractUser
from django.db import models
from users.validators import UsernameRegexValidator


class User(AbstractUser):
    """Модель пользователя"""
    email = models.EmailField(
        'Электронная почта',
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
        blank=False,
        null=False
    )
    username = models.CharField(
        'Имя пользователя',
        validators=(UsernameRegexValidator(),),
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        blank=False,
        null=False,
    )
    first_name = models.CharField(
        'Имя',
        max_length=USERNAME_MAX_LENGTH,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=USERNAME_MAX_LENGTH,
        blank=True
    )
    password = models.CharField(
        'Пароль',
        max_length=PASSWORD_MAX_LENGTH,
    )

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email',
            )
        ]

    def __str__(self) -> str:
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['author']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'user'],
                name='unique_follow',
            )
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
