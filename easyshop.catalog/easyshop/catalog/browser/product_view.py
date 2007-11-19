# Zope imports
from zope.interface import Interface
from zope.interface import implements
from zope.component import queryUtility
from zope.component import getMultiAdapter
from zope.i18nmessageid import MessageFactory

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# Five imports
from Products.Five.browser import BrowserView

# easyshop imports
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import IData
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import INumberConverter
from easyshop.core.interfaces import IPhotoManagement
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IPropertyManagement
from easyshop.core.interfaces import IShopManagement

from easyshop.core.config import MESSAGES

_ = MessageFactory("EasyShop")

class IProductView(Interface):
    """A view for product content objects.
    """

    def addToCart():
        """Adds a product to the cart.
        """
    
    def getBasePrice():
        """Returns the standard price of the product.
        """
    
    def getCurrentPrice():
        """Returns the price of the product. Calculated on current selected
        properties
        """

    def getProperties():
        """Returns properties of the product.
        """
    
    def getBuyLabel():
        """Returns the buy label in dependence whether the product 
        has properties or not.
        """

    def getPhotos():
        """Returns all photos of the object.
        """

    def getProduct():
        """Returns product attributes as dict.
        """    
        
    def getMainPhoto():
        """Returns the main photo of the object.   
        """
            
    def getAuxiliaryPhotos():
        """Returns all photos, except the main photo, of the object.
        """

    def getPriceForCustomer():
        """Returns the price for the customer.
        """
           
    def hasPhotos():
        """Returns true if the object has photos
        """ 

    def showAddQuantity():
        """Returns True if a quantity field should be displayed.
        """

    def getRelatedProducts():
        """Returns related products. Which are selected explicity with the
        related products field.
        """
        
    def showSelectPropertiesView():
        """Returns True if the select properties view is meant to be shown.
        """
                
class ProductView(BrowserView):
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

        if len(self.getRelatedProducts()) > 0:
            url = "%s/product-view-related-products" % self.context.absolute_url()
        else:
            url = self.context.absolute_url()
        
        self.context.request.response.redirect(url)

    def getProperties(self):
        """
        """
        u = queryUtility(INumberConverter)
        cm = ICurrencyManagement(self.context)
                
        selected_properties = {}
        for name, value in self.request.form.items():
            if name.startswith("property"):
                selected_properties[name[9:]] = value

        pm = IPropertyManagement(self.context)
        
        result = []
        for property in pm.getProperties():
            options = []
            for option in property.getOptions():

                # generate value string
                name  = option["name"]
                price = option["price"]

                if price != "":
                    price = u.stringToFloat(price)
                    price = cm.priceToString(price, "long", "after")
                    content = "%s %s" % (name, price)
                else:
                    content = name
                        
                # is option selected?
                selected = name == selected_properties.get(property.getId(), False)
                
                options.append({
                    "content"  : content,
                    "value"    : name,
                    "selected" : selected,
                })            
                
            result.append({
                "id"      : property.getId(),
                "title"   : property.Title(),
                "options" : options,
            })

        return result

    def getBasePrice(self):
        """
        """
        p = IPrices(self.context)
        price = p.getPriceGross()
        
        cm = ICurrencyManagement(self.context)        
        return cm.priceToString(price)

    def getCurrentPrice(self):
        """
        """
        pm = IPropertyManagement(self.context)
        
        total_diff = 0.0
        for property_id, selected_option in self.request.form.items():
            if property_id.startswith("property"):                
                total_diff += pm.getPriceForCustomer(
                    property_id[9:], 
                    selected_option
                )

        p = IPrices(self.context)
        price = p.getPriceGross() + total_diff

        cm = ICurrencyManagement(self.context)        
        return cm.priceToString(price)
                    

    def getAuxiliaryPhotos(self):
        """
        """
        pm = IPhotoManagement(self.context)
        return pm.getAuxiliaryPhotos()

    def getBuyLabel(self):
        """
        """
        pm = IPropertyManagement(self.context)
        if len(pm.getProperties()) > 0:
            return "Buy Product"
        else:
            return "Add to Cart"

    def getMainPhoto(self):
        """
        """
        pm = IPhotoManagement(self.context)
        return pm.getMainPhoto()
        
    def getPhotos(self):
        """
        """
        pm = IPhotoManagement(self.context)
        return pm.getPhotos()

    def getPriceForCustomer(self):
        """Returns the price for the customer.
        """        
        price = IPrices(self.context).getPriceForCustomer()
        cm = ICurrencyManagement(self.context)
        
        return cm.priceToString(price, symbol="symbol", position="before")

    def getProduct(self):
        """
        """
        data = IData(self.context)
        return data.asDict()
        
    def getRelatedProducts(self):
        """
        """
        mtool = getToolByName(self.context, "portal_membership")

        result = []
        # Returns just "View"-able products.
        for product in self.context.getRefs('easyshopproduct_easyshopproducts'):
            if mtool.checkPermission("View", product) is not None:
                result.append(product)
            
        return result
                        
    def hasPhotos(self):
        """
        """
        pm = IPhotoManagement(self.context)
        return pm.hasPhotos()
                    
    def showAddQuantity(self):
        """
        """
        shop = IShopManagement(self.context).getShop()                
        return shop.getShowAddQuantity()
        
    def showSelectPropertiesView(self):
        """Returns True if the select properties view is meant to be shown.
        """
        pm = IPropertyManagement(self.context)                
        if len(pm.getProperties()) > 0:
            return True

        return False