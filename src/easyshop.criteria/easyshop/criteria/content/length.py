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
from easyshop.core.interfaces import ILengthCriteria

schema = Schema((
    FloatField(
        name='length',
        default=0.0,
        widget=DecimalWidget(
            label="Length",
            label_msgid="schema_length_label",
            description = "The most length of the products of the cart",
            description_msgid="schema_length_description",
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

class LengthCriteria(BaseContent):
    """
    """
    implements(ILengthCriteria)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = BaseSchema.copy() + schema.copy()

    def Title(self):
        """
        """
        return "Length"
        
    def getValue(self):
        """
        """
        return "%s%s" % (self.getOperator(), self.getLength())
        
registerType(LengthCriteria, PROJECTNAME)
