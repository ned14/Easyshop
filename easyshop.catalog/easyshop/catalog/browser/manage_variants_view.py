# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop.imports
from easyshop.core.config import MESSAGES
from easyshop.core.interfaces import IData
from easyshop.core.interfaces import IProductVariantsManagement
from easyshop.core.interfaces import IPropertyManagement

class ManageVariantsView(BrowserView):
    """
    """ 
    def addVariant(self):
        """
        """    
        title = self.request.get("title", "")
        properties = getPropertiesAsList(self.request)
        
        pvm = IProductVariantsManagement(self.context)
        pvm.addVariant(title, properties)
        
        putils = getToolByName(self.context, "plone_utils")
        putils.addPortalMessage(MESSAGES["VARIANT_ADDED"])
        
        url = self.context.absolute_url() + "/manage-variants-view"
        self.request.response.redirect(url)
        
    def deleteVariant(self):
        """
        """
        pass

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
            result.append(IData(variant).asDict())
            
        return result
        
        
def getPropertiesAsList(request):
    """
    """
    selected_properties = []
    for name, value in request.form.items():
        if name.startswith("property"):
            selected_properties.append("%s:%s" % (name[9:], value))
    
    selected_properties.sort()
    
    return selected_properties