## Controller Python Script ""
##bind container=container
##bind context=context
##bind script=script
##bind subpath=traverse_subpath
##parameters=goto=None
##title=

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# get customer
view = getMultiAdapter((context, context.REQUEST), name="checkOutView")

if view.customerHasAddresses() == True:
    state.set(status="addresses-select-form")
else:
    state.set(status="addresses-add-form")
    
return state


