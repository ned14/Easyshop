# zope imports
from zope.interface import implements

# plone imports
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# Five imports
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView

# easyshop imports
from easyshop.core.config import _
from easyshop.core.config import TEXTS, IMAGE_SIZES
from easyshop.core.interfaces import ICategory
from easyshop.core.interfaces import IFormatterInfos
from easyshop.core.interfaces import IShop


class IFormatterPortlet(IPortletDataProvider):
    """
    """

class Assignment(base.Assignment):
    """
    """
    implements(IFormatterPortlet)

    def __init__(self):
        """
        """

    @property
    def title(self):
        """
        """
        return _(u"EasyShop: Formatter")

class Renderer(base.Renderer):
    """
    """
    render = ViewPageTemplateFile('formatter.pt')

    @property
    def available(self):
        """
        """
        mtool = getToolByName(self.context, "portal_membership")
        if not mtool.checkPermission("Manage portal", self.context):
            return False
             
        if (ICategory.providedBy(self.context) or \
            IShop.providedBy(self.context)) == False:
            return False

        if IFormatterInfos(self.context).hasFormatter() == False:
            return False
            
        return True        

    def getFormatInfo(self):
        """
        """
        fi = IFormatterInfos(self.context)
        return fi.getFormatInfosAsDict()

    def getTexts(self):
        """
        """
        fi = IFormatterInfos(self.context)        
        selected_text = fi.getText()
        
        result = []
        for text in TEXTS:        
            result.append({
                "id" : text[0],
                "title" : text[1],
                "selected" : selected_text == text[0],
            })
    
        return result
        
    def getImageSizes(self):
        """
        """
        fi = IFormatterInfos(self.context)        
        selected_size = fi.getImageSize()
        
        sizes = IMAGE_SIZES.keys()
        sizes.sort(lambda a, b: cmp(IMAGE_SIZES[a][0], IMAGE_SIZES[b][0]))

        result = []
        for size in sizes:
            result.append({
                "title" : size,
                "selected" : selected_size == size,
            })
            
        return result

class AddForm(base.NullAddForm):
    """
    """
    def create(self):
        """
        """
        return Assignment()

class FormatterView(BrowserView):
    """
    """
    def saveFormatter(self):
        """
        """
        fi = IFormatterInfos(self.context)
        f = fi.getFormatter()

        products_per_line = self.request.get("products_per_line", 0)
        lines_per_page    = self.request.get("lines_per_page", 0)
        image_size        = self.request.get("image_size", "mini")
        text              = self.request.get("text", "")
        product_height    = self.request.get("product_height", 0)
        
        products_per_line = int(products_per_line)
        lines_per_page    = int(lines_per_page)
        product_height    = int(product_height)
                
        f.setProductsPerLine(products_per_line)
        f.setLinesPerPage(lines_per_page)
        f.setImageSize(image_size)
        f.setProductHeight(product_height)        
        f.setText(text)
                
        referer = self.request.get("HTTP_REFERER", "")
        if referer.find("check-out-thanks") != -1:
            url = referer
        else:
            url = self.context.absolute_url()
                            
        self.request.response.redirect(url)