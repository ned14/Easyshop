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
from easyshop.core.interfaces import IGroupManagement
from easyshop.core.interfaces import IProduct
from easyshop.core.interfaces import IPropertyManagement

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

    def getGlobalProperties(self):
        """Returns properties which are provided from groups of the product.
        """
        result = []
        for group in IGroupManagement(self.context).getGroups():
            properties = []
            # TODO: Change to IPropertyManagement().getProperties()
            for property in group.objectValues("ProductProperty"):
                properties.append({
                    "id"      : property.getId(),
                    "title"   : property.Title(),
                    "url"     : property.absolute_url(),
                    "options" : property.getOptions(),
                })

            result.append({
                "group_title" : group.Title(),
                "group_url"   : group.absolute_url(),
                "properties"  : properties,
            })
        
        return result
        
    def getProperties(self):
        """
        """
        result = []
        # TODO: Change to IPropertyManagement().getProperties()
        for property in self.context.objectValues("ProductProperty"):
            result.append({
                "id"      : property.getId(),
                "title"   : property.Title(),                
                "path"    : "/".join(property.getPhysicalPath()),
                "options" : property.getOptions(),
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
        
    def showGlobalProperties(self):
        """Returns True for product content objects. False for groups.

        This view is used for groups and products, so the global properties 
        section (properties which come from groups) have to be hidden for 
        groups.
        """
        if IProduct.providedBy(self.context):
            return True
        else:
            return False        