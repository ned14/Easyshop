# zope imports
from zope.component import adapts
from zope.event import notify
from zope.interface import implements

# easyshop imports
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IShop
from easyshop.core.interfaces import IStockManagement
from easyshop.core.interfaces import IValidity
from easyshop.stocks.events import StockAmountIsZeroEvent

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

    def getStockInformationFor(self, product):
        """
        """        
        for information in self.stock_information.objectValues():
            if IValidity(information).isValid(product) == True:
                return information
        
        return None
        
    def getStockInformations(self):
        """
        """
        return self.stock_information.objectValues()
        
    def removeCart(self, cart):
        """
        """        
        for cart_item in IItemManagement(cart).getItems():
            product = cart_item.getProduct()
            
            # Remove only when product has not unlimited amount
            if product.getUnlimitedAmount() == False:
                amount = cart_item.getAmount()
                new_amount = product.getStockAmount() - amount
                product.setStockAmount(new_amount)
                
                if new_amount <= 0:
                    notify(StockAmountIsZeroEvent(product))