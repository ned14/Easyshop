# zope imports
from zope.interface import implements
from zope.component import adapts

# easyshop imports
from easyshop.core.interfaces import IData
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import IImageManagement
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IProduct
from easyshop.core.interfaces import IProductVariant
from easyshop.core.interfaces import IProductVariantsManagement

class ProductData(object):
    """An adapter which provides IData for product content objects.
    """    
    implements(IData)
    adapts(IProduct)

    def __init__(self, context):
        """
        """
        self.context = context
    
    def asDict(self):
        """
        """
        pvm = IProductVariantsManagement(self.context)
        
        if pvm.hasVariants() == True:
            variant = pvm.getSelectedVariant() or pvm.getDefaultVariant()
            return IData(variant).asDict()
        else:
            # price
            cm    = ICurrencyManagement(self.context)
            price = IPrices(self.context).getPriceForCustomer()
            price = cm.priceToString(price)

            # image
            image = IImageManagement(self.context).getMainImage()
            if image is not None:
                image = "%s/image_%s" % (image.absolute_url(), "preview")

            images = []
            for temp in IImageManagement(self.context).getImages():
                images.append("%s/image_tile" % temp.absolute_url())
            
            return {
                "article_id"  : self.context.getArticleId(),                
                "title"       : self.context.Title(),
                "short_title" : self.context.getShortTitle() or self.context.Title(),
                "description" : self.context.Description(),
                "url"         : self.context.absolute_url(),
                "price"       : price,
                "image"       : image,
                "images"      : images,
                "text"        : self.context.getText(),
                "short_text"  : self.context.getShortText(),
            }        
        
class ProductVariantData:
    """An adapter which provides IData for product variant content objects.
    """    
    implements(IData)
    adapts(IProductVariant)

    def __init__(self, context):
        """
        """
        self.context = context
        self.parent = context.aq_inner.aq_parent
        
    def asDict(self):
        """
        """
        # NOTE: The replacement of "%P" for title is made within ProductVariant
        # content type.
        
        # NOTE: The IImageManagement adapter is doing the check which image is 
        # to display: variant vs. parent
        
        # image
        image = IImageManagement(self.context).getMainImage()
        if image is not None:
            image = "%s/image_%s" % (image.absolute_url(), "preview")
        
        images = []
        for temp in IImageManagement(self.context).getImages():
            images.append("%s/image_tile" % temp.absolute_url())
        
        # title 
        title = self.context.Title() or self.parent.Title()
        
        # short title
        short_title = self.context.getShortTitle() or \
                      self.parent.getShortTitle() or \
                      title

        if "%" in short_title:
            short_title = short_title.replace("%P", self.parent.getShortTitle())
        
        # article id
        article_id = self.context.getArticleId() or \
                     self.parent.getArticleId()
                     
        if "%" in article_id:
            article_id = article_id.replace("%P", self.parent.getArticleId())
                     
        # Text 
        text = self.context.getText() or self.parent.getText()
        if "%" in text:
            text = text.replace("%P", self.parent.getText())

        # Short Text 
        short_text = self.context.getShortText() or self.parent.getShortText()
        if "%" in short_text:
            short_text = short_text.replace("%P", self.parent.getShortText())
        
        # Description
        description = self.context.Description() or self.parent.Description()
        if "%" in description:
            description = description.replace("%P", self.parent.Description())
        
        # options
        options = []
        for option in self.context.getForProperties():
            name, value = option.split(":")
            options.append({
                "name" : name,
                "value" : value,
            })
        
        return {
            "article_id"  : article_id,
            "title"       : title,            
            "short_title" : short_title,
            "description" : description,
            "url"         : self.context.absolute_url(),
            "image"       : image,
            "images"      : images,
            "text"        : text,
            "short_text"  : short_text,
            "options"     : options,
        }