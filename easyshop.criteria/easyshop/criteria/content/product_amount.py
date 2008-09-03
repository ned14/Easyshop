# zope imports
from zope.interface import implements

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

schema = BaseSchema.copy() + schema.copy()
schema["title"].required = False
schema["title"].visible  = {'edit':'invisible', 'view':'invisible'}

class ProductAmountCriteria(BaseContent):
    """
    """
    implements(IProductAmountCriteria)
    _at_rename_after_creation = True
    schema = schema

    def Title(self):
        """
        """
        return "Amount Of Products"
        
    def getValue(self):
        """
        """
        return self.getAmount()
        
registerType(ProductAmountCriteria, PROJECTNAME)