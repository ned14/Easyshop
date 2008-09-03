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
        import pdb; pdb.set_trace()
