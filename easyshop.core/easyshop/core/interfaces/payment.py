# zope imports
from zope.interface import Interface
from zope.interface import Attribute
from zope import schema

# easyshop.core imports
from easyshop.core.config import _
from easyshop.core.config import CREDIT_CARDS_CHOICES
from easyshop.core.config import CREDIT_CARD_MONTHS_CHOICES
from easyshop.core.config import CREDIT_CARD_YEARS_CHOICES

class IPaymentMethod(Interface):
    """Marker interface for payment methods.
    """

class ISelectablePaymentMethod(Interface):
    """Marker interface for payment methods which can be selected by a customer.
    """

class IAsynchronPaymentMethod(Interface):
    """Marker interface for payment methods which redirect to the payment 
    service, e.g. PayPal.
    """    
    
class ICreditCardPaymentMethod(IPaymentMethod):
    """Marker interface payment via credit card.
    """        
    
class IDirectDebitPaymentMethod(IPaymentMethod):
    """Marker interface for payment via direct debit.
    """

class IPayPalPaymentMethod(IPaymentMethod, ISelectablePaymentMethod, IAsynchronPaymentMethod):
    """Marker interface for payment via PayPal.
    """

class IGenericPaymentMethod(IPaymentMethod, ISelectablePaymentMethod):
    """A generic payment method.
    """
    payed = Attribute("""If checked an order gets the "payed"-state after 
        processing this payment method, otherwhise "not payed" """)

class IPaymentInformation(Interface):
    """Marker interface for payment information.
    """
    
class IBankAccount(IPaymentInformation):
    """Stores information of a bank account.
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

class ICreditCard(IPaymentInformation):
    """Stores information of a credit card.
    """
    card_type = schema.Choice(
        title=_(u"Card Type"),
        description=_(u"Please select the type of the card."),
        vocabulary = schema.vocabulary.SimpleVocabulary.fromItems(
            CREDIT_CARDS_CHOICES.items()))
    
    card_owner = schema.TextLine(
        title=_(u'Card Owner'),
        description=_(u"Please enter the name of the card owner."),
        default=u'',
        required=True,
    )

    card_number = schema.TextLine(
        title=_(u'Card Number'),
        description=_(u"Please enter your the card number."),
        default=u'',
        required=True,
    )

    card_expiration_date_month = schema.Choice(
        title=_(u'Expiration Date Month'),
        description=_(u"Please enter the expiration date of the card."),
        vocabulary = schema.vocabulary.SimpleVocabulary.fromItems(
            CREDIT_CARD_MONTHS_CHOICES),
        default=u"01")

    card_expiration_date_year = schema.Choice(
        title=_(u'Expiration Date Year'),
        description=_(u"Please enter the expiration date of the card."),
        vocabulary = schema.vocabulary.SimpleVocabulary.fromItems(
            CREDIT_CARD_YEARS_CHOICES),
        default=u"2007")


class IPaymentPrice(Interface):
    """A marker interface for payment price content objects.
    """

class IPaymentPriceManagement(Interface):
    """Provides all methods to manage the payment prices. This includes also 
    calculation of prices and taxes (maybe this will separated later to 
    different interfaces, e.g.: IPaymentPriceManagement, IPaymentPrices, 
    IPaymentTaxes).
    """
    def getPaymentPrices():
        """Return all payment prices.
        """

    def getPriceGross():
        """Returns the gross price for selected payment method.
        """

    def getPriceForCustomer():
        """Returns customer's price for selected payment method.
        """
        
    def getPriceNet():
        """Returns the net price for selected payment method.
        """

    def getTax():
        """Returns the default tax for the payment price.
        """

    def getTaxForCustomer():
        """Returns customer's tax for the payment price.
        """

    def getTaxRate():
        """Returns the default tax rate for the payment price.
        """

    def getTaxRateForCustomer():
        """Returns customer's tax rate for the payment price.
        """

class IPaymentMethodManagement(Interface):
    """Methods to manage payment methods on shop level. Payment methods are for
    instance: prepayment, direct debit, PayPal, credit card, cash on delivery.

    Some payment methods need additional payment information on customer level
    like: bank accounts for direct debit or credit cards (data of a credit card,
    like card number) for credit card (the payment method). Methods to manage 
    these payment information are provided by IPaymentInformationManagement. 
    See there for more.
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
    
class IPaymentInformationManagement(Interface):
    """Provides methods to manage payment information.
    """
    def deletePaymentInformation(id):
        """Deletes a payment information by given id.
        """

    def getPaymentInformation(id):
        """Returns payment information by given id.
        """

    def getPaymentInformations(interface=None, check_validity=False):
        """Returns all payment information of a customer.
        """

    def getSelectedPaymentInformation(check_validity=False):
        """Returns the selected payment information.
        """

    def getSelectedPaymentMethod(check_validity=False):
        """Returns the selected payment method.
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

class IPaymentPriceManagementContainer(Interface):
    """A marker interface for payment price folder objects.
    """

class IPaymentResult(Interface):
    """Result which is returned by payment processors.
    """
    code = Attribute(
        """A code which indicates success and payment state or error
            - PAYED
            - NOT_PAYED
            - ERROR""")
        
    message = Attribute(
        """Message which should be displayed to the user.""")