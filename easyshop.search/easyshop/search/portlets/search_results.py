# zope imports
from zope.component import getMultiAdapter
from zope.interface import implements

# plone imports
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

# Five imports
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# easyshop imports
from easyshop.core.config import _
from easyshop.core.interfaces import ICategory
from easyshop.core.interfaces import ICategoryManagement

class ISearchResultsPortlet(IPortletDataProvider):
    """This portlet shows some information about search results
    """

class Assignment(base.Assignment):
    """
    """
    implements(ISearchResultsPortlet)

    def __init__(self):
        """
        """

    @property
    def title(self):
        """
        """
        return _(u"EasyShop: Search Results")

class Renderer(base.Renderer):
    """
    """
    render = ViewPageTemplateFile('search_results.pt')

    @property
    def available(self):
        """
        """
        return True

            
    def getCategories(self):
        """
        """
        view = getMultiAdapter((self.context, self.request), name='search-view')
        brains = view.getSearchResults()

        products = [brain.getObject() for brain in brains]
        
        category_amounts = {}
        category_titles = {}
        category_levels = {}
        category_tops = {}
        
        for product in products:
            cm = ICategoryManagement(product)

            for category in cm.getTopLevelCategories():

                # Traverse to top category
                
                object = category
                while ICategory.providedBy(object) == True:
                    uid = object.UID()
                    category_titles[uid] = object.Title()
                    category_levels[uid] = len(object.getPhysicalPath())
                    
                    if category_amounts.has_key(uid) == False:
                        category_amounts[uid] = 0
                    
                    category_amounts[uid] += 1
                    
                    temp = object
                    object = object.aq_inner.aq_parent
                    
                    if ICategory.providedBy(object) == False:
                        category_tops[uid] = temp
                
        
        result = []
        for uid, category in category_tops.items():

            # Calculate children
            children = []
            for child in category.objectValues("Category"):
                child_uid = child.UID()
                if child_uid in category_titles.keys():
                    children.append({
                        "uid"    : child_uid,
                        "title"  : category_titles[child_uid],
                        "amount" : category_amounts[child_uid],
                        "level"  : category_levels[child_uid]
                    })
                    
            result.append({
                "uid"      : uid,
                "title"    : category_titles[uid],
                "amount"   : category_amounts[uid],
                "level"    : category_levels[uid],
                "children" : children
            })
        
        import pdb; pdb.set_trace()
        return result

class AddForm(base.NullAddForm):
    """
    """
    def create(self):
        """
        """
        return Assignment()