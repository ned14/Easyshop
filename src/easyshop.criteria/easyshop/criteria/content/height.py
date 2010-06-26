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
from easyshop.core.interfaces import IHeightCriteria

schema = Schema((
    FloatField(
        name='height',
        default=0.0,
        widget=DecimalWidget(
            label="Height",
            label_msgid="schema_height_label",
            description = "The most height of the products of the cart",
            description_msgid="schema_height_description",
            i18n_domain="EasyShop",
        ),
    ),
    StringField(
        name="operator",
        vocabulary=[">=", "<"], 
        default=">=",
        widget=SelectionWidget(
            label="Operator",
            label_msgid="schema_operator_label",
            description = "Read cart 'operator' Length",
            description_msgid = "schema_operator_description",
            i18n_domain="EasyShop",
        ),
    ),    
),
)

class HeightCriteria(BaseContent):
    """
    """
    implements(IHeightCriteria)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = BaseSchema.copy() + schema.copy()

    def Title(self):
        """
        """
        return "Height"
        
    def getValue(self):
        """
        """
        return "%s%s" % (self.getOperator(), self.getHeight())
        
registerType(HeightCriteria, PROJECTNAME)
