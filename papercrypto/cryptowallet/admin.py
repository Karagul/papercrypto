from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from cryptowallet.models import Coin, User, Wallet, Transaction, Portfolio

# Register your models here.
admin.site.register(Coin)
admin.site.register(User, UserAdmin)
admin.site.register(Wallet)
admin.site.register(Transaction)
admin.site.register(Portfolio)
 