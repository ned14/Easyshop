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
from easyshop.core.interfaces import IWeightCriteria

schema = Schema((
    FloatField(
        name='weight',
        default=0.0,
        widget=DecimalWidget(
            label="Weight",
            label_msgid="schema_weight_label",
            description = "The weight of the cart",
            description_msgid="schema_weight_description",
            i18n_domain="EasyShop",
        ),
    ),    
),
)

class WeightCriteria(BaseContent):
    """
    """
    implements(IWeightCriteria)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = BaseSchema.copy() + schema.copy()

    def Title(self):
        """
        """
        return "Weight"
        
    def getValue(self):
        """
        """
        return self.getWeight()
        
registerType(WeightCriteria, PROJECTNAME)
