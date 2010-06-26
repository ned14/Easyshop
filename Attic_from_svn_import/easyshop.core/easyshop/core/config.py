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

# NOTE: All message have to be in the plone domain.
MESSAGES = {
    "CART_ADDED_PRODUCT"      : "The product has been added to the cart.",
    "CART_INCREASED_AMOUNT"   : "The amount of the product has been increased.",
    "ORDER_RECEIVED"          : "Your order has been received. Thank you!",
    "NO_PRODUCTS_FOUND"       : "No products found.",
    "VARIANT_ADDED"           : "Variant has been added.",
    "VARIANT_ALREADY_EXISTS"  : "Variant already exists.",
    "VARIANTS_DELETED"        : "Variant(s) deleted.",
    "VARIANTS_SAVED"          : "Variant(s) saved.",
    "VARIANT_DONT_EXIST"      : "The selected combination of properties is not available.",    
    "PROPERTY_OPTIONS_SAVED"  : "Option(s) saved.",    
    "ADDED_PRODUCT_PROPERTY"  : "Property has been added",
    "ADDED_PRODUCT_OPTION"    : "Option has been added",
    "CATEGORY_ALREADY_EXISTS" : _("The category aleady exits."),
    "ADDED_CATEGORY"          : _("The category has been added."),
    "DELETED_CATEGORIES"      : _("Categories have been deleted."),
    "SELECTED_CATEGORIES"     : _("Categories have been selected."),
    "MOVED_CATEGORIES"        : _("Categories have been moved."),
    "DESELECT_CATEGORIES"     : _("Categories have been deselected."),
}

IMAGE_SIZES = {'large'   : (768, 768),
               'preview' : (400, 400),
               'mini'    : (200, 200),
               'thumb'   : (128, 128),
               'tile'    : (64, 64),
               'icon'    : (32, 32),
               'listing' : (16, 16),
               }

TITLES = (
    ("title", "Title"),
    ("short_title", "Short Title"),
)

TEXTS = (
    ("none", "None"),
    ("description", "Description"),
    ("short_text", "Short Text"),        
    ("text", "Long Text"),      
)
                         
CURRENCIES = {
    "euro" : {
        "long"   : u"Euro",
        "short"  : u"EUR",
        "symbol" : u"€"
    },
    
    "usd" : {
        "long"   : u"US Dollar",
        "short"  : u"USD",
        "symbol" : u"$"
    },    

    "gbp" : {
        "long"   : u"British Sterling",
        "short"  : u"GBP",
        "symbol" : u"£"
    },
}

VAT_COUNTRIES = { 'AT' : 'Austria',
                  'BE' : 'Belgium',
                  'BG' : 'Bulgaria',
                  'CY' : 'Cyprus',
                  'CZ' : 'Czech Republic',
                  'DE' : 'Germany',
                  'DK' : 'Denmark',
                  'EE' : 'Estonia',
                  'EL' : 'Greece',
                  'ES' : 'Spain',
                  'FI' : 'Finland',
                  'FR' : 'France',
                  'GB' : 'United Kingdom',
                  'HU' : 'Hungary',
                  'IE' : 'Ireland',
                  'IT' : 'Italy',
                  'LT' : 'Lithuania',
                  'LU' : 'Luxembourg',
                  'LV' : 'Latvia',
                  'MT' : 'Malta',
                  'NL' : 'Netherlands',
                  'PL' : 'Poland',
                  'PT' : 'Portugal',
                  'RO' : 'Romania',
                  'SE' : 'Sweden',
                  'SI' : 'Slovenia',
                  'SK' : 'Slovakia'
                 }

REDO_PAYMENT_STATES = [
    "pending",
    "sent (not paid)",
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
    (u"2012", u"2012"),
    (u"2013", u"2013"),
    (u"2014", u"2014"),
    (u"2015", u"2015"),
    (u"2016", u"2016"),
    (u"2017", u"2017"),
    (u"2018", u"2018"),
    (u"2019", u"2019"),
    (u"2020", u"2020"),
)

DEFAULT_COUNTRIES = (
    "Austria",
    "Belgium",
    "Bulgaria",
    "Cyprus",
    "Czech Republic",
    "Denmark",
    "Estonia",
    "Finland",
    "France",
    "Germany",
    "Greece",
    "Hungary",
    "Ireland",
    "Italy",
    "Latvia",
    "Lithuania",
    "Luxembourg",
    "Malta",
    "Netherlands",
    "Poland",
    "Portugal",
    "Romania",
    "Slovakia",
    "Slovenia",
    "Spain",
    "Sweden",
    "United Kingdom",
    "USA",
)


DELIVERY_TIMES_MIN = (
    (u"1",  u"1"),
    (u"2",  u"2"),
    (u"3",  u"3"),
    (u"4",  u"4"),
    (u"5",  u"5"),
    (u"6",  u"6"),
    (u"7",  u"7"),
    (u"8",  u"8"),
    (u"9",  u"9"),                            
)

DELIVERY_TIMES_MAX = (
    (u"1",  u"1"),
    (u"2",  u"2"),
    (u"3",  u"3"),
    (u"4",  u"4"),
    (u"5",  u"5"),
    (u"6",  u"6"),
    (u"7",  u"7"),
    (u"8",  u"8"),
    (u"9",  u"9"),                            
)

DELIVERY_TIMES_UNIT = (
    (u"Days",   _(u"Days")),
    (u"Weeks",  _(u"Weeks")),
)

#PAYPAL_URL = "https://www.sandbox.paypal.com/cgi-bin/webscr"
PAYPAL_URL = "https://www.paypal.com/cgi-bin/webscr"
