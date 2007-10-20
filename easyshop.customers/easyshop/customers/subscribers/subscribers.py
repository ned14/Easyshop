# zope imports
from zope.component import adapter
from Products.Archetypes.interfaces import IObjectInitializedEvent

# EasyShop imports
from Products.EasyShop.interfaces import IShop

@adapter(IShop, IObjectInitializedEvent)
def createContainer(shop, event):
    """
    """
    shop.manage_addProduct["EasyShop"].addCustomersContainer(
        id="customers", 
        title="Customers")    

    # TODO: Should be done with workflow
    shop.customers.manage_permission(
        'Modify portal content',
        ['Owner'], 1)
        
    shop.customers.reindexObject()