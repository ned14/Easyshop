# zope imports
from zope.component.exceptions import ComponentLookupError

# kss imports
from plone.app.kss.plonekssview import PloneKSSView
from kss.core import kssaction

# easyshop imports
from easyshop.core.interfaces import IFormats

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

        try:
            kss_zope.refreshViewlet(kss_core.getHtmlIdSelector("products-list"),
                                    manager="easyshop.category-manager",
                                    name="easyshop.category-viewlet")
        except ComponentLookupError:
            kss_zope.refreshViewlet(kss_core.getHtmlIdSelector("products-list"),
                                    manager="easyshop.product-selector-manager",
                                    name="easyshop.product-selector-viewlet")                                    
             
        kss_plone.refreshPortlet(portlethash)