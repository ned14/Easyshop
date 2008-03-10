# zope imports
from zope.component import adapts
from zope.interface import implements

# EasyArticle imports
from easyarticle.core.interfaces import IData
from easyarticle.core.adapters.data import GenericData

# easyarticle imports
from easyshop.easyarticle.interfaces import IESReference
from easyshop.easyarticle.interfaces import IESImage

# easyshop imports
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import IImageManagement
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IProduct

class ESImageData(GenericData):
    """
    """
    implements(IData)
    adapts(IESImage)

    def getContent(self):
        """
        """
        # Adding the background color of the image
        aDict = super(ESImageData, self).getContent()
        aDict["background_color"] = self.context.getBackgroundColor()

        # Set text
        aDict["text"] = self.context.getText()
        
        # Set link to which the image refers
        try:
            aDict["url"] = self.context.getRelatedObject().absolute_url()
        except AttributeError:
            aDict["url"] = None
        
        # Set image data
        aDict["image_url"]  = self.context.absolute_url()
        aDict["image_size"] = self.context.getImageSize()
        
        return aDict
                
class ESReferenceData(GenericData):
    """
    """
    implements(IData)
    adapts(IESReference)

    def __init__(self, context):
        """        
        """
        self.context = context
        self.object  = context.getObjectReference()
        
    def getContent(self):
        """
        """
        data = {}

        # Title
        if self.context.getOverwriteTitle() == True:
            title = self.context.Title()
        else:
            title = self.object.Title()

        # Text
        if self.context.getOverwriteText() == True:
            text = self.context.getText()
        else:
            text = self.object.getText()

        # Image    
        if len(self.context.getImage()) != 0:
            image = self.context
        else:
            image = IImageManagement(self.object).getMainImage()
        
        if image is not None:
            image_url = image.absolute_url()

        # Price
        if IProduct.providedBy(self.object) == True:
            cm = ICurrencyManagement(self.object)            
            p = IPrices(self.object)

            # Effective price
            price = p.getPriceForCustomer()
            price = cm.priceToString(price, symbol="symbol", position="before")
        
            # Standard price
            standard_price = p.getPriceForCustomer(effective=False)
            standard_price = cm.priceToString(
                standard_price, symbol="symbol", position="before")
        
        else:
            standard_price = "0.0"
            price = "0.0"
            
        data.update({
            "portal_type"    : self.object.getPortalTypeName(),
            "id"             : self.object.getId(),
            "url"            : self.object.absolute_url(),
            "title"          : title,
            "description"    : self.object.Description(),
            "text"           : text,
            "image_url"      : image_url,
            "price"          : price,
            "standard_price" : standard_price,
            "for_sale"       : self.object.getForSale(),
            "image_size"     : self.context.getImageSize(),
        })

        return data