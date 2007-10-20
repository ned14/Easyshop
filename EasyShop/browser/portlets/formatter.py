# zope imports
from zope.interface import Interface
from zope.interface import implements

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports
from Products.EasyShop.config import *
from Products.EasyShop.interfaces import ICategoryContent
from Products.EasyShop.interfaces import IShop
from Products.EasyShop.interfaces import IFormatterInfos

class IPortletFormatterView(Interface):    
    """
    """
    def getFormatInfos():
        """
        """

    def getImageSizes():
        """
        """

    def getTexts():
        """
        """    
        
    def saveFormatter():
        """
        """

    def showPortlet():
        """
        """
        
class PortletFormatterView(BrowserView):
    """
    """
    implements(IPortletFormatterView)

    def getFormatInfos(self):
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

    def showPortlet(self):
        """
        """
        mtool = getToolByName(self.context, "portal_membership")
        if not mtool.checkPermission("Manage portal", self.context):
            return False
             
        if (ICategoryContent.providedBy(self.context) or \
            IShop.providedBy(self.context)) == False:
            return False

        if IFormatterInfos(self.context).hasFormatter() == False:
            return False
            
        return True