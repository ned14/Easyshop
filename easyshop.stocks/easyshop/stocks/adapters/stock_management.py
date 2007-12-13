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
        self.context = context
        self.stock_information = context["stock-information"]

    def removeCart(self, cart):
        """
        """
        for cart_item in IItemManagement(cart).getItems():
            product = cart_item.getProduct()
            amount  = cart_item.getAmount()
            
            new_amount = product.getStockAmount() - amount
            product.setStockAmount(new_amount)
        
    def getStockInformation(self):
        """
        """
        return self.stock_information.objectValues()
        
    def getValidStockInformationFor(self, product):
        """
        """
        for information in self.stock_information.objectValues():
            if IValidity(information).isValid(product) == True:
                return information

        return None