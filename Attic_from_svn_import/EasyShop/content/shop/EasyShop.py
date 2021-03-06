# Zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# ATContentTypes imports
from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.configuration import zconf
from Products.ATContentTypes import ATCTMessageFactory as _

# EasyShop imports
from Products.EasyShop.config import *
from Products.EasyShop.interfaces import IShop
from Products.EasyShop.interfaces import IImageConversion

schema = Schema((

    TextField('text',
              required=False,
              searchable=True,
              primary=True,
              storage = AnnotationStorage(migrate=True),
              validators = ('isTidyHtmlWithCleanup',),
              #validators = ('isTidyHtml',),
              default_output_type = 'text/x-html-safe',
              widget = RichWidget(
                        description = '',
                        label = _(u'label_body_text', default=u'Body Text'),
                        rows = 25,
                        allow_file_upload = zconf.ATDocument.allow_document_upload),
    ),

    StringField(
        name="shopOwner",
        widget=StringWidget(
            label="Shop Owner",
            label_msgid="schema_shop_owner_label",
            description = "",
            description_msgid="schema_shop_owner_description",
            i18n_domain="EasyShop",
        ),
    ),
        
    StringField(
        name="currency",
        schemata = "misc",
        vocabulary="_getCurrenciesAsDL",
        default = "euro",
        widget=SelectionWidget(
            label="Currency",
            label_msgid="schema_currency_label",
            description = "",
            description_msgid="schema_currency_description",
            i18n_domain="EasyShop",
        ),
    ),
    ImageField(
        name='image',
        schemata = "misc",        
        widget=ImageWidget(
            label='Image',
            label_msgid='schema_image_label',
            i18n_domain='EasyShop',
        ),
        storage=AttributeStorage()
    ),    

    BooleanField(
        name = "expandAll",
        schemata = "misc",        
        widget = BooleanWidget(
            description = "If selected, all categories will be displayed expanded.",  
            label="Expand All",
            label_msgid="schema_expand_all_label",
            description_msgid="schema_expand_all_description",
            i18n_domain="EasyShop",
        ),
        default="1",
    ),
    
    BooleanField(
        name = "showNavigationQuantity",
        schemata = "misc",        
        widget = BooleanWidget(
            description = "If selected, the amount of products will be displayed in navigation.",
            label="Show Amount of Products",
            label_msgid="schema_show_amount_of_products_label",
            description_msgid="schema_show_amount_of_products_description",
            i18n_domain="EasyShop",
        ),
        default="1",
    ),
    BooleanField(
        name = "showAddQuantity",
        default="1",        
        schemata = "misc",        
        widget = BooleanWidget(
            description = "If selected, a quantity field is shown to add a product to cart.",  
            label="Show Quantity",
            label_msgid="schema_show_quantity_label",
            description_msgid="schema_show_quantity_description",
            i18n_domain="EasyShop",
        ),
    ),
    
    LinesField(
        name="countries",
        schemata = "misc",
        widget = LinesWidget(
            label="Countries",
            label_msgid="schema_countries_label",
            description = "This countries are offered the customers for selection within address fields.",
            description_msgid="schema_countries_description",
            i18n_domain="EasyShop",
        )
    ),
        
    StringField(
        name="payPalUrl",
        schemata="payment",
        widget=StringWidget(
            label="PayPalUrl",
            label_msgid="schema_paypal_url_label",
            description = "",
            description_msgid="schema_paypal_url_description",
            i18n_domain="EasyShop",
        ),
    ),
    
    StringField(
        name="payPalId",
        schemata="payment",
        widget=StringWidget(
            label="PayPalId",
            label_msgid="schema_paypal_id_label",
            description = "",
            description_msgid="schema_paypal_id_description",
            i18n_domain="EasyShop",
        ),
    ),    
    StringField(
        name="mailFrom",
        schemata="mailing",
        widget=StringWidget(
            label="MailFrom",
            label_msgid="schema_mail_from_label",
            description = "This mail address will be used for the sender.",
            description_msgid="schema_mail_from_description",
            i18n_domain="EasyShop",
        ),
    ),
    
    LinesField(
        name="mailTo",
        schemata="mailing",
        widget=LinesWidget(
            label="MailTo",
            label_msgid="schema_mailto_label",
            description = "To this mail addresses all shop relevant mails are sent.",
            description_msgid="schema_mailto_description",
            i18n_domain="EasyShop",
        ),
    ),
    
),
)

class EasyShop(ATFolder):
    """An shop where one can offer products for sale.
    """
    implements(IShop)
    _at_rename_after_creation = True
    schema = ATFolder.schema.copy() + schema

    def at_post_create_script(self):
        """Overwritten to create some objects.
        """
        # Add Content Type Registry
        self.manage_addProduct["CMFCore"].manage_addRegistry()
        ctr = self.content_type_registry
        ctr.addPredicate("Photo", "extension")
        ctr.getPredicate("Photo").edit("jpg jpeg png gif")
        ctr.assignTypeName("Photo", "Photo")
        
        # Add a formatter
        self.manage_addProduct["EasyShop"].addFormatter(id="formatter", title="Formatter")
        self.formatter.reindexObject()
            
    def setImage(self, data):
        """
        """
        if data and data != "DELETE_IMAGE":
            data = IImageConversion(self).convertImage(data)
        self.getField("image").set(self, data)        
    
    def _getCurrenciesAsDL(self):
        """
        """
        dl = DisplayList()
        
        keys = CURRENCIES.keys()
        keys.sort()
        
        for key in keys:
            dl.add(key, CURRENCIES[key]["long"])

        return dl

registerType(EasyShop, PROJECTNAME)