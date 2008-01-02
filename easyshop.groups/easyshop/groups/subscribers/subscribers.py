# zope imports
from zope.component import adapter
from easyshop.shop.events import IShopCreatedEvent

# easyshop imports
from easyshop.core.interfaces import IShop

@adapter(IShop, IShopCreatedEvent)
def createContainers(shop, event):
    """
    """
    shop.manage_addProduct["easyshop.shop"].addGroupsContainer(
        id="groups",
        title="Groups")        
        
    shop.groups.reindexObject()