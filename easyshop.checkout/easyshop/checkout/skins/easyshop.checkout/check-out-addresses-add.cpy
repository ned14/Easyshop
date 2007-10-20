## Controller Python Script ""
##bind container=container
##bind context=context
##bind script=script
##bind subpath=traverse_subpath
##parameters= address_type, firstname, lastname, address1, address2, zipcode, city, country, phone, also_invoice_address="yes", goto=None
##title=

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# get customer
view = getMultiAdapter((context, context.REQUEST), name="checkOutView")
customer = view.getAuthenticatedCustomer()

# add address
id = context.generateUniqueId("Address")

customer.invokeFactory("Address", id=id, title=address1)
address = getattr(customer, id)        

# set data
address.setFirstname(firstname)
address.setLastname(lastname)
address.setAddress1(address1)
address.setAddress2(address2)
address.setZipCode(zipcode)
address.setCity(city)
address.setCountry(country)
address.setPhone(phone)

# set appropriate address type    
if address_type=="shipping":
    customer.setShippingAddressAsString(id)
    if also_invoice_address == "yes":
        customer.setInvoiceAddressAsString(id)
        
    # member=context.portal_membership.getAuthenticatedMember()
    # if member.getProperty('firstname') == "":
    #     member.setProperties({
    #         "firstname" : firstname,
    #         "lastname"  : lastname,
    #     })

else:
    customer.setInvoiceAddressAsString(id)

if address_type == "shipping":
    if also_invoice_address == "yes":
        if goto == "order-preview":
            return state.set(status="order_preview")
        else:            
            return state.set(status="payment_methods")
    else:
        return state.set(status="addresses_add", address_type="invoice", goto=goto)
            
if address_type == "invoice":
    if goto == "order-preview":
        return state.set(status="order_preview")
    else:
        return state.set(status="payment_methods")
