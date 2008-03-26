# zope imports
from zope.interface import Interface
from zope.interface import Attribute
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
        description=_(u"Please enter your firstname."),
        default=u'',
        required=True,
    )

    lastname = schema.TextLine(
        title=_(u'Lastname'),
        description=_(u"Please enter your lastname."),
        default=u'',
        required=True,
    )

    company_name = schema.TextLine(
        title=_(u'Company Name'),
        description=_(u"Please enter your company name."),
        default=u'',
        required=False,
    )

    address_1 = schema.TextLine(
        title=_(u'Address 1'),
        description=_(u"Please enter your address."),
        default=u'',
        required=True,
    )

    zip_code = schema.TextLine(
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

    email = schema.TextLine(
        title=_(u'E-Mail'),
        description=_(u"Please enter your e-mail address."),
        default=u'',
        required=True,
    )
            
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

    def hasInvoiceAddress():
        """Returns True if a invoice address exists.
        """

    def hasShippingAddress():
        """Returns True if a shipping address exists.
        """
                
################################################################################
# Customers        
################################################################################

class ICustomersContainer(Interface):
    """A marker interface for customer folder content objects.
    """

class ISessionsContainer(Interface):
    """A container which holds addresses for anonymous customers.
    """

class ICustomer(Interface):
    """A customer can buy products from the shop.
    """
    firstname = schema.TextLine(
        title=_(u'Firstname'),
        description=_(u"Please enter your firstname."),
        default=u'',
        required=True,
    )

    lastname = schema.TextLine(
        title=_(u'Lastname'),
        description=_(u"Please enter your lastname."),
        default=u'',
        required=True,
    )

    email = schema.TextLine(
        title=_(u'E-Mail'),
        description=_(u"Please enter your e-mail."),
        default=u'',
        required=True,
    )

    selected_invoice_address  = Attribute("The selected invoice address.")
    selected_shipping_address = Attribute("The selected shipping address.")
    selected_payment_method   = Attribute("The selected payment method.")
    selected_shipping_method  = Attribute("The selected shipping method.")
    
    selected_country = \
        Attribute("""Country which is used to calculate the shipping price, if
                     the customer has not yet entered a invoice address""")

    selected_payment_method = \
        Attribute("""The payment is processed with this method.""")

    selected_payment_information = \
        Attribute("""Some payment methods need additional information (e.g. 
                     Credit Card)""")
                     
class ICustomerManagement(Interface):
    """Provides methods to manage customer content objects.
    """
    def addCustomer():
        """Adds a new customer. Either one for the authenticated member or one 
        for an anonymous user.
        """
        
    def getAuthenticatedCustomer():
       """Returns the current authenticated or session customer.
       """

    def getCustomerById(member_id):
        """Returns customer object for the given member id.
        """    

    def getCustomers():
       """Returns all existing customers for authenticated members.
       """
       
    def transformCustomer(mid, sid):
        """Transforms a session customer with the given session id (sid) to a 
        personalized customer with the given member id (mid)
        """