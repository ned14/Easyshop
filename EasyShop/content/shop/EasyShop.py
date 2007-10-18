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
from Products.EasyShop.interfaces import IShopContent
from Products.EasyShop.interfaces import IImageConversion
from Products.EasyShop.content.shop import EasyShopBase

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

class EasyShop(ATFolder, EasyShopBase):
    """An shop where one can offer products for sale.
    """
    implements(IShopContent)
    _at_rename_after_creation = True

    schema = ATFolder.schema.copy() + schema

    def at_post_create_script(self):
        """Overwritten to create some containers.
        """        
        
        # Add Content Type Registry
        self.manage_addProduct["CMFCore"].manage_addRegistry()
        ctr = self.content_type_registry
        ctr.addPredicate("Photo", "extension")
        ctr.getPredicate("Photo").edit("jpg jpeg png gif")
        ctr.assignTypeName("Photo", "EasyShopPhoto")
        
        # Add containers
        self.manage_addProduct["EasyShop"].addEasyShopProducts(id="products", title="Products")        
        self.manage_addProduct["EasyShop"].addEasyShopCategories(id="categories", title="Categories")
        self.manage_addProduct["EasyShop"].addEasyShopGroups(id="groups", title="Groups")
        self.manage_addProduct["EasyShop"].addTaxesContainer(id="taxes", title="Taxes")
        self.manage_addProduct["EasyShop"].addEasyShopShippingPrices(id="shippingprices", title="Shipping Prices")
        self.manage_addProduct["EasyShop"].addEasyShopShippingMethods(id="shippingmethods", title="Shipping Methods")
        self.manage_addProduct["EasyShop"].addCartsContainer(id="carts", title="Carts")
        self.manage_addProduct["EasyShop"].addEasyShopOrders(id="orders", title="Orders")
        self.manage_addProduct["EasyShop"].addEasyShopCustomers(id="customers", title="Customers")
        self.manage_addProduct["EasyShop"].addEasyShopPaymentMethods(id="paymentmethods", title="Payment Methods")
        self.manage_addProduct["EasyShop"].addEasyShopPaymentPrices(id="paymentprices", title="Payment Prices")        

        # Add a formatter
        self.manage_addProduct["EasyShop"].addEasyShopFormatter(id="formatter", title="Formatter")
        
        # Todo: This has to be done with workflow
        # Users should be able to modify itselfs. 
        self.customers.manage_permission('Modify portal content', ['Owner'], 1)
        self.orders.manage_permission('Add portal content', ['Member'], 1)

        # payment methods
        self.paymentmethods.manage_addProduct["EasyShop"].addEasyShopPayPal(id="paypal", title="PayPal")
        self.paymentmethods.manage_addProduct["EasyShop"].addEasyShopPaymentValidator(id="direct-debit", title="Direct Debit")
        self.paymentmethods.manage_addProduct["EasyShop"].addEasyShopSimplePaymentMethod(id="prepayment", title="Prepayment")   
        self.paymentmethods.manage_addProduct["EasyShop"].addEasyShopSimplePaymentMethod(id="cash-on-delivery", title="Cash on Delivery")
        
        # Shipping methods
        self.shippingmethods.manage_addProduct["EasyShop"].addEasyShopShippingMethod(id="default", title="Default")
                
        # reindex
        for obj in self.objectValues():
            obj.reindexObject()
            
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