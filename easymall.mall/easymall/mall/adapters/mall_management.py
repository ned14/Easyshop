# zope imports
from zope.interface import implements
from zope.interface import Interface
from zope.component import adapts
  
# easyshop imports
from easymall.mall.interfaces import IMall
from easymall.mall.interfaces import IMallManagement

class MallManagement:
    """Provides IShopManagement for arbitrary objects.
    """
    implements(IMallManagement)
    adapts(Interface)

    def __init__(self, context):
        """
        """
        self.context = context

    def getMall(self):
        """
        """
        object = self.context
        try:
            while object.meta_type != "EasyMall":
                if object.meta_type == "Plone Factory Tool":
                    object = object.aq_parent
                else:
                    object = object.aq_inner.aq_parent
        except AttributeError:

            # Next line is needed for the temporary products for payment and
            # shipping. As they have no real context above code seems not to
            # work. But they have given the shop as context so we can give
            # it back here. See also:
            # - adapters/shop/payment/createTemporaryPaymentProduct
            # - adapters/shop/shipping/createTemporaryShippingProduct.            
            # I'm not sure whether this is clean, I assume it is not.
            
            if IMall.providedBy(object.context):
                return object.context
            else:
                return None
        return object