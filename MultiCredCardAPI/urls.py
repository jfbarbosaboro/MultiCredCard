from django.contrib import admin
from django.urls import path
from .views import CreateAccount, AddCreditCard, GetWallet, SetLimitDefinedByClient, RemoveCreditCard, MakeAPayment, CreditRelease


urlpatterns = [
    path('createaccount/', CreateAccount),
    path('addcreditcard/', AddCreditCard),
    path('removecreditcard/', RemoveCreditCard),
    path('getwallet/', GetWallet),
    path('setLimitDefinedByClient/', SetLimitDefinedByClient),
    path('makeapayment/', MakeAPayment),
    path('creditrelease/', CreditRelease)
]