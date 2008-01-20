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
    def addProperty(self):
        """
        """
        pass
        # id = self.context.generateUniqueId("Property")                
        # property = ProductProperty(id)
        # self.context._setObject(id, property)
        # 
        # url = self.context.absolute_url() + "/manage-variants-view"
        # self.request.response.redirect(url)
        
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
        paths = self.request.get("paths", None)

        if paths is not None:
            putils = getToolByName(self.context, "plone_utils")
            putils.deleteObjectsByPaths(paths)
            putils.addPortalMessage(MESSAGES["VARIANTS_DELETED"])

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
        
        for variant in pvm.getVariants():

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
                
            result.append({
                "id"         : variant.getId(),
                "path"       : "/".join(variant.getPhysicalPath()),
                "article_id" : article_id,
                "title"      : title,
                "url"        : variant.absolute_url(),                
                "properties" : properties,
                "price"      : price,
            })                
        return result
        
    def saveVariants(self):
        """Saves all variants.
        """
        article_ids = {}                
        prices = {}
        titles = {}        
        for id, value in self.request.form.items():
            if id.startswith("price"):
                prices[id[6:]] = value
            elif id.startswith("article-id"):
                article_ids[id[11:]] = value
            elif id.startswith("title"):
                titles[id[6:]] = value

        pvm = IProductVariantsManagement(self.context)
        for variant in pvm.getVariants():
            variant.setArticleId(article_ids[variant.getId()])
            variant.setPrice(prices[variant.getId()])
            variant.setTitle(titles[variant.getId()])
            variant.reindexObject()
            
        putils = getToolByName(self.context, "plone_utils")
        putils.addPortalMessage(MESSAGES["VARIANTS_SAVED"])
        
        url = self.context.absolute_url() + "/manage-variants-view"
        self.request.response.redirect(url)
        
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