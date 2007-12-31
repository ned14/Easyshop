# Zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# ATContentTypes imports
from Products.ATContentTypes.content.folder import ATFolder

# easyshop imports
from easyshop.core.config import *
from easyshop.core.interfaces import IShop
from easyshop.core.interfaces import IImageConversion

schema = Schema((

    BooleanField(
        name = "grossPrices",
        widget = BooleanWidget(
            description = "If selected, all prices are gross prices, else net prices.",  
            label="Gross Prices",
            label_msgid="schema_expand_all_label",
            description_msgid="schema_expand_all_description",
            i18n_domain="EasyShop",
        ),
        default="1",
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
        default=DEFAULT_COUNTRIES,
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