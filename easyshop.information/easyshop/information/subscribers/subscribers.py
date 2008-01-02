# zope imports
from zope.component import adapter
from easyshop.shop.events import IShopCreatedEvent

# easyshop imports
from easyshop.core.interfaces import IShop

@adapter(IShop, IShopCreatedEvent)
def createInformation(shop, event):
    """
    """
    shop.manage_addProduct["easyshop.shop"].addInformationContainer(
        id="information", 
        title="Information")
        
    shop.information.manage_addProduct["easyshop.shop"].addInformationPage(
        id="terms-and-conditions",
        title="Terms And Conditions")
        
    shop.information.reindexObject()
