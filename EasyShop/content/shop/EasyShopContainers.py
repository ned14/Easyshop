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
from Products.EasyShop.interfaces import ICustomersContainer
from Products.EasyShop.interfaces import IGroupsContainer
from Products.EasyShop.interfaces import IOrdersContainer
from Products.EasyShop.interfaces import IPaymentMethodsContainer
from Products.EasyShop.interfaces import IPaymentPricesContainer

class EasyShopGroups(OrderedBaseFolder):
    """A simple container to hold groups.
    """    
    implements(IGroupsContainer)

class EasyShopOrders(BaseBTreeFolder):
    """A simple container to hold orders.
    """
    implements(IOrdersContainer)
                 
class EasyShopCustomers(BaseBTreeFolder):
    """A simple container to hold customers.
    """
    implements(ICustomersContainer)        

registerType(EasyShopCustomers, PROJECTNAME)
registerType(EasyShopGroups, PROJECTNAME)
registerType(EasyShopOrders, PROJECTNAME)