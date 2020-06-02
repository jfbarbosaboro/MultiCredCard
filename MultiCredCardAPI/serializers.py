from rest_framework import serializers

class ClientSerializer(serializers.Serializer):
    CPF = serializers.CharField(max_length=11)
    FirstName = serializers.CharField(max_length=100)
    LastName = serializers.CharField(max_length=100)
    DateOfBirth = serializers.DateField()

class WalletSerializer(serializers.Serializer):
    CreditCards = serializers.ListField()
    LimitDefinedByClient = serializers.DecimalField(allow_null=True, max_digits=15, decimal_places=2)
    MaxLimit = serializers.DecimalField(allow_null=True, max_digits=15, decimal_places=2)
    MaxAvailableCredit = serializers.DecimalField(allow_null=True, max_digits=15, decimal_places=2)
    
class CreditCardSerializer(serializers.Serializer):
    Number = serializers.CharField(max_length=16)
    PrintedName = serializers.CharField(max_length=100)
    ValidThruMonth = serializers.IntegerField()
    ValidThruYear = serializers.IntegerField()
    CVV = serializers.CharField(max_length=3)
    Password = serializers.CharField(max_length=100)
    Limit = serializers.DecimalField(max_digits=15, decimal_places=2)
    AvailableCredit = serializers.DecimalField(max_digits=15, decimal_places=2)
    PaymentDueDate = serializers.IntegerField()
