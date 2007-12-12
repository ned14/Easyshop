# zope imports
from zope.component import adapter
from Products.Archetypes.interfaces import IObjectInitializedEvent

# easyshop imports
from easyshop.core.interfaces import IShop

@adapter(IShop, IObjectInitializedEvent)
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
