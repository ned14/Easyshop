## Controller Python Script ""
##bind container=container
##bind context=context
##bind script=script
##bind subpath=traverse_subpath
##parameters= id, goto=""
##title=

# zope imports
from zope.component import getMultiAdapter

# get customer
view = getMultiAdapter((context, context.REQUEST), name="checkOutView")
customer = view.getAuthenticatedCustomer()
customer.setSelectedShippingMethod(id)

if goto == "":
    return state.set(status="success")
if goto == "order-preview":
    return state.set(status="order-preview")
