# zope imports
from zope.interface import implements

# easyshop imports
from easyshop.core.config import *
from easyshop.catalog.interfaces import Product

schema = Schema((
    ReferenceField( 
        name='objectReference', 
        required=True,
        multiValued=0,
        relationship='easyarticle_object',
        widget=ReferenceBrowserWidget(
            label='Products',
            label_msgid='schema_object_reference_label',
            description='',
            description_msgid="schema_object_reference_description",
            i18n_domain='EasyArticle',                    
            show_path=1,
            allow_search=1, 
            allow_browse=1,
            available_indexes={'SearchableText':'Free text search'},
            ),    
    ),    

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
        name='article_id',
        widget=StringWidget(
            label="Article ID",
            label_msgid='schema_article_id_label',
            description="Your unique article id.",
            description_msgid="schema_article_id_description",
            i18n_domain='EasyShop',
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
            label='Short Description',
            label_msgid='schema_short_text_label',
            description="This text is used within overviews, such as category view.",
            description_msgid="schema_short_description_description",
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
        name='priceGross',
        default=0.0,
        widget=DecimalWidget(
            size="10",
            label='Price Gross',
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
        relationship='easyshopcategory_easyshopproduct',
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

))

class ProductReference(Product):
    """A ProductReference makes arbitrary objects buyable.
    """
    implements(IProductReference)
    schema = Product.schema.copy() + schema.copy()

registerType(Product, PROJECTNAME)