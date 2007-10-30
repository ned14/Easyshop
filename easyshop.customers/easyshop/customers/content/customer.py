# Zope imports
from AccessControl import ClassSecurityInfo

# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# CMFCore imports
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.permissions import SetOwnPassword
from Products.CMFCore.permissions import ManageUsers

# membrane imports
# from Products.membrane.interfaces import IUserAuthProvider

# easyshop imports
from easyshop.core.config import *
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICustomer
from easyshop.core.interfaces import IPaymentManagement
from easyshop.core.interfaces import IShippingManagement
from easyshop.core.interfaces import IShopManagement

schema = Schema((

    StringField('id',
        languageIndependent=True,
        required=True,
        write_permission=ManageUsers,
        widget=StringWidget(
            label=u'User name',
            label_msgid='schema_user_name_label',
            description=u"Please select a username.",
            description_msgid="schema_user_name_description",
            i18n_domain='EasyShop',            
        ),
    ),

    StringField(
        name='title',
        widget=StringWidget(
            visible={'edit':'invisible', 'view':'invisible'},
        ),
        required=0,        
        schemata="default"
    ),

    StringField(
        name='phone',
        widget=StringWidget(
        schemata="name",
            label_msgid='schema_phone_label',
            i18n_domain='EasyShop',
        ),
        schemata="name",
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
    schema = BaseFolderSchema.copy() + schema.copy()
    
    def Title(self):
        """
        """
        return self.getId()
        
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