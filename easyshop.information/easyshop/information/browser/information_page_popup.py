# Five imports
from Products.Five.browser import BrowserView

# easyhop.core imports
from easyshop.core.interfaces import IShopManagement

class InformationPagePopupView(BrowserView):
    """
    """
    def getInformation(self):
        """Returns information for information page which is given by request.
        """
        page_id = self.request.get("page_id")    
        page = self.context.information.get(page_id)
        if page is None:
            return None
            
        shop = IShopManagement(self.context).getShop()
    
        return {
            "shop_owner"  : shop.getShopOwner(),
            "url"         : "%s/at_download/file" % page.absolute_url(),
            "title"       : page.Title(),
            "description" : page.Description(),
            "text"        : page.getText(),
        }