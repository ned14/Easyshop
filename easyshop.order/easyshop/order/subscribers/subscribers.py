# zope imports
from zope.component import adapter
from Products.Archetypes.interfaces import IObjectInitializedEvent

# easyshop imports
from easyshop.core.interfaces import IShop

@adapter(IShop, IObjectInitializedEvent)
def createContainers(shop, event):
    """
    """
    shop.manage_addProduct["easyshop.shop"].addOrdersContainer(
        id="orders",
        title="Orders")

    # TODO: Should be done with workflow
    shop.orders.manage_permission(
        'Add portal content',
        ['Member'], 1)
        
    shop.orders.reindexObject()
