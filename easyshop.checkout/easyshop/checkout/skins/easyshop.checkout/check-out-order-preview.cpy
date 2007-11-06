## Controller Python Script ""
##bind container=container
##bind context=context
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=

# zope imports
from zope.component import getMultiAdapter

# get customer
view = getMultiAdapter((context, context.REQUEST), name="orderPreviewView")
view.buy()

# Otherwise there is a redirection within the buy process to paypal.com
if view.getPaymentMethodType() != "paypal":
    return state