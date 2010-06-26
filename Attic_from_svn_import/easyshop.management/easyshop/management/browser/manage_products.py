# zope imports
from zope.component import getMultiAdapter
from zope.interface import implements

# Five imports
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# plone imports
from plone.app.layout.globals.interfaces import IViewView

# easyshop imports
from easyshop.core.interfaces import ICategoryManagement
from easyshop.core.interfaces import IGroupManagement

def _getContext(self):
    """
    """
    while 1:
        self = self.aq_parent
        if not getattr(self, '_is_wrapperish', None):
            return self

class ManageProductsView(BrowserView):
    """
    """
    implements(IViewView)
        
    def __init__(self, context, request):
        self.context = context
        self.request = request

        #Monkey patch for weird error
        ZopeTwoPageTemplateFile._getContext = _getContext

    def getCategories(self):
        """
        """
        cm = ICategoryManagement(self.context)
        
        result = []
        
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            path = "/".join(self.context.getPhysicalPath()),
            object_provides="easyshop.core.interfaces.catalog.ICategory",
            sort_on = "sortable_title")
        
        return brains

    def moveToCategory(self):
        """
        """
        return self._changeCategories("move")

    def addToCategory(self):
        """
        """
        return self._changeCategories("add")
    
    def deleteCategories(self):
        """
        """
        target_categories = self.request.form.get("target_category", "no-category")
        if not isinstance(target_categories, (list, tuple)):
            target_categories = (target_categories,)

        uids = self.request.get("selected_uids", [])
        if (len(target_categories) == 0) or (len(uids) == 0):
            return self._showView()

        reference_catalog = getToolByName(self.context, "reference_catalog")
        catalog = getToolByName(self.context, "portal_catalog")
        
        for brain in catalog.searchResults(UID = target_categories):
            category = brain.getObject()

            for brain2 in catalog.searchResults(UID = uids):
                product = brain2.getObject()
                reference_catalog.deleteReference(category, product, "categories_products")
                product.reindexObject()
                
            category.reindexObject()    

        return self._showView()
        
    def _changeCategories(self, kind):
        """
        """        
        target_categories = self.request.form.get("target_category", [])
        if not isinstance(target_categories, (list, tuple)):
            target_categories = (target_categories,)
        
        new_target_category = self.request.form.get("new_target_category", "")
        
        if (len(target_categories) == 0) and (new_target_category == ""):
            return self._showView()
        
        all_target_categories = []
        if len(target_categories) > 0:
            all_target_categories.extend(target_categories)
        
        if new_target_category != "":
            putils = getToolByName(self.context, "plone_utils")
            normalized_id = putils.normalizeString(new_target_category)
            
            self.context.manage_addProduct["easyshop.core"].addCategory(
                id = normalized_id, title=new_target_category)
                
            new_category = self.context.get(normalized_id)
            all_target_categories.append(new_category)
            
        catalog = getToolByName(self.context, "portal_catalog")
        category_brains = catalog.searchResults(UID = target_categories)
        
        if len(category_brains) == 0:
            return self._showView()
        
        target_categories = [c.getObject() for c in category_brains]
        
        uids = self.request.get("selected_uids", [])
        
        # Products are responsible for managing categories
        for brain in catalog.searchResults(UID = uids):
            product = brain.getObject()
            if kind == "add":
                existing_categories = ICategoryManagement(product).getCategories()
                all_target_categories.extend(existing_categories)
                
            # NOTE: the product is reindexed within "setCategories"
            product.setCategories(all_target_categories)

        return self._showView()

    def addToGroup(self):
        """
        """
        catalog = getToolByName(self.context, "portal_catalog")
        group_name = self.request.form.get("group_name")

        if group_name is not None:
            gm = IGroupManagement(self.context)            
            group = gm.addGroup(group_name)
            
            if group != False:

                products = []
                uids = self.request.get("selected_uids")

                for brain in catalog.searchResults(UID = uids):
                    products.append(brain.getObject())
                    
                group.setProducts(products)

        return self._showView()
                    
    def changePrice(self):
        """
        """
        prices = self.request.form.items()
        
        if prices is None:
            return 

        for uid, price in prices:
            
            if price == "":
                continue
                            
            try:
                price = int(price)
            except:
                continue
                
            catalog = getToolByName(self.context, "portal_catalog")
            brains = catalog.searchResults(UID = uid)
            
            if len(brains) == 1:
                product = brains[0].getObject()
                product.setPrice(price)
                product.reindexObject()
                
        return self._showView()
                                
    def rename(self):
        """
        """
        putils = getToolByName(self.context, "plone_utils")        

        ids  = {}
        titles = {}
        
        # rename products        
        uids = self.request.form.get("selected_uids")
        
        if not isinstance(uids, (list, tuple)):
            uids = (uids,)

        for uid in uids:

            id = self.request.form.get("id-%s" % uid, "")
            title = self.request.form.get("title-%s" % uid, "")
            
            catalog = getToolByName(self.context, "portal_catalog")
            brains = catalog.searchResults(UID = uid)
            
            if len(brains) == 1:
                product = brains[0].getObject()

                if title != "":
                    product.setTitle(title)
                    
                if id != "":
                    putils._renameObject(product, id)
                    
                product.reindexObject()
        
        return self._showView()
        
    def _showView(self):
        """
        """
        products_view = getMultiAdapter((self.context, self.context.request), name="manage-products")
        return products_view()