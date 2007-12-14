# zope imports
from zope.component import queryUtility

# plone imports
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize.instance import memoize

# Five imports
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import IData
from easyshop.core.interfaces import INumberConverter
from easyshop.core.interfaces import IPhotoManagement
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IPropertyManagement
from easyshop.core.interfaces import IShopManagement
from easyshop.core.interfaces import IStockManagement

class ProductViewlet(ViewletBase):
    """
    """
    render = ViewPageTemplateFile('product.pt')

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

    def getPriceForCustomer(self):
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
        price = p.getPriceForCustomer() + total_diff

        cm = ICurrencyManagement(self.context)
        return cm.priceToString(price)
                    
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

    def getProduct(self):
        """
        """
        data = IData(self.context)
        return data.asDict()

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
        
    def getRelatedProducts(self):
        """
        """
        mtool = getToolByName(self.context, "portal_membership")

        result = []
        # Returns just "View"-able products.
        for product in self.context.getRefs('products_products'):
            if mtool.checkPermission("View", product) is not None:
                result.append(product)
            
        return result

    def getStockInformation(self):
        """
        """
        shop = self._getShop()
        sm = IStockManagement(shop)
        stock_information = sm.getValidStockInformationFor(self.context)
        
        if stock_information is None:
            return None
            
        return IData(stock_information).asDict()
                    
    def hasPhotos(self):
        """
        """
        pm = IPhotoManagement(self.context)
        return pm.hasPhotos()
                    
    def showAddQuantity(self):
        """
        """
        shop = self._getShop() 
        return shop.getShowAddQuantity()

    @memoize
    def _getShop(self):
        """
        """
        return IShopManagement(self.context).getShop()