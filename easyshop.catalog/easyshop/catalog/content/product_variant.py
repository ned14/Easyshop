# python imports
import re

# zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.folder import ATFolder

# easyshop imports
from easyshop.core.config import *
from easyshop.core.interfaces import IImageConversion
from easyshop.core.interfaces import IProductVariant

schema = Schema((

    LinesField(
        name="forProperties",        
        widget=LinesWidget(
            visible={'edit':'invisible', 'view':'invisible'},
            label="For Properties",
            label_msgid="schema_for_properties_label",
            description = "",
            description_msgid="schema_for_properties_description",
            i18n_domain="EasyShop",
        ),
    ),

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

),
)

schema = ATFolder.schema.copy() + schema

# Misc
schema["title"].required = False

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

class ProductVariant(ATFolder):
    """A ProductVariant.
    """
    implements(IProductVariant)
    schema = schema
    _at_rename_after_creation = False
    
    def Title(self):
        """
        """
        title = self.getField("title").get(self)
        
        try:
            url = self.REQUEST.get("URL", "")
            if re.search("atct_edit$|manage-variants-view$", url):
                return title
        except AttributeError:
            pass
            
        if "%" in title:
            parent_title = self.aq_inner.aq_parent.Title()
            title = title.replace("%P", parent_title)
    
        return title
        
    def setImage(self, data):
        """
        """
        if data and data != "DELETE_IMAGE":
            data = IImageConversion(self).convertImage(data)
        self.getField("image").set(self, data)

    def SearchableText(self):
        """
        """
        # TODO: Implement.

    def base_view(self):
        """
        """
        properties = {}
        for property in self.getForProperties():
            name, value = property.split(":")
            properties["property_" + name] = value

        parameters = "&".join(["%s=%s" % (k, v) for (k, v) 
                                                in properties.items()])
        parent = self.aq_inner.aq_parent        
        url = parent.absolute_url() + "?" + parameters
                
        self.REQUEST.RESPONSE.redirect(url)
        
registerType(ProductVariant, PROJECTNAME)