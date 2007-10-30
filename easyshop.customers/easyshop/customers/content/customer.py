# Zope imports
from AccessControl import ClassSecurityInfo

# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.config import *
from easyshop.core.interfaces import ICustomer
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import IPaymentManagement
from easyshop.core.interfaces import IShippingManagement
from easyshop.core.interfaces import IShopManagement

schema = Schema((

    StringField(
        name="firstname",
        widget=StringWidget(
            label="Firstname",
            label_msgid="schema_firstname_label",
            description = "",
            description_msgid = "schema_firstname_description",
            i18n_domain="EasyShop",
        ),
    ),

    StringField(
        name="lastname",
        widget=StringWidget(
            label="Lastname",
            label_msgid="schema_lastname_label",
            description = "",
            description_msgid = "schema_lastname_description",
            i18n_domain="EasyShop",
        ),
    ),

    StringField(
        name="email",
        widget=StringWidget(
            label="E-mail",
            label_msgid="schema_email_label",
            description = "",
            description_msgid = "schema_email_description",
            i18n_domain="EasyShop",
        ),
    ),
    
    StringField(
        name='invoiceAddressAsString',
        default="default",
        widget=SelectionWidget(
            format = "select",          
            label="Invoice Address",
            label_msgid='schema_invoice_address_label',
            i18n_domain='EasyShop',
        ),
        schemata="address",
        vocabulary="_getAddressesAsDL"
    ),

    StringField(
        name='shippingAddressAsString',
        default="default",
        widget=SelectionWidget(
            format = "select",
            label="Shipping Address",
            label_msgid='schema_shipping_address_label',
            i18n_domain='EasyShop',
        ),
        schemata="address",
        vocabulary="_getAddressesAsDL"
    ),

    StringField(
        name='selectedPaymentMethod',
        widget=SelectionWidget(
            format = "select",          
            label="Payment Method",
            label_msgid='schema_selected_payment_method_label',
            i18n_domain='EasyShop',
        ),
        schemata="payment",
        vocabulary="_getPaymentMethodsAsDL"
    ),

    StringField(
        name='selectedShippingMethod',
        widget=SelectionWidget(
            format = "select",          
            label="Shipping Method",
            label_msgid='schema_selected_shipping_method_label',
            i18n_domain='EasyShop',
        ),
        schemata="shipping",
        vocabulary="_getShippingMethodsAsDL"
    ),

),
)

schema = BaseFolderSchema.copy() + schema.copy()
schema["title"].widget.visible = {'view':'invisible', 'edit':'invisible'}

class Customer(BaseFolder):
    """A customer can buy products from a shop. A customer has addresses and 
    payment methods. 

    A customer exists additionally to the members of Plone.  Whenever a
    member wants to buy something a customer content object is added for
    this member. This is intended to be changed to use remember in future.
    """    
    implements(ICustomer)    
    security = ClassSecurityInfo()
    _at_rename_after_creation = False
    schema = schema
    
    def Title(self):
        """
        """
        if self.getFirstname() and self.getLastname():
            return self.getFirstname() + " " + self.getLastname()
        else:
            return self.getId()

    def SearchableText(self):
        """
        """
        text = []
        
        text.append(self.getFirstname())
        text.append(self.getLastname())
        text.append(self.getEmail())
        
        am = IAddressManagement(self)
        for address in am.getAddresses():
            text.append(address.getFirstname())
            text.append(address.getLastname())
            text.append(address.getAddress1())
            text.append(address.getZipCode())            
            text.append(address.getCity())
            text.append(address.getCountry())
                        
        return " ".join(text)
        
    def _getAddressesAsDL(self):
        """Returns all addresses as DisplayList.
        """
        dl = DisplayList()

        am = IAddressManagement(self)
        for address in am.getAddresses():
            dl.add(address.getId(), address.getName() + " - " + address.getAddress1())

        return dl

    def _getShippingMethodsAsDL(self):
        """Returns all shipping methods as DisplayList.
        """
        dl = DisplayList()

        pm = IShippingManagement(IShopManagement(self).getShop())
        for shipping_method in pm.getShippingMethods():
            dl.add(shipping_method.getId(), shipping_method.Title())

        return dl

    def _getPaymentMethodsAsDL(self):
        """Returns all payment methods as DisplayList.
        """
        dl = DisplayList()

        pm = IPaymentManagement(IShopManagement(self).getShop())
        for payment_method in pm.getPaymentMethods():
            dl.add(payment_method.getId(), payment_method.Title())

        return dl
    
registerType(Customer, PROJECTNAME)