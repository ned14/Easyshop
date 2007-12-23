# zope imports
from zope.interface import implements

# Zope imports
from AccessControl import ClassSecurityInfo

# Archetypes imports
from Products.Archetypes.atapi import *

# easyshop imports
from easyshop.core.config import PROJECTNAME
from easyshop.core.interfaces import IProductAmountCriteria

schema = Schema((
    FloatField(
        name='amount',
        default=0.0,
        widget=DecimalWidget(
            label="Amount of Products",
            label_msgid="schema_amount_of_products_label",
            description = "The amount of same products",
            description_msgid="schema_amount_of_products_description",
            i18n_domain="EasyShop",
        ),
    ),    
),
)

class ProductAmountCriteria(BaseContent):
    """
    """
    implements(IProductAmountCriteria)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = BaseSchema.copy() + schema.copy()

    def Title(self):
        """
        """
        return "Amount Of Products"
        
    def getValue(self):
        """
        """
        return self.getAmount()
        
registerType(WeightCriteria, PROJECTNAME)
