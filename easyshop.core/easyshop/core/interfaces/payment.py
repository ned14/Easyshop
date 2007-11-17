# zope imports
from zope.interface import Interface
from zope.interface import Attribute
from zope import schema

# easyshop.core imports
from easyshop.core.config import _

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
    """
    
class IDirectDebit(ICustomerPaymentMethod):
    """A direct debit content object. Note, that this is also a 
    ICustomerPaymentMethod, means it needs information (bank details) per 
    customer.    
    """
    account_number = schema.TextLine(
        title=_(u'Account Number'),
        description=_(u"Please enter your account number"),
        default=u'',
        required=True,
    )
    
    bank_identification_code = schema.TextLine(
        title=_(u'Bank Information Code'),
        description=_(u"Please enter your bank information code"),
        default=u'',
        required=True,
    )
    
    depositor = schema.TextLine(
        title=_(u'Depositor'),
        description=_(u"Please enter the depositor of the account"),
        default=u'',
        required=True,
    )
    
    bank_name = schema.TextLine(
        title=_(u'Bank Name'),
        description=_(u"Please enter the bank name"),
        default=u'',
        required=True,
    )

class ICreditCard(ICustomerPaymentMethod):
    """A credit cart content object. Note, that this is also a 
    ICustomerPaymentMethod, means it needs information per customer.
    """
    card_type = schema.TextLine(
        title=_(u'Card Type'),
        description=_(u"Please enter the type of the card."),
        default=u'',
        required=True,
    )

    card_owner = schema.TextLine(
        title=_(u'Card Owner'),
        description=_(u"Please enter your the name of the card owner."),
        default=u'',
        required=True,
    )

    card_number = schema.TextLine(
        title=_(u'Card Number'),
        description=_(u"Please enter your the card number."),
        default=u'',
        required=True,
    )

    card_expiration_date = schema.TextLine(
        title=_(u'Expiration Date'),
        description=_(u"Please enter the expiration date of the card."),
        default=u'',
        required=True,
    )

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

