# Zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.folder import ATBTreeFolder
from Products.ATContentTypes.content.folder import ATFolder

# EasyShop imports
from Products.EasyShop.config import *
from Products.EasyShop.content.shop import EasyShopBase
from Products.EasyShop.interfaces import ICartsFolderContent
from Products.EasyShop.interfaces import ICategoryFolderContent
from Products.EasyShop.interfaces import ICustomerFolderContent
from Products.EasyShop.interfaces import IGroupFolderContent
from Products.EasyShop.interfaces import IOrderFolderContent
from Products.EasyShop.interfaces import IPaymentMethodsFolderContent
from Products.EasyShop.interfaces import IPaymentPricesFolderContent
from Products.EasyShop.interfaces import IProductFolderContent
from Products.EasyShop.interfaces import IShippingPricesFolderContent
from Products.EasyShop.interfaces import IShippingMethodsFolderContent
from Products.EasyShop.interfaces import ITaxFolderContent

class EasyShopProducts(BaseBTreeFolder, EasyShopBase):
    """A container to hold products.
    """
    implements(IProductFolderContent)

class EasyShopPaymentMethods(OrderedBaseFolder, EasyShopBase):
    """A simple container to hold payment methods.
    """
    implements(IPaymentMethodsFolderContent)

class EasyShopPaymentPrices(OrderedBaseFolder, EasyShopBase):
    """A simple container to hold payment prices.
    """
    implements(IPaymentPricesFolderContent)

class EasyShopShippingMethods(OrderedBaseFolder, EasyShopBase):
    """A simple container to hold shipping methods.
    """
    implements(IShippingMethodsFolderContent)

class EasyShopShippingPrices(OrderedBaseFolder, EasyShopBase):
    """A simple container to hold shipping prices.
    """
    implements(IShippingPricesFolderContent)
                  
class EasyShopCategories(OrderedBaseFolder, EasyShopBase):
    """A simple container to hold categories.
    """
    implements(ICategoryFolderContent)

class EasyShopGroups(OrderedBaseFolder, EasyShopBase):
    """A simple container to hold groups.
    """    
    implements(IGroupFolderContent)

class EasyShopTaxes(OrderedBaseFolder, EasyShopBase):
    """A simple container to hold taxes.
    """
    implements(ITaxFolderContent)

class EasyShopOrders(BaseBTreeFolder, EasyShopBase):
    """A simple container to hold orders.
    """
    implements(IOrderFolderContent)
                 
class EasyShopCustomers(BaseBTreeFolder, EasyShopBase):
    """A simple container to hold customers.
    """
    implements(ICustomerFolderContent)        

registerType(EasyShopCategories, PROJECTNAME)
registerType(EasyShopCustomers, PROJECTNAME)
registerType(EasyShopGroups, PROJECTNAME)
registerType(EasyShopOrders, PROJECTNAME)
registerType(EasyShopPaymentMethods, PROJECTNAME)
registerType(EasyShopPaymentPrices, PROJECTNAME)
registerType(EasyShopProducts, PROJECTNAME)
registerType(EasyShopShippingPrices, PROJECTNAME)     
registerType(EasyShopShippingMethods, PROJECTNAME)
registerType(EasyShopTaxes, PROJECTNAME)
