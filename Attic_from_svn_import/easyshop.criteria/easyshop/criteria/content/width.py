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
from easyshop.core.interfaces import IWidthCriteria

schema = Schema((
    FloatField(
        name='width',
        default=0.0,
        widget=DecimalWidget(
            label="Width",
            label_msgid="schema_width_label",
            description = "The most width product of the cart",
            description_msgid="schema_width_description",
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

class WidthCriteria(BaseContent):
    """
    """
    implements(IWidthCriteria)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = BaseSchema.copy() + schema.copy()

    def Title(self):
        """
        """
        return "Width"
        
    def getValue(self):
        """
        """
        return "%s%s" % (self.getOperator(), self.getWidth())
        
registerType(WidthCriteria, PROJECTNAME)
