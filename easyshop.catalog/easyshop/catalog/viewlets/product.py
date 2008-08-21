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
from easyshop.core.config import _
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import IData
from easyshop.core.interfaces import INumberConverter
from easyshop.core.interfaces import IImageManagement
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IProductVariantsManagement
from easyshop.core.interfaces import IPropertyManagement
from easyshop.core.interfaces import IShopManagement
from easyshop.core.interfaces import IStockManagement

class ProductViewlet(ViewletBase):
    """
    """
    render = ViewPageTemplateFile('product.pt')

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
        p = IPrices(self.context)
        price = p.getPriceForCustomer()
        
        if IProductVariantsManagement(self.context).hasVariants() == False:
            total_diff = 0.0
            pm = IPropertyManagement(self.context)
            for property_id, selected_option in self.request.form.items():
                if property_id.startswith("property"):                
                    total_diff += pm.getPriceForCustomer(
                        property_id[9:],
                        selected_option
                    )            
            price += total_diff
            
        cm = ICurrencyManagement(self.context)
        return cm.priceToString(price)

    def getStandardPriceForCustomer(self):
        """Returns the standard price for a customer when the product is for 
        sale. Used to display the crossed-out standard price.
        """
        p = IPrices(self.context)
        price = p.getPriceForCustomer(effective=False)
        
        if IProductVariantsManagement(self.context).hasVariants() == False:
            total_diff = 0.0
            pm = IPropertyManagement(self.context)
            for property_id, selected_option in self.request.form.items():
                if property_id.startswith("property"):                
                    total_diff += pm.getPriceForCustomer(
                        property_id[9:],
                        selected_option
                    )            
            price + total_diff
            
        cm = ICurrencyManagement(self.context)
        return cm.priceToString(price)
                            
    def getProductData(self):
        """
        """        
        data = IData(self.context)
        return data.asDict()

    def getImageUrls(self):
        """
        """
        pm = IImageManagement(self.context)

        result = []
        for image in pm.getImages():
            result.append(
                "%s/image_tile"  % image.absolute_url(),
            )
                        
        return result
        
    def getProperties(self):
        """
        """    
        pvm = IProductVariantsManagement(self.context)
        if pvm.hasVariants():
            return self._getPropertiesForVariants()
        else:
            return self._getPropertiesForConfiguration()
            
    def _getPropertiesForConfiguration(self):
        """
        """
        u = queryUtility(INumberConverter)
        cm = ICurrencyManagement(self.context)
                        
        selected_options = {}
        for name, value in self.request.items():
            if name.startswith("property"):
                selected_options[name[9:]] = value
        
        pm = IPropertyManagement(self.context)
        
        result = []
        for property in pm.getProperties():
            
            # Only properties with at least one option are displayed.
            if len(property.getOptions()) == 0:
                continue
            
            # Preset with select option
            options = [{
                "id"       : "select",
                "title"    : _(u"Select"),
                "selected" : False,
            }]
            
            for option in property.getOptions():

                # generate value string
                option_id    = option["id"]
                option_name  = option["name"]
                option_price = option["price"]

                if option_price != "0.0":
                    option_price = u.stringToFloat(option_price)
                    option_price = cm.priceToString(option_price, "long", "after")
                    content = "%s %s" % (option_name, option_price)
                else:
                    content = option_name
                        
                # is option selected?
                selected_option = selected_options.get(property.getId(), "")
                selected = option_id == selected_option
                
                options.append({
                    "id"       : option_id,
                    "title"    : content,
                    "selected" : selected,
                })
                
            result.append({
                "id"      : "property_" + property.getId(),
                "title"   : property.Title(),
                "options" : options,
            })

        return result
        
    def _getPropertiesForVariants(self):
        """
        """
        u = queryUtility(INumberConverter)
        cm = ICurrencyManagement(self.context)
                        
        selected_options = {}
        for name, value in self.request.items():
            if name.startswith("property"):
                selected_options[name[9:]] = value

        # If nothing is selected we select the default variant
        if selected_options == {}:
            pvm = IProductVariantsManagement(self.context)
            default_variant = pvm.getDefaultVariant()

            # If there is no default variant return empty list
            if default_variant is None:
                return []

            for property in default_variant.getForProperties():
                name, value = property.split(":")
                selected_options[name] = value
            
        pm = IPropertyManagement(self.context)
        
        result = []
        for property in pm.getProperties():
            
            # Only properties with at least one option are displayed.
            if len(property.getOptions()) == 0:
                continue
            
            options = []
            for option in property.getOptions():

                # generate value string
                option_id    = option["id"]
                option_name  = option["name"]
                # option_price = option["price"]
                # option_price = u.stringToFloat(option_price)
                # option_price = cm.priceToString(option_price, "long", "after")
                # content = "%s %s" % (option_name, option_price)
                content = option_name
                        
                # is option selected?
                selected_option = selected_options.get(property.getId(), "")
                selected = option_id == selected_option
                
                options.append({
                    "id"       : option_id,
                    "title"    : content,
                    "selected" : selected,
                })
                
            result.append({
                "id"      : "property_" + property.getId(),
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
        
        pvm = IProductVariantsManagement(self.context)
        
        if pvm.hasVariants() == False:
            stock_information = sm.getStockInformationFor(self.context)            
        else:
            product_variant = pvm.getSelectedVariant()

            # First, we try to get information for the selected product variant
            stock_information = sm.getStockInformationFor(product_variant)

            # If nothing is found, we try to get information for parent product 
            # variants object.
            if stock_information is None:
                stock_information = sm.getStockInformationFor(self.context)
            
        if stock_information is None:
            return None
            
        return IData(stock_information).asDict()
                    
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