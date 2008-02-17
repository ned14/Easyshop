# Zope imports
from zope.interface import implements
from zope.component import getUtility
from zope.component import getMultiAdapter

# Archetypes imports
from Products.Archetypes.atapi import *

# plone.portlets imports
from plone.portlets.constants import CONTEXT_CATEGORY
from plone.portlets.interfaces import ILocalPortletAssignmentManager
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager

# ATContentTypes imports
from Products.ATContentTypes.content.folder import ATFolder

# easyshop imports
from easyshop.core.interfaces import IImageConversion

from easyshop.catalog.portlets import categories
from easyshop.catalog.portlets import formatter

from easyshop.carts.portlets import cart
from easyshop.customers.portlets import my_account

# easymall imports
from easymall.mall.portlets import shop_admin
from easymall.mall.config import *
from easymall.mall.interfaces import IMallShop

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
        name = "showAddQuantity",
        default=False,
        schemata="misc",
        widget = BooleanWidget(
            description = "If selected, customers can select amount of products which are added to cart.",  
            label="Show Quantity",
            label_msgid="schema_show_quantity_label",
            description_msgid="schema_show_quantity_description",
            i18n_domain="EasyShop",
        ),
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

class MallEasyShop(ATFolder):
    """An shop where one can offer products for sale.
    """
    implements(IMallShop)
    _at_rename_after_creation = True
    schema = schema

    def at_post_create_script(self):
        """Overwritten to create some objects.
        """
        # Add Content Type Registry
        self.manage_addProduct["CMFCore"].manage_addRegistry()
        ctr = self.content_type_registry
        ctr.addPredicate("EasyShopImage", "extension")
        ctr.getPredicate("EasyShopImage").edit("jpg jpeg png gif")
        ctr.assignTypeName("EasyShopImage", "EasyShopImage")
        
        # Add left portlets 
        leftColumn = getUtility(IPortletManager, name=u'plone.leftcolumn', context=self)
        left = getMultiAdapter((self, leftColumn,), IPortletAssignmentMapping, context=self)

        if u'portlets.Admin' not in left:
            left[u'portlets.Admin'] = shop_admin.Assignment()
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

        # Block default portlets
        assignable = getMultiAdapter((self, rightColumn,), ILocalPortletAssignmentManager)
        assignable.setBlacklistStatus(CONTEXT_CATEGORY, True)

        # Create containers
        self.manage_addProduct["easyshop.shop"].addCategoriesContainer(id="categories", title="Categories")
        self.manage_addProduct["easyshop.shop"].addDiscountsContainer(id="discounts", title="Discounts")
        self.manage_addProduct["easyshop.shop"].addProductsContainer(id="products", title="Products")        
        self.manage_addProduct["easyshop.shop"].addStockInformationContainer(id="stock-information", 
            title="Stock Information")    
                
        ### Information
        self.manage_addProduct["easyshop.shop"].addInformationContainer(id="information", title="Information")
        self.information.manage_addProduct["easyshop.shop"].addInformationPage(
            id="terms-and-conditions", title="Terms And Conditions")
        
    def setImage(self, data):
        """
        """
        if data and data != "DELETE_IMAGE":
            data = IImageConversion(self).convertImage(data)
        self.getField("image").set(self, data)        
    
registerType(MallEasyShop, PROJECTNAME)