# zope imports
from zope.component import adapter
from easyshop.shop.events import IShopCreatedEvent

# easyshop imports
from easyshop.core.interfaces import IShop

@adapter(IShop, IShopCreatedEvent)
def createContainers(shop, event):
    """
    """
    shop.manage_addProduct["easyshop.shop"].addStockInformationContainer(
        id="stock-information", 
        title="Stock Information")    
        
    shop["stock-information"].reindexObject()