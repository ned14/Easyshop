# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# AdvancedQuery
from Products.AdvancedQuery import Eq

class MallView(BrowserView):
    """
    """ 
    def getShops(self):
        """Returns all shops of the mall.
        """
        catalog = getToolByName(self.context, "portal_catalog")
        query = Eq("object_provides", "easyshop.core.interfaces.shop.IShop") & \
                Eq("path", "/".join(self.context.getPhysicalPath())) & \
                ~ Eq("id", self.context.getId())

        brains = catalog.evalAdvancedQuery(
                        query, ("getObjPositionInParent", ))

        shops = []
        for brain in brains:
            shop = brain.getObject()
            shops.append({
                "title" : shop.Title(),
                "url"   : shop.absolute_url(),
            })
            
        return shops