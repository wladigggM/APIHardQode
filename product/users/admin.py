from django.contrib import admin

from .models import Balance


# Register your models here.
@admin.register(Balance)
class BalanceModelAdmin(admin.ModelAdmin):
    """Модель баланса в админке"""

    list_display = ('user', 'balance')
    readonly_fields = ('balance',)

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_staff:
            return []
        return self.readonly_fields

