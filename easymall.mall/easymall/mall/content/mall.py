# Zope imports
from zope.interface import alsoProvides
from zope.interface import implements
from zope.component import getUtility
from zope.component import getMultiAdapter

# Archetypes imports
from Products.Archetypes.atapi import *

# ATContentTypes imports
from Products.ATContentTypes.content.folder import ATFolder

# plone.portlets imports
from plone.portlets.constants import CONTEXT_CATEGORY
from plone.portlets.interfaces import ILocalPortletAssignmentManager
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager

# easyshop imports
from easyshop.core.config import *
from easyshop.core.interfaces import IShop
from easyshop.core.interfaces import IImageConversion

from easyshop.catalog.portlets import categories
from easyshop.catalog.portlets import formatter
from easyshop.shop.portlets import admin
from easyshop.shop.content.shop import EasyShop

from easyshop.carts.portlets import cart
from easyshop.customers.portlets import my_account

# easyshop imports
from easymall.mall.config import *
from easymall.mall.interfaces import IMall

schema = EasyShop.schema.copy()
    
class EasyMall(ATFolder):
    """A mall holds several shops.
    """
    implements(IMall)
    _at_rename_after_creation = True
    schema = schema

    def at_post_create_script(self):
        """Overwritten to create some objects.
        """
        # Add right portlets 
        rightColumn = getUtility(IPortletManager, name=u'plone.rightcolumn', context=self)
        right = getMultiAdapter((self, rightColumn,), IPortletAssignmentMapping, context=self)

        if u'portlets.Formatter' not in right:
            right[u'portlets.Formatter'] = formatter.Assignment()
            order = [right.keys()[-1]]+right.keys()[:-1]
            right.updateOrder(list(order))

        if u'portlets.Cart' not in right:
            right[u'portlets.Cart'] = cart.Assignment()
            order = [right.keys()[-1]]+right.keys()[:-1]
            right.updateOrder(list(order))

        if u'portlets.MyAccount' not in right:
            right[u'portlets.MyAccount'] = my_account.Assignment()
            order = [right.keys()[-1]]+right.keys()[:-1]
            right.updateOrder(list(order))

        # Block default portlets
        assignable = getMultiAdapter((self, rightColumn,), ILocalPortletAssignmentManager)
        assignable.setBlacklistStatus(CONTEXT_CATEGORY, True)
        
    def _getCurrenciesAsDL(self):
        """
        """
        dl = DisplayList()
        
        keys = CURRENCIES.keys()
        keys.sort()
        
        for key in keys:
            dl.add(key, CURRENCIES[key]["long"])

        return dl
                
registerType(EasyMall, PROJECTNAME)