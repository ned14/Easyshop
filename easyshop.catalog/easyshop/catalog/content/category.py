# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import *

# ATContentTypes imports
from Products.ATContentTypes.content.folder import ATFolder

# easyshop imports
from easyshop.core.config import *
from easyshop.core.interfaces import IImageConversion
from easyshop.core.interfaces import ICategory
from easyshop.core.interfaces import IShopManagement

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

    ReferenceField( 
        name='products', 
        multiValued=1,
        relationship='category_products',
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
    implements(ICategory)
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
        shop = IShopManagement(self).getShop()
        return "/".join(shop.getPhysicalPath()) + "/products"

registerType(Category, PROJECTNAME)