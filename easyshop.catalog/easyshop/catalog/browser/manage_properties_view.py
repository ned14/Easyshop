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
        file_name = self.request.get("file", "")

        property.invokeFactory("ProductPropertyOption", new_id, title=title, image=file_name)

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
