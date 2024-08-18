from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.serializers.user_serializer import CustomUserSerializer, BalanceSerializer
from users.models import Balance

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    http_method_names = ["get", "head", "options"]
    permission_classes = (permissions.IsAdminUser,)


class UserBalanceViewSet(viewsets.ModelViewSet):

    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer
    permission_classes = [permissions.IsAdminUser,]

    @action(detail=True, methods=['post'])
    def deposit(self, request, pk=None):
        amount = request.data.get('amount')
        if not amount:
            return Response({"Error": "Amount is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = int(amount)
            if amount < 0:
                raise ValueError("Amount must be positive")
        except ValueError as e:
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        user_balance = self.get_object()
        user_balance.deposit(amount)
        return Response({"balance": user_balance.balance}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def write_off(self, request, pk=None):
        amount = request.data.get('amount')
        if not amount:
            return Response({"Error": "Amount is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = int(amount)
            if amount < 0:
                raise ValueError("Amount must be positive")
        except ValueError as e:
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        user_balance = self.get_object()
        user_balance.write_off(amount)
        return Response({"balance": user_balance.balance}, status=status.HTTP_200_OK)

