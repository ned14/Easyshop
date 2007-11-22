# coding=utf-8
import os
from Globals import package_home
from Products.CMFCore.permissions import setDefaultRoles

# MessageFactory
from zope.i18nmessageid import MessageFactory
_ = MessageFactory("EasyShop")

PROJECTNAME = "easyshop.shop"

# Permissions
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner'))
ADD_CONTENT_PERMISSIONS = {
    "Customer" : "EasyShop: Add Customer",
    "Address"  : "EasyShop: Add Address",
    "EasyShop" : "EasyShop: Add EasyShop",
}

setDefaultRoles('EasyShop: Add Customer', ('Manager',))

# Create path to default shop form
product_globals = globals()
home = package_home(product_globals)
DEFAULT_SHOP_FORM = os.path.sep.join([home, "browser", "default_shop_form.pt"])


MESSAGES = {
    "CART_ADDED_PRODUCT"    : "The product has been added to the cart.",
    "CART_INCREASED_AMOUNT" : "The amount of the product has been increased.",
    "ORDER_RECEIVED"        : "Your order has been received. Thank you!",    
}

JAVASCRIPTS = [
    {'id': 'easyshop.js'}
]

STYLESHEETS = [
    {'id': 'easyshop.css'},
    # {'id' : 'easyshop.kss', 'rel': 'k-stylesheet'},
]

IMAGE_SIZES = {'large'   : (768, 768),
               'preview' : (400, 400),
               'mini'    : (200, 200),
               'thumb'   : (128, 128),
               'tile'    : (64, 64),
               'icon'    : (32, 32),
               'listing' : (16, 16),
               }

TEXTS = (
    ("none", "None"),
    ("description", "Description"),
    ("short_text", "Short Text"),        
    ("text", "Long Text"),      
)
                         
CURRENCIES = {
    "euro" : {
        "long"   : "Euro",
        "short"  : "EUR",
        "symbol" : "€"
    },
    
    "usd" : {
        "long"   : "US-Dollar",
        "short"  : "USD",
        "symbol" : "$"
    },    
}

REDO_PAYMENT_STATES = [
    "pending",
    "sent (not payed)",
]

REDO_PAYMENT_PAYMENT_METHODS = [
    "paypal"
]

CREDIT_CARDS_CHOICES = {
    _(u"Visa"): u"Visa",
    _(u"MasterCard/EuroCard"): u"MasterCard/EuroCard",
    _(u"American Express"): u"American Express",
}

CREDIT_CARD_MONTHS_CHOICES = (
    (u"01", u"01"),    
    (u"02", u"02"),
    (u"03", u"03"),
    (u"04", u"04"),    
    (u"05", u"05"),
    (u"06", u"06"),
    (u"07", u"07"),    
    (u"08", u"08"),
    (u"09", u"09"),
    (u"10", u"10"),    
    (u"11", u"11"),
    (u"12", u"12"),
)

CREDIT_CARD_YEARS_CHOICES = (
    (u"2007", u"2007"),    
    (u"2008", u"2008"),
    (u"2009", u"2009"),
    (u"2010", u"2010"),    
    (u"2011", u"2011"),
)