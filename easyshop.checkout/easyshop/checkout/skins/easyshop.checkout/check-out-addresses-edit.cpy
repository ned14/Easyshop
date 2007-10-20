## Controller Python Script ""
##bind container=container
##bind context=context
##bind script=script
##bind subpath=traverse_subpath
##parameters= id, firstname, lastname, address1, address2, companyname, zipcode, city, country, phone, also_invoice_address="yes", goto=None
##title=

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName


# get customer
view = getMultiAdapter((
    context.getShop(), 
    context.REQUEST), 
    name="checkOutView")
    
customer = view.getAuthenticatedCustomer()

# get address
address = getattr(customer, id)        

# set data
address.setFirstname(firstname)
address.setLastname(lastname)
address.setCompanyName(companyname)
address.setAddress1(address1)
address.setAddress2(address2)
address.setZipCode(zipcode)
address.setCity(city)
address.setCountry(country)
address.setPhone(phone)

return state.set(status="addresses_select")