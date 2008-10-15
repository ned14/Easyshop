# zope imports
from zope.component import queryUtility
from zope.component import getMultiAdapter
from zope.viewlet.interfaces import IViewlet

# CMFPlone imports
from Products.CMFPlone.utils import tuplize
        
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

    def getTotalPriceForCustomer(self, formatted=True):
        """
        """
        selected_accessories = self.request.get("accessories", [])
        selected_accessories = tuplize(selected_accessories)
        
        product_price = self.getPriceForCustomer(formatted=False)
        
        total_accessories = 0
        for accessory in self.getAccessories():
            # We take only selected accessories into account
            if accessory["uid"] in selected_accessories:
                total_accessories += accessory["total_raw_price"]
        
        total_price = product_price + total_accessories    
        
        cm = ICurrencyManagement(self.context)
        return cm.priceToString(total_price)

    def getPriceForCustomer(self, formatted=True):
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
                        property_id[42:],
                        selected_option
                    )            
            price += total_diff

        if formatted == True:
            cm = ICurrencyManagement(self.context)
            return cm.priceToString(price)
        else:
            return price
    
    def getTotalStandardPriceForCustomer(self):
        """
        """
        selected_accessories = self.request.get("accessories", [])
        selected_accessories = tuplize(selected_accessories)
        
        product_price = self.getStandardPriceForCustomer(formatted=False)
        
        total_accessories = 0
        for accessory in self.getAccessories():
            # We take only selected accessories into account
            if accessory["uid"] in selected_accessories:
                total_accessories += accessory["total_raw_standard_price"]
        total_price = product_price + total_accessories    
        
        cm = ICurrencyManagement(self.context)
        return cm.priceToString(total_price)
        
    def getStandardPriceForCustomer(self, formatted=True):
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
                        property_id[42:],
                        selected_option
                    )            
            price + total_diff
        
        if formatted == True:
            cm = ICurrencyManagement(self.context)
            return cm.priceToString(price)
        else:
            return price
                            
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
    
    def getAccessories(self):
        """
        """
        catalog = getToolByName(self.context, "portal_catalog")
        
        accessories = tuplize(self.request.get("accessories", []))

        result = []
        for uid_with_quantiy in self.context.getAccessories():
            uid, quantity = uid_with_quantiy.split(":")
                        
            try:
                brain = catalog.searchResults(UID=uid)[0]                
            except IndexError:
                # This could happend if the user doesn't have the View 
                # permission (e.g. product is private)
                continue
                
            product = brain.getObject()
            
            # Try to get quantity out of request (In case the customer has
            # changed them within the form). If there is none we take the default
            # quantity which are given from the shop owner within the accessories
            # admin interface.
            quantity = self.request.get("%s_quantity" % product.UID(), quantity)
            
            # Same viewlet with the context of the accessory to get the 
            # properties of the accessory.            
            viewlet = getMultiAdapter((product, self.request, self.view, self.manager), IViewlet, name="easyshop.product-viewlet")
            properties = viewlet.getProperties()
            
            try:
                quantity = int(quantity)
            except ValueError:
                quantity = 1
                
            # Standard price
            standard_price = viewlet.getStandardPriceForCustomer(formatted=False)
            total_raw_standard_price = quantity * standard_price
            cm = ICurrencyManagement(self.context)
            standard_price = cm.priceToString(standard_price)
            total_standard_price = cm.priceToString(total_raw_standard_price)

            # Effective price
            price = viewlet.getPriceForCustomer(formatted=False)
            total_raw_price = quantity * price
            
            cm = ICurrencyManagement(self.context)
            price = cm.priceToString(price)
            total_price = cm.priceToString(total_raw_price)
            
            result.append({
                "uid" : uid,
                "title" : brain.Title,
                "quantity" : quantity,
                "checked" : uid in accessories,
                "for_sale" : product.getForSale(),
                "total_raw_price" : total_raw_price, 
                "total_raw_standard_price" : total_raw_standard_price, 
                "standard_price" : standard_price,
                "total_standard_price" : total_standard_price,
                "price" : price,
                "total_price" : total_price,
                "properties" : properties,
            })
        
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
                selected_options[name[42:]] = value
        
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
                "id"      : "property_%s_%s" % (self.context.UID(), property.getId()),
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
                if len(name) > 42:
                    selected_options[name[42:]] = value
                else:
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
                "id"      : "property_%s_%s" % (self.context.UID(), property.getId()),
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