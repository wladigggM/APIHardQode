from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers

from users.models import Subscription, Balance

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователей."""

    class Meta:
        model = User
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписки."""

    # TODO

    class Meta:
        model = Subscription
        fields = (
            # TODO
        )


class BalanceSerializer(serializers.ModelSerializer):
    """Сериализатор баланса."""

    # TODO

    class Meta:
        model = Balance
        fields = (
            'user',
            'balance',
        )
