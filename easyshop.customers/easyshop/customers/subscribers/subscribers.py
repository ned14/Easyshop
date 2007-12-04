# zope imports
from zope.component import adapter
from Products.Archetypes.interfaces import IObjectInitializedEvent

# easyshop imports
from easyshop.core.interfaces import IShop

@adapter(IShop, IObjectInitializedEvent)
def createContainer(shop, event):
    """
    """
    shop.manage_addProduct["easyshop.shop"].addCustomersContainer(
        id="customers", 
        title="Customers")    
    shop.customers.reindexObject()
    
    shop.manage_addProduct["easyshop.shop"].addSessionsContainer(
        id="sessions", 
        title="Sessions")        
    shop.sessions.reindexObject()