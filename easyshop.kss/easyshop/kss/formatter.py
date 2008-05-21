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
    def saveFormatter(self, portlethash):
        """
        """
        fi = IFormats(self.context)
        fi.setFormats(self.request.form)
        
        kss_core  = self.getCommandSet("core")
        kss_zope  = self.getCommandSet("zope")
        kss_plone = self.getCommandSet("plone")
        
        layout = self.request.form.get("layout")

        if layout == "categories-view":
            kss_zope.refreshViewlet(kss_core.getHtmlIdSelector("categories-list"),
                                    manager="easyshop.categories-manager",
                                    name="easyshop.categories-viewlet")

        elif layout == "products-view":
            kss_zope.refreshViewlet(kss_core.getHtmlIdSelector("products-list"),
                                    manager="easyshop.products-manager",
                                    name="easyshop.products-viewlet")

        elif layout == "product-selector-view":
            kss_zope.refreshViewlet(kss_core.getHtmlIdSelector("products-list"),
                                    manager="easyshop.product-selector-manager",
                                    name="easyshop.product-selector-viewlet")                                    

        # For easyshop.easyarticle
        elif layout == "overview":
            kss_zope.refreshViewlet(kss_core.getHtmlIdSelector("products-list"),
                                    manager="easyshop.products-manager",
                                    name="easyshop.products-viewlet")

        # else:
        #     kss_zope.refreshViewlet(kss_core.getHtmlIdSelector("products-list"),
        #                             manager="easyshop.search-results-manager",
        #                             name="easyshop.search-results-viewlet")

        kss_plone.refreshPortlet(portlethash)