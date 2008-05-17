# zope imports
from zope import schema
from zope.interface import Interface
from zope.interface import Attribute
from zope.app.file.interfaces import IImage

# easyshop.core imports
from easyshop.core.config import _

################################################################################
# Formatter        
################################################################################
    
class IFormatter(Interface):
    """Marker interface to mark formatter content objects.
    
    A formatter provides informations of how products of a shop/category/selector
    are displayed. The first formatter which is found is taken. Is no formatter
    is found default values are taken.
    """

class IFormats(Interface):
    """Provides methods to get an formater resp. formatter infos.
    """    
    def getFormats():
        """Returns the infos of the found formatter as dict.
        """

    def setFormats(data):
        """Sets format with given data. Data has to be dictionary.
        """

class IFormatable(Interface):
    """Marker interface to mark objects as formatable.
    """
    
################################################################################
# Category        
################################################################################
        
class ICategory(IFormatable):
    """Marker interface to mark category content objects. 

    A Category groups arbitrary Products together.
    
    Categories are visible to Customer and mainly used to structure 
    Products. A user of a shop may browse through Products via Categories.
       
    Categories may have sub-categories. 
       
    A product can have more than one category.

    categories may assigned special taxes, shipping prices, discounts and 
    similiar.
    """
    
class ICategoryManagement(Interface):
    """Provides methods to manage category content objects.
    """
    def getCategories():
        """Returns all categories of context as brains.
        """

    # TODO: Change to brains?
    def getTopLevelCategories(self):
        """Returns the top level categories of context. 
        
        Note: The adapter for products returns real objects here (not brains), 
        because of the using of getBRefs which returns real objects. The 
        adapters for shop and categories return brains. This is inconsistent but
        needed (e.g. in the categories portlet) for speed reasons and intended 
        to change soon.
        """
        
class ICategoriesContainer(Interface):
    """A marker interface for categories containers.
    """

################################################################################
# Image        
################################################################################

class IEasyShopImage(Interface):
    """Marker interface for a  image content objects.
    """                                       
    
class IImageConversion(Interface):
    """Provides methods to convert an image. 
    """
    def convertImage(image):
        """Convert given image.
        """
        
class IImageManagement(Interface):
    """Provides methods to manage image content objects.
    """    
    def getMainImage():
        """Return the main image.
        """    

    def getImages():
        """Returns all images.
        """
        
    def hasImages():
        """Returns True if at least one image exists.
        """        

################################################################################
# Product        
################################################################################
        
class IProduct(Interface):
    """Products are sold in the shop.
    """
    description = schema.Text(
        title=_(u"Description"),
        description=_(u"A short description, which is displayed in search results"),
        default=u"",
        required=False,
    )

    articleId = schema.TextLine(
        title=_(u"Article Id"),
        description=_(u"External unique id of the product"),
        default=u"",
        required=False,
    )

    shortTitle = schema.TextLine(
        title=_(u"Short Title"),
        description=_(u"Short title of the product, which can be displayed in overviews"),
        default=u"",
        required=False,
    )
        
    shortText = schema.TextLine(
        title=_(u"Short Text"),
        description=_(u"A short text of the product, which can be displayed in overviews"),
        default=u"",
        required=False,
    )

    text = schema.TextLine(
        title=_(u"Text"),
        description=_(u"A text of the product, which is displayed in detailed views"),
        default=u"",
        required=False,
    )

    # image = schema.Object(
    #     title=_(u"Text"),
    #     schema = IImage,
    #     description=_(u"The main image of the product"),
    #     required=False,
    # )
    # 
    unlimitedAmount = schema.Bool(
        title=_(u"Unlimited Amount"),
        description=_(u"If selected, the stock amount of the product is not decreased."),
        default=False,
        required=False,
    )

    stockAmount = schema.Float(
        title=_(u"Stock Amount"),
        description=_(u"The amount of this product in stock. This number is decreased automatically when the product has been sold."),
        default=0.0,
        required=False,
    )

    weight = schema.Float(
        title=_(u"Weight"),
        description=_(u"The weight of the product."),
        default=0.0,
        required=False,
    )

    price = schema.Float(
        title=_(u"Price"),
        description=_(u"The price of the product."),
        default=0.0,
        required=False,
    )
    
    forSale = schema.Bool(
        title=_(u"For Sale"),
        description=_(u"If selected the sale price is active and displayed additionally."),
        default=False,
        required=False,
    )
    
    salePrice = schema.Float(
        title=_(u"Sale Price"),
        description=_(u"The sale price of the product."),
        default=0.0,
        required=False,
    )

    
class IProductManagement(Interface):
    """Provides methods to handle product content objects.
    """
    
    def getAllProducts():
        """Returns all products (top and sub levels).
        """
        
    def getAmountOfProducts():
        """Returns the amount products.
        """        

    def getProducts():
        """Returns top level products.
        """

    def getTotalAmountOfProducts():
        """Returns the amount of products of all subcategories.
        """
        
class IProductsContainer(Interface):
    """Marker interface for product folder content objects.
    """    

################################################################################
# ProductVariants        
################################################################################

class IProductVariant(IProduct):
    """Marker interface to mark product variant content objects.
    """

class IProductVariantsManagement(Interface):
    """Provides methods to manage product variants.
    """
    def addVariants(title, properties):
        """Adds a product variant.
        """
    
    def deleteVariants(ids):
        """Deletes variants with given ids.
        """
        
    def getDefaultVariant():
        """Returns the default product variant.
        """
    
    def getVariants():
        """Returns existing product variants.
        """

    def getSelectedVariant(properties):
        """Returns selected product.
        """

    def hasVariant(properties):
        """Returns True if a variant with given properties exists.
        """

    def hasVariants():
        """Returns True if context has at least one variant.
        """
        
################################################################################
# Property        
################################################################################

class IProperty(Interface):
    """A property for various content objects.
    """
    
class IPropertyOption(Interface):
    """A property for various content objects.
    """
    
class IPropertyManagement(Interface):
    """Provides methods to manage property content objects.
    """ 
    def getOptionsForProperty(property_id):
        """Return all options of the given property id.
        """
        
    def getPriceForCustomer(property_id, option_name):
        """Returns the customer price of a context's property with given id and
        option name.
        
        The tax for property is the same for its product.
        """
       
    def getPriceGross(property_id, option_name):
        """Returns the gross price of a context's property with given id and
        option name.
        """

    def getPriceNet(property_id, option_name):
        """Returns the net price of a context's property with given id and
        option name.
        
        The tax for property is the same for its product.
        """

    def getProperties():
        """Returns all properties.
        """
        
    def getProperty(id):
        """Returns the property with given title.
        
        Using title, because then a property could be deleted and added
        again. This wouldn't work with id or uid.
        
        This requires, that title per property is unique. This will be done in
        edit view.
        """

    def getTitlesByIds(property_id, option_id):
        """Returns the titles of property and option with given id.
        """
################################################################################
# Selector        
################################################################################

class IProductSelector(IFormatable):
    """A marker interface for product selector content objects.
    """
        