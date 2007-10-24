# zope imports
from zope.component import adapter
from Products.Archetypes.interfaces import IObjectInitializedEvent

# easyshop imports
from easyshop.core.interfaces import IShop

@adapter(IShop, IObjectInitializedEvent)
def createContainers(shop, event):
    """
    """
    shop.manage_addProduct["easyshop.shop"].addShippingPricesContainer(
        id="shippingprices", 
        title="Shipping Prices")

    shop.manage_addProduct["easyshop.shop"].addShippingMethodsContainer(
        id="shippingmethods",
        title="Shipping Methods")

    shop.shippingmethods.manage_addProduct["easyshop.shop"].addShippingMethod(
        id="default",
        title="Default")
        
    shop.shippingmethods.reindexObject()
    shop.shippingprices.reindexObject()
