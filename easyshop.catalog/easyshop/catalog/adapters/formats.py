# zope imports
from persistent.dict import PersistentDict
from zope.annotation.interfaces import IAnnotations
from zope.interface import implements

# easyshop imports
from easyshop.core.interfaces import IFormats
from easyshop.core.interfaces import IShop

KEY = "EASYSHOP_FORMAT"

class FormatterInfos:
    """Provides IFormaterInfos for shop and category content objects.
    """
    implements(IFormats)
     
    def __init__(self, context):
        """
        """
        annotations = IAnnotations(context)
        formats = annotations.get(KEY)

        if formats is None:
            formats = annotations[KEY]  = PersistentDict()

            # Set defaults
            formats["enabled"]           = False
            formats["text"]              = "short_text"
            formats["title"]             = "title"
            formats["chars"]             = "20"
            formats["image_size"]        = "mini"
            formats["lines_per_page"]    = "1"
            formats["products_per_line"] = "2"
            formats["product_height"]    = "0"
            
        self.context = context
        self.formats = formats

    def getFormats(self, effective=True):
        """Returns either the first object with formats enabled or the shop
        content object
        """
        object = self.context
        if effective == True:
            while IShop.providedBy(object) == False:
                try:                 
                    fi = IFormats(object)
                except TypeError:
                    pass
                else:              
                    if fi.formats["enabled"] == True:
                        break
                
                if object.getParentCategory() is not None:
                    object = object.getParentCategory()
                else:
                    object = object.aq_inner.aq_parent
        
        fi = IFormats(object)
        
        try:
            lines_per_page = int(fi.formats["lines_per_page"])
        except (TypeError, ValueError):
            lines_per_page = 1

        try:
            products_per_line = int(fi.formats["products_per_line"])
        except (TypeError, ValueError):
            products_per_line = 2

        try:
            product_height = int(fi.formats["product_height"])
        except (TypeError, ValueError):
            product_height = 0
            
        return {
            "enabled"           : fi.formats["enabled"],
            "lines_per_page"    : lines_per_page,
            "products_per_line" : products_per_line,
            "product_height"    : product_height,
            "image_size"        : fi.formats["image_size"],
            "text"              : fi.formats["text"],            
            "title"             : fi.formats["title"],
            "chars"             : fi.formats["chars"],
        }
        
    def setFormats(self, data):
        """
        """
        # When enabled is checked browsers return "on"; if not browsers return 
        # None. So change "on" to True and None to False here.
        if data.get("enabled", False) != False:
            enabled = True
        else:
            enabled = False
            
        self.formats["enabled"]           = enabled
        self.formats["text"]              = data.get("text")
        self.formats["title"]             = data.get("title")
        self.formats["chars"]             = data.get("chars")
        self.formats["image_size"]        = data.get("image_size")
        self.formats["lines_per_page"]    = data.get("lines_per_page")
        self.formats["products_per_line"] = data.get("products_per_line")
        self.formats["product_height"]    = data.get("product_height")