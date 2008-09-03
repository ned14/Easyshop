# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import IImageManagement
from easyshop.core.interfaces import IProductVariant

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
        
        
class ProductVariantImageManagement:
    """Provides IImageManagement for ProductVariant.
    """
    implements(IImageManagement)
    adapts(IProductVariant)
    
    def __init__(self, context):
        """
        """
        self.context = context
        self.parent  = context.aq_inner.aq_parent

    def getMainImage(self):
        """Returns the main image. This is either the product itself or the
        first image object within the product.
        """ 
        # Returns the object, which contains the image field (not the image
        # field itself), to be able to get image_shop_large. etc.
        
        # 1. Try to get the image out of the variant object or the parent 
        # product object
        image = self.context.getField("image").get(self.context)
        if len(image) == 0:
            image = self.parent.getField("image").get(self.parent)

        if len(image) != 0:
            return image

        # TODO: Change to catalog and object_provides
        # 2. Try to get the first sub images.
        images = self.context.objectValues("EasyShopImage")
        if len(images) == 0:
            images = self.parent.objectValues("EasyShopImage")
            
        if len(images) != 0:
            return images[0]
            
        return None
            
    def getImages(self):
        """Returns all images.
        """        
        result = []
        image = self.getMainImage()
        if image is not None:
            result.append(self.context)

        images = self.context.objectValues("EasyShopImage")
        if len(images) == 0:
            images = self.parent.objectValues("EasyShopImage")        
        result.extend(images)
        
        return result
        
    def hasImages(self):
        """Returns True if at least one image exists.
        """
        return len(self.getImages()) > 0