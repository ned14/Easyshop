# kss imports
from plone.app.kss.plonekssview import PloneKSSView
from kss.core import kssaction

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
# from easyshop.core.config import MESSAGES
from easyshop.core.interfaces import IFormats
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IShopManagement

class FormatterKSSView(PloneKSSView):
    """
    """
    @kssaction
    def saveFormatter(self, form, portlethash):
        """
        """
        fi = IFormats(self.context)        
        fi.setFormats(form)
        
        kss_core  = self.getCommandSet("core")
        kss_zope  = self.getCommandSet("zope")
        kss_plone = self.getCommandSet("plone")

        selector = kss_core.getHtmlIdSelector("mycategories")
        kss_zope.refreshViewlet(selector,
                                manager="easyshop.easyshop-manager",
                                name="easyshop.categories")
         
        kss_plone.refreshPortlet(portlethash)