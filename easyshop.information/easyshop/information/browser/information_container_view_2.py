# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

class InformationContainerView(BrowserView):
    """
    """
    def getInformationPages(self):
        """Returns all information pages.
        """
        mtool = getToolByName(self.context, "portal_membership")
        if mtool.checkPermission("Manage portal", self.context) == True:
            omit_edit_link = False
        else:
            omit_edit_link = True
        
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            path = "/".join(self.context.getPhysicalPath()),
            portal_type = "InformationPage",
            sort_on = "getObjPositionInParent",
        )
            
        result = []
        for page in brains:
            result.append({
                "id"             : page.getId,
                "title"          : page.Title,
                "description"    : page.Description,
                "omit_edit_link" : omit_edit_link,
                "url"            : page.getURL(),
                "edit_url"       : "%s/edit" % page.getURL(),
                "download_url"   : "%s/at_download/file" % page.getURL(),
            })

        return result