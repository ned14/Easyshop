# Five imports
from Products.Five.browser import BrowserView

# Easyshop imports
from easyshop.catalog.adapters.property_management import getTitlesByIds
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IImageManagement
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IProductVariant
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

            # Get titles of property and option
            titles = getTitlesByIds(
                product,
                selected_property["id"], 
                selected_property["selected_option"])
                
            if titles is None:
                continue

            if IProductVariant.providedBy(product) == True:
                show_price = False
            else:
                show_price = True
                
            properties.append({
                "id" : selected_property["id"],
                "selected_option" : titles["option"],
                "title" : titles["property"],
                "price" : cm.priceToString(property_price),
                "show_price" : show_price,
            })
                        
        return {
            "title"      : product.Title(),
            "url"        : product.absolute_url(),
            "price"      : price,
            "image_url"  : image_url,
            "properties" : properties,
        }