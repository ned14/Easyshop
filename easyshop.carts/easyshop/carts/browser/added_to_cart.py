# Five imports
from Products.Five.browser import BrowserView

# ATCT imports
from Products.ATContentTypes.config import HAS_LINGUA_PLONE

# Easyshop imports
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IPhotoManagement
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IPropertyManagement

class AddedToCartView(BrowserView):
    """
    """
    def getProduct(self):
        """Returns the last input product of the cart.
        """
        cart = ICartManagement(self.context).getCart()

        try:
            cart_item = IItemManagement(cart).getItems()[-1]
        except IndexError:
            return []

        # Get product
        product = cart_item.getProduct()
                        
        # Price
        price = IPrices(cart_item).getPriceForCustomer()
        cm    = ICurrencyManagement(self.context)
        price = cm.priceToString(price)        
        
        # Get selected properties
        properties = []
        pm = IPropertyManagement(product)

        for selected_property in cart_item.getProperties():
            property_price = pm.getPriceForCustomer(
                selected_property["id"], 
                selected_property["selected_option"]) 

            # This could happen if a property is deleted and there are 
            # still product with this selected property in the cart.
            # Todo: Think about, whether theses properties are not to 
            # display. See also checkout_order_preview
            try:    
                property_title = pm.getProperty(
                    selected_property["id"]).Title()
            except AttributeError:
                property_title = selected_property["id"]
            
            properties.append({
                "id" : selected_property["id"],
                "selected_option" : selected_property["selected_option"],
                "title" : property_title,
                "price" : cm.priceToString(property_price)
            })

        # NOTE: Change to translation
        if HAS_LINGUA_PLONE:
            product = product.getTranslation()

        # Photo
        photo = IPhotoManagement(product).getMainPhoto()
        if photo is not None:
            image_url = photo.absolute_url()
        else:
            image_url = None
                                    
        return {
            "title"      : product.Title(),
            "url"        : product.absolute_url(),
            "price"      : price,
            "image_url"  : image_url,
            "properties" : properties,
        }