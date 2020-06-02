def GetCreditCardMockedData(creditCard):
    finalDigit = creditCard["Number"][-1]
    limit = None
    availableCredit = None
    paymentDueDate = None
    inexistent = [
        '1111111111111111',
        '2222222222222222',
        '3333333333333333',
        '4444444444444444',
        '5555555555555555',
        '6666666666666666',
        '7777777777777777',
        '8888888888888888',
        '9999999999999999',
    ]

    if creditCard["Number"] in inexistent or len(creditCard["Number"]) != 16:
        return None, None, None

    if finalDigit == '0':
        limit = 1000
        availableCredit = 1000
        paymentDueDate = 1

    if finalDigit == '1':
        limit = 1000
        availableCredit = 1000
        paymentDueDate = 28
    
    if finalDigit == '2':
        limit = 1000
        availableCredit = 0
        paymentDueDate = 15

    if finalDigit == '3':
        limit = 2000
        availableCredit = 1800
        paymentDueDate = 28

    if finalDigit == '4':
        limit = 2000
        availableCredit = 1800
        paymentDueDate = 19

    if finalDigit == '5':
        limit = 2000
        availableCredit = 10
        paymentDueDate = 19

    if finalDigit == '6':
        limit = 3000
        availableCredit = 500
        paymentDueDate = 19

    if finalDigit == '7':
        limit = 3000
        availableCredit = 500
        paymentDueDate = 15

    if finalDigit == '8':
        limit = 3000
        availableCredit = 0
        paymentDueDate = 15

    if finalDigit == '9':
        limit = 10000
        availableCredit = 8000
        paymentDueDate = 3

    return limit, availableCredit, paymentDueDate