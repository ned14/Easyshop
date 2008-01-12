# zope imports
from zope.interface import implements

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import IImageManagement

class ImageManagement:
    """Provides IImageManagement for several classes.
    """
    implements(IImageManagement)
    
    def __init__(self, context):
        """
        """
        self.context = context

    def getMainImage(self):
        """Returns the main image. This is either the product itself or the 
        first image object within the product.
        """ 
        # Returns the object, which contains the image field (not the image
        # field itself), to be able to get image_shop_large. etc.
        image = self.context.getField("image").get(self.context)
        if len(image) != 0:
            return self.context
        else:
            try:
                return self.context.objectValues("EasyShopImage")[0]
            except IndexError:
                return None
                
    def getImages(self):
        """Returns all images.
        """
        result = []
        image = self.context.getField("image").get(self.context)
        if len(image) != 0:
            result.append(self.context)
        
        result.extend(self.context.objectValues("EasyShopImage"))
        return result
        
    def hasImages(self):
        """Returns True if at least one image exists.
        """
        return len(self.getImages()) > 0