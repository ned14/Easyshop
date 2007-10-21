# zope imports
from zope.interface import Interface
from zope.interface import Attribute

class IPaymentMethod(Interface):
    """A marker interface for payment content objects.
    """

class IShopPaymentMethod(IPaymentMethod):
    """A marker interface for shop payment content objects, means payment
    methods which doesn't need any customer related information and hence 
    live just once within shop level. Example: PayPal.
    """    

class ICustomerPaymentMethod(IPaymentMethod):
    """A marker interface for customer payment content objects, means
    payment methods which holds information per customer and hence live 
    within customer objects. Example: direct debit
    """    

class ISimplePaymentMethod(IShopPaymentMethod):
    """A marker interface for simple payment content objects.
    
    Note, that this is also a IShopPaymentMethod, means it needs no
    further information per customer.
    """

    payed = Attribute("""
        If checked an order gets the "payed"-state after processing this
        payment method, otherwhise "not payed" """)
        
class IPayPal(IShopPaymentMethod):
    """A marker interface for paypal content objects. 
    
    Note, that this is also a IShopPaymentMethod, means it needs no
    further information per customer.
    """
    
class IDirectDebit(ICustomerPaymentMethod):
    """A marker interface for direct debit content objects.
    
    Note, that this is also a ICustomerPaymentMethod, means it needs 
    further information (bank details) per customer.    
    """

class IPaymentMethodValidator(Interface):
    """A corresponding validator object for a customer payment method object.
    It *can* exist within shop level to decide whether a customer payment
    method (like direct debit) is generally allowed or not. To manage this it
    holds criterion objects (just like shop payment objects).
    """
    
class IPaymentPrice(Interface):
    """A marker interface for payment price content objects.
    """

class IPaymentPrices(Interface):
    """Provides methods to manage payment prices content object and 
    prices and taxes for them.
    """
    
class IPaymentManagement(Interface):
    """Provides methods to manage payment methods.
    """
    def deletePaymentMethod(id):
        """Deletes a Payment Method by given id.
        """            

    def getPaymentMethod(id):
        """Returns payment method by given id.
        """
    
    def getPaymentMethods():
        """Returns all payment informations.
        """
    
    def getSelectedPaymentMethod():
        """Returns the actual payment information.
        """
        
class IPaymentProcessing(Interface):
    """Provides methods to processing a payment.
    """

    def process(order):
        """Processes a payment.
        """

class IPaymentMethodsContainer(Interface):
    """A marker interface for payment method folder content objects.
    """

class IPaymentPricesContainer(Interface):
    """A marker interface for payment price folder objects.
    """

