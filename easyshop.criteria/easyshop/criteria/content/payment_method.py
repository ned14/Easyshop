# zope imports
import transaction
from zope.interface import implements

# Zope imports
from AccessControl import ClassSecurityInfo

# Archetypes imports
from Products.Archetypes.atapi import *

# easyshop imports
from easyshop.core.config import *
from easyshop.core.interfaces import IPaymentMethodCriteria
from easyshop.core.interfaces import IPaymentMethodManagement
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
        name='paymentMethods',
        widget=MultiSelectionWidget(
            label='Payment Methods',
            label_msgid='schema_payment_methods_label',
            i18n_domain='EasyShop',
        ),
        multiValued=1,
        vocabulary="_getPaymentMethodsAsDL"
    ),

),
)

class PaymentMethodCriteria(BaseContent):
    """
    """
    implements(IPaymentMethodCriteria)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = BaseSchema.copy() + schema.copy()

    def Title(self):
        """
        """
        return "Payment Method"

    def getValue(self):
        """
        """
        return ", ".join(self.getPaymentMethods())
    
    def _getPaymentMethodsAsDL(self):
        """Returns all payment methods as DisplayList.
        """
        dl = DisplayList()        
        shop = IShopManagement(self).getShop()
        for method in IPaymentMethodManagement(shop).getPaymentMethods():
            dl.add(method.getId(), method.Title())

        return dl

    def _renameAfterCreation(self, check_auto_id=False):
        """Overwritten to set the default value for id.
        """
        transaction.commit()
        new_id = "PaymentMethodCriteria"
        self.setId(new_id)
        
registerType(PaymentMethodCriteria, PROJECTNAME)