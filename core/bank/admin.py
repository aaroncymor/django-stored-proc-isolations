from django.contrib import admin
from .models import Account


# Register your models here.
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'balance')
    search_fields = ('account_number', )
    list_filter = ('balance', )
