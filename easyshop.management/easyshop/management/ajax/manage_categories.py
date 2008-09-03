# imports
from zope.component import getMultiAdapter
from zope.viewlet.interfaces import IViewletManager

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop.imports 
from easyshop.core.interfaces import ICategoryManagement

class ManageCategoriesView(BrowserView):
    """
    """ 
    def addCategory(self):
        """
        """
        name = self.request.get("name")
        self.context.invokeFactory("Category", id=name, title=name)
        self.context[name].reindexObject()
        
        return self._refreshViewlet()
        
    def moveCategoryUp(self):
        """
        """
        uid = self.request.get("uid")
        category = self._getCategoryByUID(uid)
        
        if category is not None:
            category.setPositionInParent(category.getPositionInParent()-3)
            self._reindexPositions(category)

        return self._refreshViewlet()

    def moveCategoryDown(self, uid):
        """
        """
        uid = self.request.get("uid")
        category = self._getCategoryByUID(uid)
        
        if category is not None:
            category.setPositionInParent(category.getPositionInParent()+3)
            self._reindexPositions(category)
            
        return self._refreshViewlet()

    def _refreshViewlet(self):
        """
        """
        renderer = getMultiAdapter((self.context, self.request, self), IViewletManager, name="easyshop.management.categories-management")
        renderer = renderer.__of__(self.context)
        
        renderer.update()
        return renderer.render()        

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