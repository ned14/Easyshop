# zope imports
from zope.component import adapts
from zope.interface import implements

# EasyArticle imports
from Products.EasyArticle.interfaces import IData
from Products.EasyArticle.adapters.data import GenericData

# easyarticle imports
from easyshop.easyarticle.interfaces import IESReference
from easyshop.easyarticle.interfaces import IESImage

# easyshop imports
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import IImageManagement
from easyshop.core.interfaces import IProduct

class ESImageData(GenericData):
    """
    """
    implements(IData)
    adapts(IESImage)

    def getDict(self):
        """
        """
        # Adding the background color of the image
        aDict = super(ESImageData, self).getDict()
        aDict["background_color"] = self.context.getBackgroundColor()
        try:
            aDict["url"] = self.context.getRelatedObject().absolute_url()
        except AttributeError:
            aDict["url"] = None
        
        return aDict
                
class ESReferenceData:
    """
    """
    implements(IData)
    adapts(IESReference)

    def __init__(self, context):
        """        
        """
        self.context = context
        
    def getDict(self):
        """
        """
        object = self.context.getObjectReference()
                
        data = {}

        # Title
        if self.context.getOverwriteTitle() == True:
            title = self.context.Title()
        else:
            title = object.Title()

        # Text
        if self.context.getOverwriteText() == True:
            text = self.context.getText()
        else:
            text = object.getText()

        # Image    
        if len(self.context.getImage()) != 0:
            image = self.context
        else:
            image = IImageManagement(object).getMainImage()
        
        if image is not None:
            image_url = image.absolute_url()

        # Price
        if IProduct.providedBy(object) == True:
            cm = ICurrencyManagement(object)
            price = cm.priceToString(object.getPrice())
        else:
            price = "0.0"
            
        data.update({
            "portal_type" : object.getPortalTypeName(),
            "url"         : object.absolute_url(),
            "title"       : title,
            "description" : object.Description(),
            "text"        : text,
            "image_url"   : image_url,
            "price"       : price,
            "for_sale"    : False,
        })
                        
        return data