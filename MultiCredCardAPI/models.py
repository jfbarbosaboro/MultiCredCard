from django.db import models
from django.conf import settings

# Create your models here.

class Client(models.Model):
    User = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    CPF = models.CharField(unique=True, max_length=11)
    FirstName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    DateOfBirth = models.DateField()

class Wallet(models.Model):
    Client = models.OneToOneField(
        Client,
        on_delete=models.CASCADE
    )
    LimitDefinedByClient = models.DecimalField(null=True, max_digits=15, decimal_places=2)

class CreditCard(models.Model):
    Wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    Number = models.CharField(max_length=16)
    PrintedName = models.CharField(max_length=100)
    ValidThruMonth = models.IntegerField()
    ValidThruYear = models.IntegerField()
    CVV = models.CharField(max_length=3)
    Password = models.CharField(max_length=100)
    Limit = models.DecimalField(null=True, max_digits=15, decimal_places=2)
    AvailableCredit = models.DecimalField(null=True, max_digits=15, decimal_places=2)
    PaymentDueDate = models.IntegerField()

# This is the main function of the system
def CreditCardComparerGenerator(currentDay):
    def CreditCardComparer(card1, card2):
        #If the credit cards have the same Payment Due Dates and the Same Limits,
        #the preferable credit card is that with smaller AvailableCredit
        if card1.PaymentDueDate == card2.PaymentDueDate:
            if card1.Limit == card2.Limit:
                return card1.AvailableCredit - card2.AvailableCredit
            else:
                #If they have different Limits, the preferable is that with smaller Limit
                return card1.Limit - card2.Limit
        else:
            # If the Payment Due Date are different, the preferable is that with most distant Payment Due Date
            if card1.PaymentDueDate <= currentDay and currentDay <= card2.PaymentDueDate:
                return -1
            else:
                return card2.PaymentDueDate - card1.PaymentDueDate
    return CreditCardComparer


