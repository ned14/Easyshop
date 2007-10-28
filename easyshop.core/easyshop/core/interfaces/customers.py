# zope imports
from zope.interface import Interface
from zope import schema

# easyshop.core imports
from easyshop.core.config import _

################################################################################
# Address
################################################################################
        
class IAddress(Interface):
    """A address of a customer.
    """
    firstname = schema.TextLine(
        title=_(u'Firstname'),
        description=_(u"Please enter your firstname"),
        default=u'',
        required=True,
    )

    lastname = schema.TextLine(
        title=_(u'Lastname'),
        description=_(u"Please enter your lastname"),
        default=u'',
        required=True,
    )

    companyName = schema.TextLine(
        title=_(u'Company Name'),
        description=_(u"Please enter your company name"),
        default=u'',
        required=False,
    )

    address1 = schema.TextLine(
        title=_(u'Address 1'),
        description=_(u"Please enter your address."),
        default=u'',
        required=True,
    )

    address2 = schema.TextLine(
        title=_(u'Address 2'),
        description=_(u"Please enter your address."),
        default=u'',
        required=False,
    )

    zipCode = schema.TextLine(
        title=_(u'Zip Code'),
        description=_(u"Please enter your zip code."),
        default=u'',
        required=True,
    )

    city = schema.TextLine(
        title=_(u'City'),
        description=_(u"Please enter your city."),
        default=u'',
        required=True,
    )

    country = schema.Choice(
        title=_(u'Country'),
        description=_(u"Please enter your country."),
        vocabulary = "easyshop.countries")
            
    phone = schema.TextLine(
        title=_(u'Phone'),
        description=_(u"Please enter your phone number."),
        default=u'',
        required=False,
    )
    
class IAddressManagement(Interface):
    """Provides methods to manage address content objects.
    """
    def addAddress(a1, a2, z, ci, co):
        """Adds an address.
            
           Parameters:    
               a1 = address 1
               a2 = address 2
               z  = zipcode
               ci = city
               co = country           
        """
        
    def deleteAddress(id):
        """Deletes an address by given id.
        """

    def getAddress(id):
        """Returns address by given id. If it isn't exist returns None.
        """
        
    def getAddresses():
        """Returns all addresses.
        """

    def getEmailAddress():
        """Returns the email address of an customer.
        Which is saved in the corresponding member.
        """
        
    def getInvoiceAddress():
        """Returns the invoice address.
        """

    def getShippingAddress():
        """Returns the shipping address.
        """
        
    def hasAddresses():
        """Returns True if context has at least one address.
        """
        
################################################################################
# Customers        
################################################################################

class ICustomersContainer(Interface):
    """A marker interface for customer folder content objects.
    """

class ICustomer(Interface):
    """A customer can buy products from the shop.
    """
    
class ICustomerManagement(Interface):
    """Provides methods to manage customer content objects.
    """
    def getAuthenticatedCustomer():
       """Returns the current authenticated customer.
       """

    def getCustomerById(id):
        """Returns a customer by given id
        """    

    def getCustomers():
       """
       """

    def hasCustomer(customer):
       """
       """        