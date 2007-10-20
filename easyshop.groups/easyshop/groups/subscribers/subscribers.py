# zope imports
from zope.component import adapter
from Products.Archetypes.interfaces import IObjectInitializedEvent

# EasyShop imports
from Products.EasyShop.interfaces import IShop

@adapter(IShop, IObjectInitializedEvent)
def createContainers(shop, event):
    """
    """
    shop.manage_addProduct["EasyShop"].addGroupsContainer(
        id="groups",
        title="Groups")        
        
    shop.groups.reindexObject()