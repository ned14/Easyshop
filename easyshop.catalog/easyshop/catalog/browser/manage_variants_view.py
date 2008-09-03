# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop.imports
from easyshop.catalog.adapters.property_management import getTitlesByIds
from easyshop.catalog.adapters.property_management import getOptionsForProperty
from easyshop.core.config import MESSAGES
from easyshop.core.interfaces import IProductVariantsManagement
from easyshop.core.interfaces import IPropertyManagement

class ManageVariantsView(BrowserView):
    """
    """ 
    def isOptionSelected(self, variant, property_id, option_id):
        """
        """
        try:
            selected_option_id = variant['properties_ids'][property_id]
        except KeyError:
            return False
            
        if selected_option_id == option_id:
            return True
        else:
            return False
            
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
        price = self.request.get("price", 0.0)
        
        try:        
            price = float(price)
        except ValueError:
            price = 0.0
            
        properties = self._getPropertiesAsList()
        
        pvm = IProductVariantsManagement(self.context)
        result = pvm.addVariants(properties, title, article_id, price)
        
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

            # Only properties with at least one option are displayed.
            options = property.getOptions()
            if len(options) == 0:
                continue
                
            result.append({
                "id"      : property.getId(),
                "name"    : "property_" + property.getId(),
                "title"   : property.Title(),
                "options" : options,
            })
        
        return result
    
    def getVariants(self):
        """
        """
        result = []
        pvm = IProductVariantsManagement(self.context)
        
        for variant in pvm.getVariants():
            
            # Options 
            properties = []
            properties_ids = {}
            for property in variant.getForProperties():
                property_id, option_id = property.split(":")
                properties_ids[property_id] = option_id
                titles = getTitlesByIds(variant, property_id, option_id)
                if titles is None:
                    continue
                properties.append(titles)

            result.append({
                "id"             : variant.getId(),
                "path"           : "/".join(variant.getPhysicalPath()),
                "article_id"     : variant.getArticleId(),
                "title"          : variant.Title(),
                "url"            : variant.absolute_url(),                
                "properties"     : properties,
                "properties_ids" : properties_ids,
                "price"          : variant.getPrice(),
            })                
        return result
        
    def saveVariants(self):
        """Saves all variants.
        """
        article_ids = {}                
        prices = {}
        properties = {}                
        titles = {}

        for id, value in self.request.form.items():
            if id.startswith("price"):
                prices[id[6:]] = value
            elif id.startswith("article-id"):
                article_ids[id[11:]] = value
            elif id.startswith("title"):
                titles[id[6:]] = value
            elif id.startswith("property"):
                property_id, variant_id = id.split("|")
                property_id = property_id[9:]
                if properties.has_key(variant_id) == False:
                    properties[variant_id] = []
                properties[variant_id].append("%s:%s" % (property_id, value))
        
        pvm = IProductVariantsManagement(self.context)
        for variant in pvm.getVariants():
            # Title
            title = titles[variant.getId()]
            
            # Title is only set when it's different from parent product 
            # variants. Otherwise we leave it empty ot display parent's title
            if title != self.context.Title():
                variant.setTitle(title)
            else:
                variant.setTitle("")
            
            # Article ID
            article_id = article_ids[variant.getId()]
            
            # Article ID is only set when it's different from parent product 
            # variants. Otherwise we leave it empty ot display parent's article 
            # id
            if article_id != self.context.getArticleId():
                variant.setArticleId(article_id)
            else:
                variant.setArticleId("")
                
            # Price can always be set, because 0.0 is considered as empty 
            # anyway.
            variant.setPrice(prices[variant.getId()])

            properties[variant.getId()].sort()
            variant.setForProperties(properties[variant.getId()])
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
            if name.startswith("add_property"):
                name = name[13:]
                if value == "all":
                    temp = []
                    for option in getOptionsForProperty(self.context, name):
                        temp.append("%s:%s" % (name, option["id"]))
                    selected_properties.append(temp)
                else:
                    selected_properties.append(["%s:%s" % (name, value)])
    
        selected_properties.sort()    
        return selected_properties