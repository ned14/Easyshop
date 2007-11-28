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
        f = fi.getFormatter()
        
        products_per_line = form.get("products_per_line", 0)
        lines_per_page    = form.get("lines_per_page", 0)
        image_size        = form.get("image_size", "mini")
        text              = form.get("text", "")
        product_height    = form.get("product_height", 0)
        
        products_per_line = int(products_per_line)
        lines_per_page    = int(lines_per_page)
        product_height    = int(product_height)
                
        f.setProductsPerLine(products_per_line)
        f.setLinesPerPage(lines_per_page)
        f.setImageSize(image_size)
        f.setProductHeight(product_height)        
        f.setText(text)
        
        kss_core  = self.getCommandSet("core")
        kss_zope  = self.getCommandSet("zope")
        kss_plone = self.getCommandSet("plone")

        selector = kss_core.getHtmlIdSelector("mycategories")
        kss_zope.refreshViewlet(selector,
                                manager="easyshop.easyshop-manager",
                                name="easyshop.categories")
         
        kss_plone.refreshPortlet(portlethash)