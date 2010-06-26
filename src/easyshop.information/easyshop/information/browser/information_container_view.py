# Five imports
from Products.Five.browser import BrowserView

# easyshop imports
from easyshop.core.interfaces import IShopManagement
from easyshop.core.interfaces import IInformationManagement

class InformationContainerView(BrowserView):
    """
    """
    def getInformationPages(self):
        """
        """
        shop = IShopManagement(self.context).getShop()
        im   = IInformationManagement(shop)
                
        result = []
        for information in im.getInformationPages():
            
            result.append({
                "id"          : information.getId(),
                "title"       : information.Title(),
                "url"         : information.absolute_url(),
                "description" : information.Description(),
                "up_url"      : "%s/es_folder_position?position=up&id=%s" % (self.context.absolute_url(), information.getId()),
                "down_url"    : "%s/es_folder_position?position=down&id=%s" % (self.context.absolute_url(), information.getId()),
                "amount_of_criteria" : len(information.objectIds()),                
            })

        return result