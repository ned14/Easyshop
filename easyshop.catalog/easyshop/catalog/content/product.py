# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.folder import ATFolder

# ATBackRef imports
from Products.ATBackRef.BackReferenceField import *
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget

# easyshop imports
from easyshop.core.config import *
from easyshop.core.interfaces import ICategory
from easyshop.core.interfaces import IImageConversion
from easyshop.core.interfaces import IProduct
from easyshop.core.interfaces import IShopManagement

schema = Schema((

    StringField(
        name="shortTitle",
        widget=StringWidget(
            label="ShortTitle",
            label_msgid="schema_short_title_label",
            description = "A short title, which may displayed in overviews. If it is empty the standard title field is used.",
            description_msgid="schema_short_title_description",
            i18n_domain="EasyShop",
        ),
    ),

    StringField(
        name='articleId',
        widget=StringWidget(
            label="Article ID",
            label_msgid='schema_article_id_label',
            description="Your unique article id.",
            description_msgid="schema_article_id_description",
            i18n_domain='EasyShop',
        )
    ),
    
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
            description="This text is used within overviews, such as category view.",
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
            description="This text is used within the product view.",
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

    FloatField(
        name='weight',
        default=0.0,
        widget=DecimalWidget(
            label="Weight",
            label_msgid="schema_weight_label",
            description = "The weight of the product.",
            description_msgid="schema_weight_description",
            i18n_domain="EasyShop",
        ),
    ),
    
    FloatField(
        name='price',
        default=0.0,
        widget=DecimalWidget(
            size="10",
            label='Price',
            label_msgid='schema_price_gross_label',
            i18n_domain='EasyShop',
        )
    ),
    
    ReferenceField( 
        name='relatedProducts',
        multiValued=1,
        relationship='easyshopproduct_easyshopproducts',
        allowed_types=("Product",),
        widget=ReferenceBrowserWidget(
            label="Related Products",
            label_msgid="schema_related_products_label",
            description='Please select all products, which should be associated with this product.',
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
    
    BackReferenceField( 
        name='easyshopcategories', 
        multiValued=1,
        relationship='category_products',
        allowed_types=("Category",),
        widget=BackReferenceBrowserWidget(
            label="Categories",
            label_msgid="schema_categories_label",
            description='Please select all catgories, which should be associated with this product.',
            description_msgid="schema_categories_description",        
            i18n_domain='EasyShop',            
            show_path=1,        
            allow_search=1, 
            allow_browse=1,
            allow_sorting=1,             
            restrict_browsing_to_startup_directory=1,
            startup_directory="getStartupDirectoryForCategories",
            available_indexes={'Title'         : "Product's Title",
                               'SearchableText':'Free text search',
                               'Description'   : "Object's description"},
            ),    
    ),        
    BackReferenceField( 
        name='easyshopgroups',
        multiValued=1,
        relationship='group_product',
        allowed_types=("ProductGroup",),
        widget=BackReferenceBrowserWidget(
            label="Groups",
            label_msgid="schema_groups_label",
            description='Please select all groups, which should be associated with this product.',
            description_msgid="schema_groups_description",
            i18n_domain='EasyShop',            
            show_path=1,        
            allow_search=1, 
            allow_browse=1,
            allow_sorting=1,             
            restrict_browsing_to_startup_directory=1,
            startup_directory="getStartupDirectoryForGroups",
            available_indexes={'Title'         : "Product's Title",
                               'SearchableText':'Free text search',
                               'Description'   : "Object's description"},
            ),    
    ),        
),
)

class Product(ATFolder):
    """A Product is offered for sale.
    """
    implements(IProduct)
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
        
    def getStartupDirectoryForCategories(self):
        """
        """
        shop = IShopManagement(self).getShop()
        return "/".join(shop.getPhysicalPath()) + "/categories"
        
    def getStartupDirectoryForGroups(self):
        """
        """
        shop = IShopManagement(self).getShop()
        return "/".join(shop.getPhysicalPath()) + "/groups"

    def setEasyshopcategories(self, value):
        """
        """
        # save the old categories
        old_categories = self.getEasyshopcategories()

        # Set the new values
        self.getField("easyshopcategories").set(self, value)

        # Reindex to get the new values ...
        self.reindexObject()        
                
        # ... here. Now reindex all categories of this product and all parent 
        # categories of them.
        
        # Todo: Reindex categories which are kept only once.
        for category in old_categories:
            obj = category
            while ICategory.providedBy(obj):
                obj.reindexObject()
                obj = obj.aq_inner.aq_parent
        
        for category in self.getEasyshopcategories():
            obj = category
            while ICategory.providedBy(obj):
                obj.reindexObject()
                obj = obj.aq_inner.aq_parent
        
    def SearchableText(self):
        """
        """
        return " ".join((
            self.Title(),
            self.getShortTitle(),
            self.Description(),
            self.getArticleId(),
        ))
                
registerType(Product, PROJECTNAME)