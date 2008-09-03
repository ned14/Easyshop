# zope imports
from zope.annotation.interfaces import IAnnotations

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName


KEY = "EASYSHOP_FORMAT"

class FormatterView(BrowserView):
    """
    """
    def addTitle(self):
        """Adds title to IFormatables
        """
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            object_provides = "easyshop.core.interfaces.catalog.IFormatable"
        )

        for brain in brains:
            object = brain.getObject()
            annotations = IAnnotations(object)
            if annotations.has_key(KEY) == True:
                annotations[KEY]["title"] = "title"
                annotations[KEY]["chars"] = "0"