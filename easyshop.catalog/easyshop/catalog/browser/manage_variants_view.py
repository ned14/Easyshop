# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop.imports
from easyshop.catalog.adapters.property_management import getTitlesByIds
from easyshop.catalog.adapters.property_management import getOptionsForProperty
from easyshop.core.config import MESSAGES
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IProductVariantsManagement
from easyshop.core.interfaces import IPropertyManagement
from easyshop.core.interfaces import IShopManagement

class ManageVariantsView(BrowserView):
    """
    """ 
    def addVariants(self):
        """
        """    
        putils = getToolByName(self.context, "plone_utils")
                
        title = self.request.get("title", "")
        article_id = self.request.get("article_id", "")
        
        properties = self._getPropertiesAsList()
        
        pvm = IProductVariantsManagement(self.context)
        result = pvm.addVariants(properties, title, article_id)
        
        if result == False:
            putils.addPortalMessage(MESSAGES["VARIANT_ALREADY_EXISTS"])
        else:
            putils.addPortalMessage(MESSAGES["VARIANT_ADDED"])
        
        url = self.context.absolute_url() + "/manage-variants-view"
        self.request.response.redirect(url)
        
    def deleteVariants(self):
        """
        """
        ids = self.request.get("id", None)
        
        if id is not None:
            pvm = IProductVariantsManagement(self.context)        
            pvm.deleteVariants(ids)

        putils = getToolByName(self.context, "plone_utils")
        putils.addPortalMessage("Deleted")

        url = self.context.absolute_url() + "/manage-variants-view"
        self.request.response.redirect(url)

    def getProperties(self):
        """
        """
        result = []
        pm = IPropertyManagement(self.context)
        for property in pm.getProperties():
            result.append({
                "id"      : "property_" + property.getId(),
                "title"   : property.Title(),
                "options" : property.getOptions(),
            })
        
        return result
    
    def getVariants(self):
        """
        """
        result = []
        pvm = IProductVariantsManagement(self.context)
        
        for variant in  pvm.getVariants():

            # article id
            article_id = variant.getArticleId() or \
                         variant.aq_inner.aq_parent.getArticleId()
            
            # Title
            title = variant.Title() or \
                    variant.aq_inner.aq_parent.Title()
                        
            # Options 
            properties = []
            for property in variant.getForProperties():
                property_id, option_id = property.split(":")
                titles = getTitlesByIds(variant, property_id, option_id)
                if titles is None:
                    continue
                properties.append(titles)

            # Price
            shop  = IShopManagement(self.context).getShop()
            cm    = ICurrencyManagement(self.context)
            if shop.getGrossPrices() == True:
                price = IPrices(variant).getPriceGross()
            else:
                price = IPrices(variant).getPriceNet()
                
            price = cm.priceToString(price)        
                        
            result.append({
                "id"         : variant.getId(),
                "article_id" : article_id,
                "title"      : title,
                "url"        : variant.absolute_url(),                
                "properties" : properties,
                "price"      : price,
            })                
        return result
        
        
    def _getPropertiesAsList(self):
        """
        """
        selected_properties = []
        for name, value in self.request.form.items():
            if name.startswith("property"):
                name = name[9:]
                if value == "all":
                    temp = []
                    for option in getOptionsForProperty(self.context, name):
                        temp.append("%s:%s" % (name, option["id"]))
                    selected_properties.append(temp)
                else:
                    selected_properties.append(["%s:%s" % (name, value)])
    
        selected_properties.sort()    
        return selected_properties