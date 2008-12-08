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
    
    StringField(
        name="operator",
        vocabulary=["current", "not valid"],
        default="current",   
        widget=SelectionWidget(
            label="Operator",
            label_msgid="_operator_label",
            description = "",
            description_msgid = "_operator_description",
            i18n_domain="",        
        ),
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

    def getValue(self):
        """
        """
        value = "%s: " % self.getOperator()
        value +=  ", ".join(self.getShippingMethods())

        return value

    def _getShippingMethodsAsDL(self):
        """Returns all payment methods as DisplayList
        """
        dl = DisplayList()
        
        shop = IShopManagement(self).getShop()
        sm = IShippingMethodManagement(shop)
        
        for shipping_method in sm.getShippingMethods():
            # Don't display the parent shipping method
            if shipping_method == self.aq_parent:
                continue
            dl.add(shipping_method.getId(), shipping_method.Title())

        return dl

registerType(ShippingMethodCriteria, PROJECTNAME)