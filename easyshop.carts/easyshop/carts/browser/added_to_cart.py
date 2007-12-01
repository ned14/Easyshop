# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# Easyshop imports
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import IPhotoManagement
from easyshop.core.interfaces import IPrices

class AddedToCartView(BrowserView):
    """
    """
    def getProduct(self):
        """Returns the last input product of the cart.
        """
        uid = self.request.get("uid", None)
        if uid is None:
            return []
            
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            UID = uid
        )
        
        try:
            product = brains[0].getObject()
        except IndexError:
            return []

        # Price
        price = IPrices(product).getPriceForCustomer()
        cm    = ICurrencyManagement(self.context)
        price = cm.priceToString(price)        
        
        # Photo
        photo = IPhotoManagement(product).getMainPhoto()
        if photo is not None:
            image_url = photo.absolute_url()
        else:
            image_url = None
        
        return {
            "title"     : product.Title(),
            "url"       : product.absolute_url(),
            "price"     : price,
            "image_url" : image_url,
        }