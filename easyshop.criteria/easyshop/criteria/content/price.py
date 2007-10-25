# zope imports
from zope.interface import implements

# Zope imports
from DateTime import DateTime
from AccessControl import ClassSecurityInfo

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# Archetypes imports
from Products.Archetypes.atapi import *

# easyshop imports
from easyshop.core.config import *
from easyshop.core.interfaces import IPriceCriteria


schema = Schema((
    FloatField(
        name='price',
        default=0.0,
        widget=DecimalWidget(
            label='Price Gross',
            label_msgid='schema_value_label',
            i18n_domain='EasyShop',
        ),
    ),

),
)

class PriceCriteria(BaseContent):
    """
    """
    implements(IPriceCriteria)    
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = BaseSchema.copy() + schema.copy()

    def Title(self):
        """
        """
        return "Price"
        
    def getValue(self):
        """
        """
        return self.getPrice()

registerType(PriceCriteria, PROJECTNAME)
