# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import IData
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import IImageManagement
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IProduct

class ProductData:
    """An adapter which provides IData for product content objects.
    """    
    implements(IData)
    adapts(IProduct)

    def __init__(self, context):
        """
        """
        self.context = context
    
    def asDict(self):
        """
        """
        # price
        cm    = ICurrencyManagement(self.context)
        price = IPrices(self.context).getPriceForCustomer()
        price = cm.priceToString(price)

        # image
        image = IImageManagement(self.context).getMainImage()
        if image is not None:
            image = "%s/image_%s" % (image.absolute_url(), "preview")
        else:
            image = None
              
        return {
            "title"       : self.context.Title(),
            "short_title" : self.context.getShortTitle() or self.context.Title(),
            "url"         : self.context.absolute_url(),
            "price"       : price,
            "image"       : image,
            "text"        : self.context.getText(),
        }        