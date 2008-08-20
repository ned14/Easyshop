# kss imports
from plone.app.kss.plonekssview import PloneKSSView
from kss.core import kssaction

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop.imports 
from easyshop.core.interfaces import ICategoryManagement

class CategoriesKSSView(PloneKSSView):
    """
    """
    @kssaction
    def moveCategoryUp(self, uid):
        """
        """
        category = self._getCategoryByUID(uid)
        
        if category is None:
            self._refreshViewlet()
            return
        
        category.setPositionInParent(category.getPositionInParent()-3)
        self._reindexPositions(category)
        self._refreshViewlet()

    @kssaction
    def moveCategoryDown(self, uid):
        """
        """
        category = self._getCategoryByUID(uid)
        
        if category is None:
            self._refreshViewlet()
            return
        
        category.setPositionInParent(category.getPositionInParent()+3)
        self._reindexPositions(category)
        self._refreshViewlet()

    def _refreshViewlet(self):
        """
        """
        kss_core  = self.getCommandSet("core")
        kss_zope  = self.getCommandSet("zope")
        
        kss_zope.refreshViewlet(
            kss_core.getHtmlIdSelector("manage-categories"),
            manager="easyshop.management.categories-management",
            name="easyshop.management.categories")
            
    def _reindexPositions(self, category):
        """
        """
        if category.getParentCategory() is not None:
            parent = category.getParentCategory()
        else:
            parent = category.aq_inner.aq_parent        

        category.reindexObject()

        i = 0
        for category in ICategoryManagement(parent).getTopLevelCategories():
            i+=2
            category.setPositionInParent(i)            
            category.reindexObject()

    def _getCategoryByUID(self, uid):
        """
        """
        catalog = getToolByName(self.context, "portal_catalog")
        category_brains = catalog(UID = uid)
        if len(category_brains) == 1:
            return category_brains[0].getObject()
        else:
            return None