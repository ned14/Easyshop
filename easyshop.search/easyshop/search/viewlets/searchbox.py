# plone imports
from plone.app.layout.viewlets.common import SearchBoxViewlet as Base

# Five imports
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# CMFCore imports
from Products.CMFCore.utils import getToolByName

class SearchBoxViewlet(Base):
    """
    """
    render = ViewPageTemplateFile('searchbox.pt')
    
    def getShopUrl(self):
        """
        """
        ptool = getToolByName(self.context, "portal_properties")
        return ptool.site_properties.easyshop_path