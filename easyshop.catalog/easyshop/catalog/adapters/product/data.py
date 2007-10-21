# zope imports
from zope.interface import implements
from zope.component import adapts

# EasyShop imports
from Products.EasyShop.interfaces import IData
from Products.EasyShop.interfaces import ICurrencyManagement
from Products.EasyShop.interfaces import IPhotoManagement
from Products.EasyShop.interfaces import IPrices
from Products.EasyShop.interfaces import IProduct
from Products.EasyShop.interfaces import IPropertyManagement

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

        # properties view
        property_manager = IPropertyManagement(self.context)
        if len(property_manager.getProperties()) > 0:
            showSelectPropertiesView = True
        else:    
            showSelectPropertiesView = False

        # photo
        photo = IPhotoManagement(self.context).getMainPhoto()
        if photo is not None:
            image = "%s/image_%s" % (photo.absolute_url(), "preview")
        else:
            image = None
              
        return {
            "title"       : self.context.Title(),
            "short_title" : self.context.getShortTitle() or self.context.Title(),
            "url"         : self.context.absolute_url(),
            "price"       : price,
            "image"       : image,
            "text"        : self.context.getText(),
            "showSelectPropertiesView" : showSelectPropertiesView,
        }        