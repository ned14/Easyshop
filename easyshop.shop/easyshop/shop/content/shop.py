# Zope imports
from zope.event import notify
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import *

# ATContentTypes imports
from Products.ATContentTypes.content.folder import ATFolder

# easyshop imports
from easyshop.core.config import *
from easyshop.core.interfaces import IShop
from easyshop.core.interfaces import IImageConversion

from easyshop.shop.events import ShopCreatedEvent

schema = Schema((

    StringField(
        name="shopOwner",
        required=True,
        widget=StringWidget(
            label="Shop Owner",
            label_msgid="schema_shop_owner_label",
            description = "",
            description_msgid="schema_shop_owner_description",
            i18n_domain="EasyShop",
        ),
    ),

    BooleanField(
        name="grossPrices",
        default=True,
        schemata="misc",        
        widget=BooleanWidget(
            description = "If selected, all prices are gross prices, else net prices.",
            label="Gross Prices",
            label_msgid="schema_gross_prices_label",
            description_msgid="schema_gross_prices_description",
            i18n_domain="EasyShop",
        ),
    ),
        
    StringField(
        name="currency",
        schemata="misc",
        vocabulary="_getCurrenciesAsDL",
        default="euro",
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
        default=True,
        schemata="misc",
        widget = BooleanWidget(
            description = "If selected, customers can select amount of products which are added to cart.",  
            label="Show Quantity",
            label_msgid="schema_show_quantity_label",
            description_msgid="schema_show_quantity_description",
            i18n_domain="EasyShop",
        ),
    ),
    
    LinesField(
        name="countries",
        schemata="misc",
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
        name="payPalId",
        schemata="payment",
        widget=StringWidget(
            label="PayPal ID",
            label_msgid="schema_paypal_id_label",
            description = "",
            description_msgid="schema_paypal_id_description",
            i18n_domain="EasyShop",
        ),
    ),    

    StringField(
        name="mailFromName",
        schemata="mailing",
        widget=StringWidget(
            label="Mail 'From' Name",
            label_msgid="schema_mail_from_name_label",
            description = "EasyShop generates e-mail using this email as the e-mail sender. Leave it blank to use Plone's default.",
            description_msgid="schema_mail_from_description",
            i18n_domain="EasyShop",
        ),
    ),
    
    StringField(
        name="mailFromAddress",
        schemata="mailing",
        widget=StringWidget(
            label="EasyShop 'From' Address",
            label_msgid="schema_mail_from_address_label",
            description = "Plone generates e-mail using this address as the e-mail sender. Leave it blank to use Plone's default.",
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
            description = "To this mail addresses all shop relevant mails (e.g. order has been submitted) are sent. Leave it blank to use Plone's default.",
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
        ctr.addPredicate("EasyShopImage", "extension")
        ctr.getPredicate("EasyShopImage").edit("jpg jpeg png gif")
        ctr.assignTypeName("EasyShopImage", "EasyShopImage")
        
        # Shoot event
        notify(ShopCreatedEvent(self))
        
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