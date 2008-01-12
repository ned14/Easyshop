# Five imports
from Products.Five.browser import BrowserView

# Easyshop imports
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IImageManagement
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
                
        # Price
        price = IPrices(cart_item).getPriceForCustomer()
        cm    = ICurrencyManagement(self.context)
        price = cm.priceToString(price)        
        
        # Image
        product = cart_item.getProduct()
        image = IImageManagement(product).getMainImage()
        if image is not None:
            image_url = image.absolute_url()
        else:
            image_url = None
        
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
                        
        return {
            "title"      : product.Title(),
            "url"        : product.absolute_url(),
            "price"      : price,
            "image_url"  : image_url,
            "properties" : properties,
        }