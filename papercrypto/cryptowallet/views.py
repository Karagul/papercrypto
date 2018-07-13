from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.generic import View, TemplateView
from django.core import serializers

import json

# Import models
from .models import Portfolio, Wallet, Transaction, User, Coin

# Create your views here.
class IndexView(TemplateView):
    template_name = "index.html"
    def get(self, request):
        return HttpResponse("Index")

# Main dashboard
class DashboardView(TemplateView):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        portfolio = Portfolio.objects.get(user=user)
        portfolio_value = "{:,.2f}".format(portfolio.total_value())
        portfolio_cash = "{:,.2f}".format(portfolio.cash)

        recent_transactions = Transaction.objects.order_by('-execution_date')[:5]
        wallets = portfolio.wallet_set.all()

        
        percentages = portfolio.value_percentages()
        btc_pct = percentages["BTC"]
        bch_pct = percentages["BCH"]
        eth_pct = percentages["ETH"]
        ltc_pct = percentages["LTC"]
        cash_pct = percentages["USD"]
        context = {
            'portfolio_value': portfolio_value,
            'portfolio_cash': portfolio_cash,
            'recent_transactions': recent_transactions,
            'wallets': wallets,
            'btc_pct': btc_pct,
            'bch_pct': bch_pct,
            'eth_pct': eth_pct,
            'ltc_pct': ltc_pct,
            'cash_pct': cash_pct
        }
        return render(request, 'cryptowallet/dashboard.html', context)

# Trade page where transactions can be made
class TradeView(TemplateView):
    template_name = "trade.html"

    def get(self, request, *args, **kwargs):
        user = self.request.user
        portfolio = Portfolio.objects.get(user=user)
        portfolio_value = "{:,.2f}".format(portfolio.total_value())
        portfolio_cash = "{:,.2f}".format(portfolio.cash)
        wallets = portfolio.wallet_set.all()
        transaction = Transaction()
        context = {
            'portfolio_value': portfolio_value,
            'portfolio_cash': portfolio_cash,
            'transaction': transaction
        }
        return render(request, 'cryptowallet/trade.html', context)

# Wallet page where individual wallets can be looked at in more detail
