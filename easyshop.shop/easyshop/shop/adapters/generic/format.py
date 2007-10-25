# zope imports
from zope.interface import implements
from zope.component import adapts
from zope.component.exceptions import ComponentLookupError
  
# easyshop imports
from easyshop.core.config import IMAGE_SIZES
from easyshop.core.interfaces import IFormatter
from easyshop.core.interfaces import IFormatterInfos
from easyshop.core.interfaces import IShop

class FormatterInfos:
    """Provides IFormaterInfos for shipping price content objects.
    """
    implements(IFormatterInfos)
     
    def __init__(self, context):
        """
        """
        self.context = context
        self.formatter = self._getFormatter()

    def getText(self):
        """
        """
        if self.formatter is None:
            return "short_text"
            
        return self.formatter.getText()

    def getFormatter(self):
        """
        """
        return self.formatter
        
    def getFormatInfosAsDict(self):
        """
        """
        return {
            "lines_per_page"    : self.getLinesPerPage(),
            "products_per_line" : self.getProductsPerLine(),
            "image_size"        : self.getImageSize(),
            "text"              : self.getText(),
            "product_height"    : self.getProductHeight(),
        }
    
    def getProductHeight(self):
        """
        """    
        if self.formatter is None:
            return 0
            
        return self.formatter.getProductHeight()
        
    def getLinesPerPage(self):
        """
        """
        if self.formatter is None:
            return 5
            
        return self.formatter.getLinesPerPage()

    def getProductsPerLine(self):
        """
        """
        if self.formatter is None:
            return 1
        
        return self.formatter.getProductsPerLine()

    def getImageSize(self):
        """
        """
        if self.formatter is None:
            return "mini"
        
        return self.formatter.getImageSize()
    
    def hasFormatter(self):
        """
        """    
        try:
            self.context.objectValues("Formatter")[0]
        except IndexError:
            return False
        
        return True
        
    def _getFormatter(self):
        """
        """
        obj = self.context

        while IShop.providedBy(obj) == False:
            try:
                return self.context.objectValues("Formatter")[0]
            except IndexError:
                pass
            
            obj = obj.aq_inner.aq_parent

        # For a shop
        try:
            return obj.objectValues("Formatter")[0]
        except IndexError:
            pass
                    
        return None        