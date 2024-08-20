from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

from courses.models import Course, Group


class CustomUser(AbstractUser):
    """Кастомная модель пользователя - студента."""

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=250,
        unique=True
    )
    is_student = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'password'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return self.get_full_name()


class Balance(models.Model):
    """Модель баланса пользователя."""
    DoesNotExist = None
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )
    balance = models.PositiveIntegerField(
        default=1000,
    )

    def deposit(self, amount):
        """Функция добавления балов"""
        if amount < 0:
            raise ValueError("Amount must be positive")
        self.balance += amount
        self.save()

    def write_off(self, amount):
        if amount < 0:
            raise ValueError("Amount must be positive")
        if self.balance - amount < 0:
            raise ValueError("Insufficient balance")
        self.balance -= amount
        self.save()

    # TODO

    class Meta:
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'
        ordering = ('-id',)


class Subscription(models.Model):
    """Модель подписки пользователя на курс."""
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        null=True,
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        null=True,
    )
    start_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    group = models.ForeignKey(Group, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-id',)
