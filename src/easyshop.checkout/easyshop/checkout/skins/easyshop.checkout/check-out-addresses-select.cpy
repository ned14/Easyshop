## Controller Python Script ""
##bind container=container
##bind context=context
##bind script=script
##bind subpath=traverse_subpath
##parameters= address_type, selected_shipping_address, selected_invoice_address, goto, also_invoice_address=False
##title=

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# get customer
shop_view = getMultiAdapter((context, context.REQUEST), name="checkOutView")
customer = shop_view.getAuthenticatedCustomer()

# set addresses
customer.setShippingAddressAsString(selected_shipping_address)
customer.setInvoiceAddressAsString(selected_invoice_address)

# figure out next template
if goto == "order-preview":
    return state.set(status="order-preview")
else:
    return state.set(status="success")        