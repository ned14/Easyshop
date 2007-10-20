# Zope imports
import zope
from AccessControl import ClassSecurityInfo

# Archetypes imports
from Products.Archetypes.atapi import *

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports
from Products.EasyShop.interfaces import IShop
from Products.EasyShop.config import *

class EasyShopBase:
    """BaseClass
    """
    security = ClassSecurityInfo()
    schema = BaseBTreeFolderSchema.copy()

    def getShop(self):
        """
        """
        object = self
        try:
            while object.meta_type != "EasyShop":
                if object.meta_type == "Plone Factory Tool":
                    object = object.aq_parent
                else:
                    object = object.aq_inner.aq_parent
        except AttributeError:

            # Next line is needed for the temporary products for payment and
            # shipping. As they have real context above code seems not to
            # work. But they have given the shop as context so we can give
            # it back here. See also:
            # - adapters/shop/payment/createTemporaryPaymentProduct
            # - adapters/shop/shipping/createTemporaryShippingProduct.            
            # I'm not sure whether this is clean, I assume it is not.
            
            if IShop.providedBy(self.context):
                return self.context
            else:
                return None
        return object