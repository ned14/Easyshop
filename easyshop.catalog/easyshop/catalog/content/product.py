# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.folder import ATFolder

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# ATReferenceBrowserWidget imports
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
        schemata="advanced",
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
        schemata="advanced",        
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
            label='Text',
            label_msgid='schema_text_label',
            description="This text is used within the detailed product view.",
            description_msgid="schema_text_description",
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

    BooleanField(
        name="unlimitedAmount",
        schemata="advanced",
        widget = BooleanWidget(
            label="Unlimited Amount",
            label_msgid="schema_unlimited_amount_label",
            description = "If selected, the stock amount of the product is not decreased.",
            description_msgid="schema_unlimited_amount_description",
            i18n_domain="EasyShop",
        ),
    ),
    
    FloatField(
        name="stockAmount",
        schemata="advanced",
        default=0.0,
        widget=DecimalWidget(
            label="Stock Amount",
            label_msgid="schema_stock_amount_label",
            description = "The amount of this product in stock. This number is decreased automatically when the product has been sold.",
            description_msgid="schema_stock_amount_description",
            i18n_domain="EasyShop",
        ),
    ),

    FloatField(
        name='weight',
        schemata="advanced",        
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
            label_msgid='schema_price_label',
            i18n_domain='EasyShop',
        )
    ),

    BooleanField(
        name="forSale",
        schemata="advanced",
        widget = BooleanWidget(
            label="For Sale",
            label_msgid="schema_for_sale_label",
            description = "If selected the price is displayed additionally.",
            description_msgid="schema_for_sale_description",
            i18n_domain="EasyShop",
        ),
    ),
    
    FloatField(
        name='salePrice',
        schemata="advanced",
        default=0.0,
        widget=DecimalWidget(
            size="10",
            label='Sale Price',
            label_msgid='schema_sale_price_gross_label',
            i18n_domain='EasyShop',
        )
    ),

    ReferenceField(
        name='relatedProducts',
        schemata="advanced",
        multiValued=1,
        relationship='products_products',
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
    
),
)

schema = ATFolder.schema.copy() + schema

# Dates
schema.changeSchemataForField('effectiveDate',  'plone')
schema.changeSchemataForField('expirationDate', 'plone')
schema.changeSchemataForField('creation_date', 'plone')    
schema.changeSchemataForField('modification_date', 'plone')    

# Categorization
schema.changeSchemataForField('subject', 'plone')
schema.changeSchemataForField('relatedItems', 'plone')
schema.changeSchemataForField('location', 'plone')
schema.changeSchemataForField('language', 'plone')

# Ownership
schema.changeSchemataForField('creators', 'plone')
schema.changeSchemataForField('contributors', 'plone')
schema.changeSchemataForField('rights', 'plone')

# Settings
schema.changeSchemataForField('allowDiscussion', 'plone')
schema.changeSchemataForField('excludeFromNav', 'plone')
schema.changeSchemataForField('nextPreviousEnabled', 'plone')

class Product(ATFolder):
    """A Product is offered for sale.
    """
    implements(IProduct)
    schema = schema
    
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
        
        catalog = getToolByName(self, "portal_catalog")
        brains = catalog.searchResults(
            path = shop_path,
            object_provides = "easyshop.core.interfaces.catalog.ICategoriesContainer"
        )
        
        if len(brains) > 0:
            products_folder = brains[0]
            return products_folder.getPath()
        else:
            return shop_path
        
    def getStartupDirectoryForGroups(self):
        """
        """
        shop = IShopManagement(self).getShop()
        shop_path = "/".join(shop.getPhysicalPath())
        
        catalog = getToolByName(self, "portal_catalog")
        brains = catalog.searchResults(
            path = shop_path,
            object_provides = "easyshop.core.interfaces.groups.IGroupsContainer"
        )
        
        if len(brains) > 0:
            products_folder = brains[0]
            return products_folder.getPath()
        else:
            return shop_path

    def getCategories(self):
        """
        """
        return self.getBRefs("categories_products")
        
    def setCategories(self, categories):
        """
        """
        # Set the new values
        reference_catalog = getToolByName(self, "reference_catalog")
                
        # save the old categories
        old_categories = self.getCategories()
        
        # delete the product from old categories
        for category in old_categories:
            reference_catalog.deleteReference(category, self, "categories_products")

        for category in categories:
            reference_catalog.addReference(category, self, "categories_products")

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
        
        for category in self.getCategories():
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