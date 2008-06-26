# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

class MigrateView(BrowserView):
    """
    """
    def migrate(self):
        """
        """
        # self.context._initBTrees()
        # self.context.reindexObject()
        
        utool = getToolByName(self.context, "portal_url")
        portal = utool.getPortalObject()
        
        shop = portal["shop"]
        
        import pdb; pdb.set_trace()
        self.context._populateFromFolder(shop)