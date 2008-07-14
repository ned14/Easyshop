import transaction

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import ICategory

class MigrateView(BrowserView):
    """
    """
    def migrate(self):
        """
        """
        utool = getToolByName(self.context, "portal_url")
        portal = utool.getPortalObject()
        shop = portal.shop2
        
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            portal_type = "Category",
        )
        
        for brain in brains:
                
            category = brain.getObject()
            
            parent = category.aq_inner.aq_parent
            if ICategory.providedBy(parent):
                category.setParentCategory(parent)
                category.setPositionInParent(category.getObjPositionInParent())
                
        # transaction.commit()
        # 
        # for brain in brains:
        #     category = brain.getObject()
        # 
        #     if len(category.getPhysicalPath()) == 5:
        #         ids = category.objectIds("Category")
        #         if len(ids) > 0:
        #             data = category.manage_cutObjects(ids)
        #             shop.manage_pasteObjects(data)
        # 
        # transaction.commit()
        # 
        # for brain in brains:
        #     category = brain.getObject()
        # 
        #     if len(category.getPhysicalPath()) == 4:
        #         ids = category.objectIds("Category")
        #         if len(ids) > 0:
        #             data = category.manage_cutObjects(ids)
        #             shop.manage_pasteObjects(data)
        #             
