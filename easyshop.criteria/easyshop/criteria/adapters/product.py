# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import IValidity
from easyshop.core.interfaces import IProductCriteria

class ProductCriteriaValidity:
    """Adapter which provides IValidity for product criteria content objects.
    """    
    implements(IValidity)
    adapts(IProductCriteria)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def isValid(self, product):
        """Returns True, if the given product is selected product.
        """
        if product.getId() in self.context.getProducts():
            return True
        return False

