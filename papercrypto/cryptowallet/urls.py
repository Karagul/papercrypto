from django.urls import path

from . import views

app_name = 'cryptowallet'
urlpatterns = [
    path('', views.IndexView.as_view()),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('trade/', views.TradeView.as_view(), name='trade')
]