# zope imports
from zope.component import adapter
from Products.Archetypes.interfaces import IObjectInitializedEvent

# EasyShop imports
from Products.EasyShop.interfaces import IShop

@adapter(IShop, IObjectInitializedEvent)
def createContainers(shop, event):
    """
    """
    shop.manage_addProduct["EasyShop"].addShippingPricesContainer(
        id="shippingprices", 
        title="Shipping Prices")

    shop.manage_addProduct["EasyShop"].addShippingMethodsContainer(
        id="shippingmethods",
        title="Shipping Methods")

    shop.shippingmethods.manage_addProduct["EasyShop"].addShippingMethod(
        id="default",
        title="Default")
        
    shop.shippingmethods.reindexObject()
    shop.shippingprices.reindexObject()
