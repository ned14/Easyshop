# zope imports
import transaction
from zope.interface import implements

# Zope imports
from AccessControl import ClassSecurityInfo

# Archetypes imports
from Products.Archetypes.atapi import *

# easyshop imports
from easyshop.core.config import *
from easyshop.core.interfaces import IShippingMethodManagement
from easyshop.core.interfaces import IShippingMethodCriteria
from easyshop.core.interfaces import IShopManagement

schema = Schema((

    StringField(
        name='title',
        widget=StringWidget(
            visible={'edit':'invisible', 'view':'invisible'},
            label='Title',
            label_msgid='schema_title_label',
            i18n_domain='EasyShop',
        ),
        required=0
    ),

    LinesField(
        name='shippingMethods',
        widget=MultiSelectionWidget(
            label='Payment Methods',
            label_msgid='schema_shipping_methods_label',
            i18n_domain='EasyShop',
        ),
        multiValued=1,
        vocabulary="_getShippingMethodsAsDL"
    ),

),
)

class ShippingMethodCriteria(BaseContent):
    """
    """
    implements(IShippingMethodCriteria)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = BaseSchema.copy() + schema.copy()

    def Title(self):
        """
        """
        return "Shipping Method"

    def getValue(self):
        """
        """
        return ", ".join(self.getShippingMethods())

    def _getShippingMethodsAsDL(self):
        """Returns all payment methods as DisplayList
        """
        dl = DisplayList()
        
        shop = IShopManagement(self).getShop()
        sm = IShippingMethodManagement(shop)
        
        for shipping_method in sm.getShippingMethods():
            dl.add(shipping_method.getId(), shipping_method.Title())
        
        return dl

    def _renameAfterCreation(self, check_auto_id=False):
        """Overwritten to set the default value for id
        """
        transaction.commit()
        new_id = "ShippingMethodCriteria"
        self.setId(new_id)
        
registerType(ShippingMethodCriteria, PROJECTNAME)