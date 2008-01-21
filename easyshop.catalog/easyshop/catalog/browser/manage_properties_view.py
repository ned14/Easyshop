# zope imports
from zope import event

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# Archetypes imports
from Products.Archetypes.event import ObjectInitializedEvent

# easyshop.imports
from easyshop.core.config import MESSAGES

class ManagePropertiesView(BrowserView):
    """
    """
    def addOption(self):
        """
        """
        property_id = self.request.get("property_id", "")
        property    = self.context[property_id]
                
        new_id    = self.context.generateUniqueId("ProductPropertyOption")
        title     = self.request.get("title", "")
        price     = self.request.get("price", "")
        file_name = self.request.get("file", "")

        # Price
        try:
            price = float(price)
        except ValueError:
            price = 0.0
            
        new_id = property.invokeFactory("ProductPropertyOption", new_id, title=title, 
            image=file_name, price=price)
        
        option = property[new_id]
        option._renameAfterCreation(check_auto_id=True)
        
        putils = getToolByName(self.context, "plone_utils")
        putils.addPortalMessage(MESSAGES["ADDED_PRODUCT_OPTION"])
        
        url = self.context.absolute_url() + "/" + "manage-properties-view"
        self.context.request.response.redirect(url)
        
    def addProperty(self):
        """
        """
        new_id = self.context.generateUniqueId("ProductProperty")
        title  = self.request.get("title", "")
        self.context.invokeFactory("ProductProperty", new_id, title=title)
        
        property = self.context[new_id]
        event.notify(ObjectInitializedEvent(property))
        property.at_post_create_script()

        putils = getToolByName(self.context, "plone_utils")
        putils.addPortalMessage(MESSAGES["ADDED_PRODUCT_PROPERTY"])
        
        url = self.context.absolute_url() + "/" + "manage-properties-view"
        self.context.request.response.redirect(url)

    def deletePaths(self):
        """
        """
        paths = self.request.get("paths", [])
        if len(paths) != 0:
            putils = getToolByName(self.context, "plone_utils")
            
            # Strange UnicodeDecodeError here. For the same object deleted via 
            # the default folder contents delete method (which uses also 
            # deleteObjectsByPaths there is none.
            try:
                success, failure = putils.deleteObjectsByPaths(
                    paths, REQUEST=self.request)
            except UnicodeDecodeError:
                pass
                
            putils.addPortalMessage(MESSAGES["VARIANTS_DELETED"])

        url = self.context.absolute_url() + "/" + "manage-properties-view"
        self.context.request.response.redirect(url)
        
    def getProperties(self):
        """
        """
        result = []
        for property in self.context.objectValues("ProductProperty"):
            options = property.getOptions()
            result.append({
                "id"      : property.getId(),
                "title"   : property.Title(),                
                "path"    : "/".join(property.getPhysicalPath()),
                "options" : options,
            })
        
        return result

    def saveOptions(self):
        """Saves all variants.
        """
        names = {}
        prices = {}
        images = {}

        for id, value in self.request.form.items():
            if id.startswith("price"):
                prices[id[6:]] = value
            elif id.startswith("name"):
                names[id[5:]] = value
            elif id.startswith("image"):
                images[id[6:]] = value

        property_id = self.request.get("property_id")
        property = self.context.get(property_id, None)
        
        if property is None:
            return 
            
        for option in property.objectValues("ProductPropertyOption"):
            
            try:
                price = float(prices[option.getId()])
            except ValueError:
                price = 0.0
                
            option.setPrice(price)
            option.setTitle(names[option.getId()])
            
            image = images[option.getId()]
            option.setImage(image)
            
        putils = getToolByName(self.context, "plone_utils")
        putils.addPortalMessage(MESSAGES["PROPERTY_OPTIONS_SAVED"])
    
        url = self.context.absolute_url() + "/manage-properties-view"
        self.request.response.redirect(url)