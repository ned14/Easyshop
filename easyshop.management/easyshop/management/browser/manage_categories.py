# zope imports
from zope.component import getMultiAdapter
from zope.interface import implements

# Five imports
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# CMFPlone imports
from Products.CMFPlone.utils import base_hasattr

# plone imports
from plone.app.layout.globals.interfaces import IViewView

# easyshop imports
from easyshop.core.config import MESSAGES
from easyshop.core.interfaces import ICategoryManagement
from easyshop.core.interfaces import IShopManagement

def _getContext(self):
    """
    """
    while 1:
        self = self.aq_parent
        if not getattr(self, '_is_wrapperish', None):
            return self

class ManageCategoriesView(BrowserView):
    """
    """
    implements(IViewView)
    
    def __init__(self, context, request):
        """
        """
        self.context = context
        self.request = request

        #Monkey patch for weird error
        ZopeTwoPageTemplateFile._getContext = _getContext
        
        selected_categories = self.request.get("selected_category", [])
        if not isinstance(selected_categories, (list, tuple)):
            selected_categories = (selected_categories,)
        
        self.selected_categories = selected_categories
        
        if self.hasSelectedCategories() and \
           ("manage-categories" in self.request.form.keys()):
            putils = getToolByName(self.context, "plone_utils")
            putils.addPortalMessage(MESSAGES["SELECTED_CATEGORIES"])
    
    def deleteCategories(self):
        """
        """
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(UID = self.selected_categories)
        
        for category in [b.getObject() for b in brains]:
            parent = category.aq_inner.aq_parent
            parent.manage_delObjects(category.getId())

        putils = getToolByName(self.context, "plone_utils")
        putils.addPortalMessage(MESSAGES["DELETED_CATEGORIES"])
        
        self._redirect()
        
    def addCategory(self):
        """
        """
        category_name = self.request.get("category_name", "")
        if category_name == "":
            return self._showView()
            
        shop = IShopManagement(self.context).getShop()

        putils = getToolByName(self.context, "plone_utils")        
        normalized_id = putils.normalizeString(category_name)

        if base_hasattr(shop, normalized_id) == True:
            putils.addPortalMessage(MESSAGES["CATEGORY_ALREADY_EXISTS"], "error")
            return self._showView()
        else:
            shop.invokeFactory("Category", id=normalized_id, title=category_name)
            putils.addPortalMessage(MESSAGES["ADDED_CATEGORY"])
            
        new_category = shop[normalized_id]
        
        if self.hasSelectedCategories() == True:
            catalog = getToolByName(self.context, "portal_catalog")
            brains = catalog.searchResults(UID = self.selected_categories)            
            parent_categories = [b.getObject() for b in brains]            
            new_category.setParentCategory(parent_categories)
            new_category.reindexObject()

        return self._showView()
    
    def deselectCategories(self):
        """
        """
        putils = getToolByName(self.context, "plone_utils")
        putils.addPortalMessage(MESSAGES["DESELECT_CATEGORIES"])
        self._redirect()
        
    def getSelectedCategories(self):
        """
        """
        return self.selected_categories

    def moveCategoryDown(self):
        """
        """
        category_uid = self.request.get("category_uid")
        category = self._getCategoryByUID(category_uid)
        
        if category is None:
            self._redirect()
            return False
        
        category.setPositionInParent(category.getPositionInParent()+3)
        self._reindexPositions(category)
        self._redirect()

    def moveCategoryUp(self):
        """
        """
        category_uid = self.request.get("category_uid")
        category = self._getCategoryByUID(category_uid)
        
        if category is None:
            self._redirect()
            return False
        
        category.setPositionInParent(category.getPositionInParent()-3)
        self._reindexPositions(category)
        self._redirect()

    def setCollapsileState(self):
        """
        """
        set_state = self.request.get("set_state", "false")
        uid = self.request.get("uid")
        extended = self.request.SESSION.get("extended", [])
        
        if uid is not None:
            if set_state == "false" and uid not in extended:
                extended.append(uid)
                self.request.SESSION["extended"] = extended
            elif set_state == "true" and uid in extended:
                del extended[extended.index(uid)]
        
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
                      
    def moveToCategory(self):
        """
        """
        catalog = getToolByName(self.context, "portal_catalog")
        target_category_uid = self.request.get("target_category")
        
        if target_category_uid == "no-category":
            for selected_category_uid in self.selected_categories:
                brains = catalog.searchResults(UID = selected_category_uid)
                selected_category = brains[0].getObject()
                selected_category.setParentCategory(None)
                selected_category.reindexObject()
        
        elif target_category_uid is not None:
            target_category_brains = catalog(UID = target_category_uid)
            
            if len(target_category_brains) == 1:
                target_category = target_category_brains[0].getObject()
                                
                for selected_category_uid in self.selected_categories:
                    brains = catalog.searchResults(UID = selected_category_uid)
                    selected_category = brains[0].getObject()
                    selected_category.setParentCategory(target_category)
                    selected_category.reindexObject()
        
        putils = getToolByName(self.context, "plone_utils")
        putils.addPortalMessage(MESSAGES["MOVED_CATEGORIES"])
                    
        return self._showView()
            
    def hasSelectedCategories(self):
        """
        """
        return len(self.selected_categories) > 0

    def _showView(self):
        """
        """        
        view = getMultiAdapter((self.context, self.context.request), name="manage-categories")
        return view()
        
    def _redirect(self):
        """
        """
        self.request.response.redirect("manage-categories")
        
