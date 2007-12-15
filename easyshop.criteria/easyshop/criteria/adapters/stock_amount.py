# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import IValidity
from easyshop.core.interfaces import IStockAmountCriteria

class StockAmountCriteriaValidity:
    """Adapter which provides IValidity for stock amount content objects.
    """
    implements(IValidity)
    adapts(IStockAmountCriteria)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def isValid(self, product):
        """Returns True, if the stock amount of the product is equal or less then
        entered criteria stock amount.
        """
        if product.getStockAmount() <= self.context.getAmount():
            return True
        else:
            return False
