# coding=utf-8
from Products.CMFCore.permissions import setDefaultRoles
PROJECTNAME = "EasyShop"

# Permissions
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner'))
ADD_CONTENT_PERMISSIONS = {
    'Customer': 'EasyShop: Add Customer',
}

setDefaultRoles('EasyShop: Add Customer', ('Manager',))

product_globals = globals()

DEPENDENCIES = []
PRODUCT_DEPENDENCIES = []

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

METATYPES_NOT_TO_LIST = ["Photo", 
                         "Product", 
                         "Products",                          
                         "Category",
                         "Customer",
                         "Cart",
                         "CartItem",                         
                         "CustomerTax",
                         "DefaultTax",
                         "ShippingPrice",
                         "CategoryCriteria",
                         "CountryCriteria",
                         "CustomerCriteria",                         
                         "DateCriteria",
                         "GroupCriteria",
                         "ProductCriteria",
                         "Order",
                         "OrderItem",
                         "DirectDebit",
                         "PayPal",                                                                                                                                                                                                                                                          
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
                         
DIRECT_DEBIT = "directdebit"
PREPAYMENT   = "prepayment"   
PAYPAL       = "paypal"

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