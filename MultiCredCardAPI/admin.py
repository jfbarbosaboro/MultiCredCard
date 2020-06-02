from django.contrib import admin
from .models import Client, Wallet, CreditCard

# Register your models here.

admin.site.register(Client)
admin.site.register(Wallet)
admin.site.register(CreditCard)