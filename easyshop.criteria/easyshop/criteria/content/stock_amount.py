# zope imports
import transaction
from zope.interface import implements

# Zope imports
from AccessControl import ClassSecurityInfo

# Archetypes imports
from Products.Archetypes.atapi import *

# easyshop imports
from easyshop.core.config import *
from easyshop.core.interfaces import IStockAmountCriteria

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

    FloatField(
        name='amount',
        widget=DecimalWidget(
            label="Amount",
            label_msgid="schema_amount_label",
            description="The criteria is True if the stock amount of the product is equal or less than the entered amount.",
            description_msgid="schema_amount_description",            
            i18n_domain="EasyShop",
        ),
    ),
    
),
)

class StockAmountCriteria(BaseContent):
    """
    """
    implements(IStockAmountCriteria)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = BaseSchema.copy() + schema.copy()

    def Title(self):
        """
        """
        return "Stock Amount Criteria"
        
    def getValue(self):
        """
        """
        return self.getAmount()
        
    def _renameAfterCreation(self, check_auto_id=False):
        """Overwritten to set the default value for id
        """
        transaction.commit()
        new_id = "Stock Amount Criteria"
        self.setId(new_id)

registerType(StockAmountCriteria, PROJECTNAME)