# zope imports
from zope.component import getMultiAdapter
from zope.interface import implements

# plone imports
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
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
        if len(self.getCategories()) > 0:
            return True
        else:
            return False

    @memoize
    def getCategories(self):
        """
        """
        current_category_uid = self.request.get("uid")
        
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
                    
                    # Title
                    title = category_titles[child_uid]
                    short_title = title
                    if len(short_title)>13:
                        short_title = short_title[:13] + "..."
                    
                    # Current
                    if current_category_uid == child_uid:
                        klass = "navTreeCurrentItem"
                    else:
                        klass = ""
                        
                    children.append({
                        "uid"         : child_uid,
                        "title"       : title,
                        "short_title" : short_title,
                        "amount"      : category_amounts[child_uid],
                        "level"       : category_levels[child_uid],
                        "class"       : klass,
                    })
            
            # Title
            title = category_titles[uid]
            short_title = title            
            if len(short_title)>15:
                short_title = short_title[:15] + "..."

            # Current
            if current_category_uid == uid:
                klass = "navTreeCurrentItem"
            else:
                klass = ""
            
            result.append({
                "uid"         : uid,
                "title"       : title,
                "short_title" : short_title,
                "amount"      : category_amounts[uid],
                "level"       : category_levels[uid],
                "children"    : children,
                "class"       : klass,
            })
        
        return result

class AddForm(base.NullAddForm):
    """
    """
    def create(self):
        """
        """
        return Assignment()