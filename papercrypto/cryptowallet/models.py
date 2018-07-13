from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import AbstractUser

import gdax
from decimal import Decimal

public_client = gdax.PublicClient()

# Create your models here.
class Coin(models.Model):
    symbol = models.CharField(max_length=16)
    name = models.CharField(max_length=64)

    def exchange_rate(self):
        prod = str(self.symbol) + '-USD'
        # Try API call up to 3 times (sometimes fails)
        success = False
        for i in range(5):
            try:
                exchange_rate = public_client.get_product_ticker(product_id=prod)["price"]
                break
            except Exception:
                print("ERROR: API call failed for %s" % prod)

        return float(exchange_rate)

    def __str__(self):
        return "%s - %s" % (self.symbol, self.name)

class User(AbstractUser):
    pass

class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cash = models.DecimalField(max_digits=22, decimal_places=2)

    def total_value(self):
        total = float(self.cash)
        wallets = self.wallet_set.all()
        for wallet in wallets:
            total += wallet.cash_value()
        return total

    def value_percentages(self):
        percentages = {}
        wallets = self.wallet_set.all()
        for wallet in wallets:
            percentages[str(wallet.coin.symbol)] = (float(wallet.cash_value()) /
                                                    float(self.total_value())) * 100.0
        percentages["USD"] = float(self.cash) / self.total_value() * 100.0
        return percentages

    def __str__(self):
        wallets = self.wallet_set.all()
        ret = ""
        for wallet in wallets:
            ret += "%s " % wallet
        return "%s- Cash: %f" % (ret, self.cash)

class Wallet(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=18, decimal_places=4)

    def cash_value(self):
        return self.coin.exchange_rate() * float(self.quantity)

    def __str__(self):
        return "%s - %s - %f" % (self.portfolio.user, self.coin, self.quantity)



class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12, decimal_places=4)
    buy = models.BooleanField()
    execution_date = models.DateTimeField(auto_now_add=True)
    execution_price = models.DecimalField(max_digits=22, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.buy:
                self.wallet.quantity = self.wallet.quantity + self.quantity
                self.wallet.portfolio.cash = self.wallet.portfolio.cash - (self.quantity *
                                                                           self.execution_price)
            else:
                self.wallet.quantity = self.wallet.quantity - self.quantity
                self.wallet.portfolio.cash = self.wallet.portfolio.cash + (self.quantity *
                                                                           self.execution_price)
            self.wallet.save()
            self.wallet.portfolio.save()
        super().save(*args, **kwargs)  # Call the "real" save() method.

    def __str__(self):
        transaction_type = ""
        if self.buy:
            transaction_type = "BOUGHT"
        else:
            transaction_type = "SOLD"
        return "%s, %s %f units\nPrice/unit: %f\nDate: %s" % (self.wallet, transaction_type,
                                                              self.quantity, self.execution_price,
                                                              self.execution_date)

class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['wallet', 'quantity', 'buy']

    