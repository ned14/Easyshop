# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import *

# CMFCore imports
from Products.CMFCore.utils import getToolByName

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
        name='shortText',
        allowable_content_types=(
            'text/plain', 
            'text/structured',
            'text/html', 
            'application/msword',),
        default_output_type='text/html',            
        widget=RichWidget(
            label='Short Text',
            label_msgid='schema_short_text_label',
            description="This text is used within overviews.",
            description_msgid="schema_short_description_description",
            i18n_domain='EasyShop',
        ),
    ),

    TextField(
        name='text',
        allowable_content_types=(
            'text/plain', 
            'text/structured',
            'text/html', 
            'application/msword',),
        default_output_type='text/html',            
        widget=RichWidget(
            label='Long Text',
            label_msgid='schema_long_text_label',
            description="This text is used within detailed category view.",
            description_msgid="schema_long_description_description",
            i18n_domain='EasyShop',
        ),
    ),

    ImageField(
        name='image',
        sizes= {'large'   : (768, 768),
                'preview' : (400, 400),
                'mini'    : (200, 200),
                'thumb'   : (128, 128),
                'tile'    :  (64, 64),
                'icon'    :  (32, 32),
                'listing' :  (16, 16),
               },
        widget=ImageWidget(
            label='Image',
            label_msgid='schema_image_label',
            i18n_domain='EasyShop',
        ),
        storage=AttributeStorage()
    ),

    ReferenceField(
        name='parentCategory',
        multiValued=0,
        relationship='parent_category',
        allowed_types=("Category",),
        widget=ReferenceBrowserWidget(        
            label='Parent Category',
            label_msgid='schema_categoy_label',
            description='Select the parent category.',
            description_msgid="schema_category_description",
            i18n_domain='EasyShop',                    
            show_path=1,
            allow_search=1, 
            allow_browse=1,
            allow_sorting=1,
            restrict_browsing_to_startup_directory=1,
            startup_directory="getStartupDirectoryForCategories",
            available_indexes={'Title'         : "Categories' Title",
                               'SearchableText':'Free text search',
                               'Description'   : "Object's description"},
            ),
    ),
    
    IntegerField(
        name='positionInParent',
        default="0",
        widget=IntegerWidget(
            visible = {"edit": "invisible", "view": "invisible"},
            label="Position in parent",
            label_msgid="schema_position_in_parent_label",
            description = "The position of the category in parent category",
            description_msgid = "schema_position_in_parent_description",
            i18n_domain="EasyShop",
        ),
    ),
    
    ReferenceField( 
        name='products', 
        multiValued=1,
        relationship='categories_products',
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
    
    def setProducts(self, value):
        """
        """
        old_products = self.getProducts()
        
        # Set the new values
        self.getField("products").set(self, value)

        # Reindex the old products in case a product has been deleted.
        for product in old_products:
            product.reindexObject()
            
        # Reindex all products of the category to update the "categories" index. 
        for product in self.getProducts():
            product.reindexObject()

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
        shop_path = "/".join(shop.getPhysicalPath())
        
        catalog = getToolByName(self, "portal_catalog")
        brains = catalog.searchResults(
            path = shop_path,
            object_provides = "easyshop.core.interfaces.catalog.IProductsContainer"
        )
        
        if len(brains) > 0:
            products_folder = brains[0]
            return products_folder.getPath()
        else:
            return shop_path

    def getStartupDirectoryForCategories(self):
        """
        """
        shop = IShopManagement(self).getShop()
        shop_path = "/".join(shop.getPhysicalPath())
        
        return shop_path
            
registerType(Category, PROJECTNAME)