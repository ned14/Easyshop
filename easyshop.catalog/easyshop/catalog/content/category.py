# Zope imports
from AccessControl import ClassSecurityInfo

# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import *

# ATContentTypes imports
from Products.ATContentTypes.content.folder import ATFolder

# EasyShop imports
from Products.EasyShop.config import *
from Products.EasyShop.interfaces import IImageConversion
from Products.EasyShop.interfaces import ICategoryContent

schema = Schema((
    TextField(
        name='description',
        widget=TextAreaWidget(
            label='Description',
            label_msgid='schema_help_description',
            description="A short summary of the content",
            description_msgid="schema_help_description",
            i18n_domain='plone',
        )
    ),
    
    TextField(
        name='text',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            description="",
            description_msgid="schema_text_description",        
            label='Long Description',
            label_msgid='schema_text_label',
            i18n_domain='EasyShop',
        ),
        default_output_type='text/html'
    ),

    ImageField(
        name='image',
        sizes= IMAGE_SIZES,
        widget=ImageWidget(
            description="",
            description_msgid="schema_",                
            label='Image',
            label_msgid='schema_image_label',
            i18n_domain='EasyShop',
        ),
        storage=AttributeStorage()
    ),

    ReferenceField( 
        name='easyshopproducts', 
        multiValued=1,
        relationship='easyshopcategory_easyshopproduct',
        allowed_types=("Product",),
        widget=ReferenceBrowserWidget(        
            label='Products',
            label_msgid='schema_products_label',
            description='Please select all products, which should associated with this category.',
            description_msgid="schema_products_description",
            i18n_domain='EasyShop',                    
            show_path=1,        
            allow_search=1, 
            allow_browse=1,
            allow_sorting=1,
            restrict_browsing_to_startup_directory=1,
            startup_directory="getStartupDirectoryForProducts",
            available_indexes={'Title'         : "Product's Title",
                               'SearchableText':'Free text search',
                               'Description'   : "Object's description"},
            ),    
    ),    
    
),
)

class Category(ATFolder):
    """
    """
    implements(ICategoryContent)
    schema = ATFolder.schema.copy() + schema.copy()

    def setImage(self, data):
        """
        """
        if data and data != "DELETE_IMAGE":
            data = IImageConversion(self).convertImage(data)
        self.getField("image").set(self, data)        

    def getStartupDirectoryForProducts(self):
        """
        """
        shop = self.getShop()
        return "/".join(shop.getPhysicalPath()) + "/products"

    def getCategories(self):
        """
        """
        return [c.Title() for c in self.objectValues("Category")]

    def setEasyshopproducts(self, value):
        """
        """
        self.getField("easyshopproducts").set(self, value)
        
        obj = self
        while ICategoryContent.providedBy(obj):
            obj.reindexObject()
            obj = obj.aq_inner.aq_parent
        
                
registerType(Category, PROJECTNAME)