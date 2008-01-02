# zope imports
from zope.component import adapter

# easyshop imports
from easyshop.core.interfaces import IShop
from easyshop.shop.events import IShopCreatedEvent

@adapter(IShop, IShopCreatedEvent)
def createContainers(shop, event):
    """
    """
    shop.manage_addProduct["easyshop.shop"].addProductsContainer(
        id="products",
        title="Products")

    shop.manage_addProduct["easyshop.shop"].addCategoriesContainer(
        id="categories",
        title="Categories")

    shop.products.reindexObject()
    shop.categories.reindexObject()
