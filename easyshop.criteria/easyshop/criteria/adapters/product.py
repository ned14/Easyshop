# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import ICartItem
from easyshop.core.interfaces import IProductCriteria
from easyshop.core.interfaces import IValidity

class ProductCriteriaValidity:
    """Adapter which provides IValidity for product criteria content objects.
    """    
    implements(IValidity)
    adapts(IProductCriteria)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def isValid(self, object):
        """Returns True, if the given object is selected product of the
        criterion.
        """
        if ICartItem.providedBy(object):
            object = object.getProduct()        
                        
        if object.getId() in self.context.getProducts():
            return True
        return False

