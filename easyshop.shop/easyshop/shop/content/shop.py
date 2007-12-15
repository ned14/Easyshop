# Zope imports
from zope.interface import implements
from zope.component import getUtility
from zope.component import getMultiAdapter

# Archetypes imports
from Products.Archetypes.atapi import *

# plone.portlets imports
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager

# ATContentTypes imports
from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.configuration import zconf
from Products.ATContentTypes import ATCTMessageFactory as _

# easyshop imports
from easyshop.core.config import *
from easyshop.core.interfaces import IShop
from easyshop.core.interfaces import IImageConversion

from easyshop.catalog.portlets import categories
from easyshop.catalog.portlets import formatter
from easyshop.shop.portlets import admin

from easyshop.carts.portlets import cart
from easyshop.customers.portlets import my_account

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
            description = "If selected, a quantity field is shown to add a product to cart.",  
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

# Move Plone's default fields into one tab, to make some place for own ones.
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

class EasyShop(ATFolder):
    """An shop where one can offer products for sale.
    """
    implements(IShop)
    _at_rename_after_creation = True
    schema = schema

    def at_post_create_script(self):
        """Overwritten to create some objects.
        """
        # Add Content Type Registry
        self.manage_addProduct["CMFCore"].manage_addRegistry()
        ctr = self.content_type_registry
        ctr.addPredicate("Photo", "extension")
        ctr.getPredicate("Photo").edit("jpg jpeg png gif")
        ctr.assignTypeName("Photo", "Photo")
        
        # Set language to neutral as a shop is not translatable.
        self.setLanguage("")

        # Add left portlets
        leftColumn = getUtility(IPortletManager, name=u'plone.leftcolumn', context=self)
        left = getMultiAdapter((self, leftColumn,), IPortletAssignmentMapping, context=self)

        if u'portlets.Admin' not in left:
            left[u'portlets.Admin'] = admin.Assignment()
            order = [left.keys()[-1]]+left.keys()[:-1]
            left.updateOrder(list(order))

        if u'portlets.Categories' not in left:
            left[u'portlets.Categories'] = categories.Assignment()
            order = [left.keys()[-1]]+left.keys()[:-1]
            left.updateOrder(list(order))

        # Add right portlets 
        rightColumn = getUtility(IPortletManager, name=u'plone.rightcolumn', context=self)
        right = getMultiAdapter((self, rightColumn,), IPortletAssignmentMapping, context=self)

        if u'portlets.Formatter' not in right:
            right[u'portlets.Formatter'] = formatter.Assignment()
            order = [right.keys()[-1]]+right.keys()[:-1]
            right.updateOrder(list(order))

        if u'portlets.Cart' not in right:
            right[u'portlets.Cart'] = cart.Assignment()
            order = [right.keys()[-1]]+right.keys()[:-1]
            right.updateOrder(list(order))

        if u'portlets.MyAccount' not in right:
            right[u'portlets.MyAccount'] = my_account.Assignment()
            order = [right.keys()[-1]]+right.keys()[:-1]
            right.updateOrder(list(order))
            
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