# zope imports
import transaction
from zope.interface import implements

# Zope imports
from DateTime import DateTime
from AccessControl import ClassSecurityInfo

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# Archetypes imports
from Products.Archetypes.atapi import *

# EasyShop imports
from Products.EasyShop.config import *
from Products.EasyShop.interfaces import IPaymentMethodCriteriaContent

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

class EasyShopPaymentMethodCriteria(BaseContent):
    """
    """
    implements(IPaymentMethodCriteriaContent)
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
        """Returns all payment methods as DisplayList
        """
        dl = DisplayList()

        dl.add("directdebit", "Direct Debit")
        dl.add("prepayment", "Prepayment")
        dl.add("cash-on-delivery", "Cash On Delivery")
        dl.add("paypal", "PayPal")
        
        return dl

    def _renameAfterCreation(self, check_auto_id=False):
        """Overwritten to set the default value for id
        """
        transaction.commit()
        new_id = "PaymentMethodCriteria"
        self.setId(new_id)
        
registerType(EasyShopPaymentMethodCriteria, PROJECTNAME)