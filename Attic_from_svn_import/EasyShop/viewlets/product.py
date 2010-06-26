# zope imports
from zope.component import queryUtility
from zope.i18nmessageid import MessageFactory

# plone imports
from plone.app.layout.viewlets.common import ViewletBase

# Five imports
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports
from Products.EasyShop.interfaces import ICartManagement
from Products.EasyShop.interfaces import ICurrencyManagement
from Products.EasyShop.interfaces import IData
from Products.EasyShop.interfaces import IItemManagement
from Products.EasyShop.interfaces import INumberConverter
from Products.EasyShop.interfaces import IPhotoManagement
from Products.EasyShop.interfaces import IPrices
from Products.EasyShop.interfaces import IPropertyManagement
from Products.EasyShop.interfaces import IShopManagement

from Products.EasyShop.config import MESSAGES

_ = MessageFactory("EasyShop")

class ProductViewlet(ViewletBase):
    """
    """
    render = ViewPageTemplateFile('product.pt')

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