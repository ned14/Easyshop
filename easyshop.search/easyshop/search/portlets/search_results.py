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
        for product in products:
            cm = ICategoryManagement(product)
            for category in cm.getTopLevelCategories():
                uid = category.UID()
                if category_amounts.has_key(uid) == False:
                    category_amounts[uid] = 0
                    category_titles[uid] = category.Title()
                    
                category_amounts[uid] += 1
                
        
        result = []
        for uid in category_amounts.keys():
            result.append({
                "uid"    : uid,
                "title"  : category_titles[uid],
                "amount" : category_amounts[uid],
            }) 
            
        return result

class AddForm(base.NullAddForm):
    """
    """
    def create(self):
        """
        """
        return Assignment()