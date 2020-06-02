from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Client, Wallet, CreditCard, CreditCardComparerGenerator
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import BasicAuthentication
from .serializers import ClientSerializer, WalletSerializer, CreditCardSerializer
from .mock import GetCreditCardMockedData
from datetime import datetime
from functools import cmp_to_key

# Create your views here.

@api_view(['POST'])
def CreateAccount(request):
    clientData = JSONParser().parse(request)
    print(str(clientData))

    if IsNewClient(clientData):
        user = User.objects.create_user(clientData['CPF'], clientData['Email'], clientData['Password'])
        client = Client(
            User=user,
            FirstName=clientData["FirstName"],
            LastName=clientData["LastName"],
            CPF=clientData["CPF"],
            DateOfBirth=clientData["DateOfBirth"])
        client.save()
        wallet = Wallet(Client = client)
        wallet.save()
        return HttpResponse(content="Client successfuly created!", status=200)
    else:
        return HttpResponse(content="There is already an account for this CPF.",status=409)


def IsNewClient(clientData):
    existentCPF = Client.objects.filter(CPF=clientData['CPF'])
    if existentCPF:
        return False
    else:
        return True


@api_view(['POST'])
@authentication_classes([BasicAuthentication])
def AddCreditCard(request):
    if request.user.is_authenticated:
        cardData = JSONParser().parse(request)
        existent = list(CreditCard.objects.filter(Number=cardData['Number']))
        if not existent:
            wallet = Wallet.objects.get(Client__CPF=request.user.username)
            
            # Getting mocked data about the credit card.
            # This should be obtained via credit card administrator's API
            limit, availableCredit, paymentDueDate = GetCreditCardMockedData(cardData)
            if limit == None or availableCredit == None:
                return HttpResponse(content="This is not a valid credit card.", status=400)
            
            creditCard = CreditCard(
                Wallet=wallet,
                Number=cardData["Number"],
                PrintedName=cardData["PrintedName"],
                ValidThruMonth=cardData["ValidThruMonth"],
                ValidThruYear=cardData["ValidThruYear"],
                CVV=cardData["CVV"],
                Password=cardData["Password"],
                Limit=limit,
                AvailableCredit=availableCredit,
                PaymentDueDate=paymentDueDate
            )
            creditCard.save()
            return HttpResponse(content="Card successfuly added!", status=200)
        else:
            return HttpResponse(content="This card is already in the system.", status=409)
    else:
        return HttpResponse(status=401)
    
@api_view(['DELETE'])
@authentication_classes([BasicAuthentication])
def RemoveCreditCard(request):
    if request.user.is_authenticated:
        number = JSONParser().parse(request)["Number"]
        try:
            creditCard = CreditCard.objects.get(Number=number, Wallet__Client__CPF=request.user.username)
            creditCard.delete()
        finally:
            return HttpResponse(content="Card successfuly removed!", status=200)
    else:
        return HttpResponse(status=401)

@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def GetWallet(request):
    if request.user.is_authenticated:
        wallet = Wallet.objects.get(Client__CPF=request.user.username)

        creditCards = sorted(list(CreditCard.objects.filter(Wallet=wallet)), key=cmp_to_key(CreditCardComparerGenerator(datetime.today().day)))

        credidCardsSerializer = CreditCardSerializer(creditCards, many=True)

        maxLimit = 0
        maxAvailableCredit = 0
        for creditCard in list(creditCards):
            maxLimit += creditCard.Limit
            maxAvailableCredit += creditCard.AvailableCredit

        walletSerializer = WalletSerializer(
            {
                "CreditCards":credidCardsSerializer.data,
                "MaxLimit":maxLimit, 
                "LimitDefinedByClient":wallet.LimitDefinedByClient,
                "MaxAvailableCredit":maxAvailableCredit
            }
        )

        return JsonResponse(walletSerializer.data)

    else:
        return HttpResponse(status=401)

@api_view(['PUT'])
@authentication_classes([BasicAuthentication])
def SetLimitDefinedByClient(request):
    if request.user.is_authenticated:
        definedLimit = JSONParser().parse(request)["LimitDefinedByClient"]
        wallet = Wallet.objects.get(Client__CPF=request.user.username)

        creditCards = CreditCard.objects.filter(Wallet=wallet)
        maxLimit = 0
        for creditCard in list(creditCards):
            maxLimit += creditCard.Limit
        
        if (maxLimit < definedLimit):
            return HttpResponse(content="The limit must be less than or equal to the sum of all credit card limits.", status=400)

        wallet.LimitDefinedByClient = definedLimit
        wallet.save()
        return HttpResponse(content="Wallet limit successfuly updated!", status=200)
    else:
        return HttpResponse(status=401)

@api_view(['POST'])
@authentication_classes([BasicAuthentication])
def MakeAPayment(request):
    if request.user.is_authenticated:
        paymentData = JSONParser().parse(request)
        value = paymentData['Value']
        cnpj = paymentData['CNPJ']

        wallet = Wallet.objects.get(Client__CPF=request.user.username)
        creditCards = sorted(list(CreditCard.objects.filter(Wallet=wallet)), key=cmp_to_key(CreditCardComparerGenerator(datetime.today().day)))

        totalAvailableCredit = 0
        for creditCard in creditCards:
            totalAvailableCredit += creditCard.AvailableCredit

        if value > wallet.LimitDefinedByClient:
            return HttpResponse(content="Insufficient limit.", status=403)
        elif value > totalAvailableCredit:
            return HttpResponse(content="Insufficient credit.", status=403)
        else:
            creditCardsForUniqueTransaction = list(filter(lambda x: x.AvailableCredit >= value, creditCards))
            if creditCardsForUniqueTransaction:
                CallCreditCardAdministratorForPayment(cnpj, creditCardsForUniqueTransaction[0], value)
                creditCardsForUniqueTransaction[0].AvailableCredit -= value
                creditCardsForUniqueTransaction[0].save()
            else:
                for creditCard in creditCards:
                    if value >= creditCard.AvailableCredit:
                        value -= creditCard.AvailableCredit
                        CallCreditCardAdministratorForPayment(cnpj, creditCard, creditCard.AvailableCredit)
                        creditCard.AvailableCredit = 0
                        creditCard.save()
                    else:
                        CallCreditCardAdministratorForPayment(cnpj, creditCard, value)
                        creditCard.AvailableCredit -= value
                        creditCard.save()
                        break
            return HttpResponse(content="Payment completed successfuy!.", status=200)
    else:
        return HttpResponse(status=401)

@api_view(['PUT'])
@authentication_classes([BasicAuthentication])
def CreditRelease(request):
    if request.user.is_authenticated:
        carData = JSONParser().parse(request)
        releaseValue =carData["ReleaseValue"]
        number = carData["Number"]
        try:
            creditCard = CreditCard.objects.get(Number=number, Wallet__Client__CPF=request.user.username)
            if creditCard.AvailableCredit + releaseValue > creditCard.Limit:
                return HttpResponse(content="The total available credit cannot be greater than the credit card's limit.", status=403)
            else:
                creditCard.AvailableCredit += releaseValue
                creditCard.save()
                return HttpResponse(content="Credit was successfuly release.", status=200)
        except:
            return HttpResponse(status=401)
    else:
        return HttpResponse(status=401)

def CallCreditCardAdministratorForPayment(cnpj, creditCard, value):
    # This is just a mocked function to simulate a call to 
    # credit card administrator API to make a payment.
    pass

def CallCreditCardAdministratorForCreditRelease(creditCard, value):
    # This is just a mocked function to simulate a call to 
    # credit card administrator API to make a payment.
    pass