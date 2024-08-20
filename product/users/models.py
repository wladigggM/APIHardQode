from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Кастомная модель пользователя - студента."""

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=250,
        unique=True
    )
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

    # TODO

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-id',)
