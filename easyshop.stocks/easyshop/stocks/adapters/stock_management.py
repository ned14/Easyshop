# zope imports
from zope.component import adapts
from zope.interface import implements

# easyshop imports
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IShop
from easyshop.core.interfaces import IStockManagement
from easyshop.core.interfaces import IValidity

class StockManagement:
    """Adapter which provides IStockManagement for shop content objects.
    """
    implements(IStockManagement)
    adapts(IShop)
    
    def __init__(self, context):
        """
        """
        self.context     = context
        self.stock_rules = context["stock-rules"]

    def removeCart(self, cart):
        """
        """
        for cart_item in IItemManagement(cart).getItems():
            product = cart_item.getProduct()
            amount  = cart_item.getAmount()
            
            new_amount = product.getStockAmount() - amount
            product.setStockAmount(new_amount)
        
    def getStockRules(self):
        """
        """
        return self.stock_rules.objectValues()
        
    def getValidStockRuleFor(self, product):
        """
        """
        for rule in self.stock_rules.objectValues():
            if IValidity(rule).isValid(product) == True:
                return rule

        return None