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
          
            return {
                "title"       : self.context.Title(),
                "short_title" : self.context.getShortTitle() or self.context.Title(),
                "url"         : self.context.absolute_url(),
                "price"       : price,
                "image"       : image,
                "text"        : self.context.getText(),
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
        # image
        image = IImageManagement(self.context).getMainImage()
        if image is not None:
            image = "%s/image_%s" % (image.absolute_url(), "preview")
        
        # title 
        title = self.context.Title() or self.parent.Title()
        
        # short title
        short_title = self.context.getShortTitle() or \
                      self.parent.getShortTitle() or \
                      title
        
        # article id
        article_id = self.context.getArticleId() or \
                     self.parent.getArticleId()
        # text 
        text = self.context.getText() or self.parent.getText()

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
            "url"         : self.context.absolute_url(),
            "image"       : image,
            "text"        : text,
            "options"     : options,
        }