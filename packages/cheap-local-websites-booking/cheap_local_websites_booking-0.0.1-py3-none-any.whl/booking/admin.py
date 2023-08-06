from django.contrib import admin
from .models import Client

class ClientAdmin(admin.ModelAdmin):
    search_fields = ['name', 'business name', 'email', 'phone_number']
    list_display = ('name', 'phone_number', 'business_name', 'email')

admin.site.register(Client, ClientAdmin)