# zope imports
from zope.component import adapter
from easyshop.shop.events import IShopCreatedEvent

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import IShop

@adapter(IShop, IShopCreatedEvent)
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

    # Publish all payment methods by default
    wftool = getToolByName(shop, "portal_workflow")
    for shipping_method in shop.shippingmethods.objectValues():
        wftool.doActionFor(shipping_method, "publish")
        
    shop.shippingmethods.reindexObject()
    shop.shippingprices.reindexObject()
