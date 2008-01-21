# Zope imports
from zope.interface import Interface
from zope.interface import implements
from zope.i18nmessageid import MessageFactory

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# Five imports
from Products.Five.browser import BrowserView

# easyshop imports
from easyshop.core.config import MESSAGES
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IProductVariantsManagement
from easyshop.core.interfaces import IShopManagement

_ = MessageFactory("EasyShop")

class IProductView(Interface):
    """A view for product content objects.
    """

    def addToCart():
        """Adds a product to the cart.
        """
                    
class ProductAddToCartView(BrowserView):
    """
    """
    implements(IProductView)

    def addToCart(self):
        """
        """
        shop = IShopManagement(self.context).getShop()        
        cm = ICartManagement(shop)
        
        cart = cm.getCart()
        if cart is None:
            cart = cm.createCart()

        properties = []
        for property_id, selected_option in self.request.form.items():
            if property_id.startswith("property") == False:
                continue
                
            if selected_option == "please_select":
                continue
                    
            properties.append(
                {"id" : property_id[9:], 
                 "selected_option" : selected_option 
                }
            )

        # get quantity
        quantity = int(self.context.request.get("quantity", 1))

        # returns true if the product was already within the cart    
        result = IItemManagement(cart).addItem(self.context, tuple(properties), quantity)
        
        # Set portal message
        putils = getToolByName(self.context, "plone_utils")        
        if result == True:
            putils.addPortalMessage(_(MESSAGES["CART_INCREASED_AMOUNT"]))
        else:
            putils.addPortalMessage(_(MESSAGES["CART_ADDED_PRODUCT"]))

        url = "%s/added-to-cart" % shop.absolute_url()
        self.context.request.response.redirect(url)
        
class ProductVariantsAddToCartView(BrowserView):
    """
    """
    implements(IProductView)

    def addToCart(self):
        """
        """
        import pdb; pdb.set_trace()
        pvm = IProductVariantsManagement(self.context)
        product_variant = pvm.getSelectedVariant() or pvm.getDefaultVariant()
        
        shop = IShopManagement(product_variant).getShop()        
        cm = ICartManagement(shop)
        
        cart = cm.getCart()
        if cart is None:
            cart = cm.createCart()

        properties = []
        for property in product_variant.getForProperties():
            property_id, selected_option = property.split(":")
            properties.append(
                {"id" : property_id,
                 "selected_option" : selected_option,
                }
            )

        # get quantity
        quantity = int(self.context.request.get("quantity", 1))

        # returns true if the product was already within the cart    
        result = IItemManagement(cart).addItem(product_variant, tuple(properties), quantity)
        
        # Set portal message
        putils = getToolByName(self.context, "plone_utils")        
        if result == True:
            putils.addPortalMessage(_(MESSAGES["CART_INCREASED_AMOUNT"]))
        else:
            putils.addPortalMessage(_(MESSAGES["CART_ADDED_PRODUCT"]))

        url = "%s/added-to-cart" % shop.absolute_url()
        self.context.request.response.redirect(url)