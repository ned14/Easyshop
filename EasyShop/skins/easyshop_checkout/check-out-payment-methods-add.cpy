## Controller Python Script ""
##bind container=container
##bind context=context
##bind script=script
##bind subpath=traverse_subpath
##parameters= id, account_number="", bank_identification_code="", name="", bankname="", goto=""
##title=

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# get customer
view = getMultiAdapter((context, context.REQUEST), name="checkOutView")
customer = view.getAuthenticatedCustomer()

if id.startswith("direct_debit_new"):
    # add DirectDebit
    id = context.generateUniqueId("DirectDebit")
    customer.invokeFactory("DirectDebit", id=id, title=name)
    direct_debit = getattr(customer, id)        
    direct_debit.setAccountNumber(account_number)
    direct_debit.setBankIdentificationCode(bank_identification_code)
    direct_debit.setBankName(bankname)
    direct_debit.setName(name)
elif id.startswith("direct_debit_existing"):
    id = id.split(":")[1]

customer.setSelectedPaymentMethod(id)

if goto == "":
    return state.set(status="success")
if goto == "overview":
    return state.set(status="goto_overview")
if goto == "manage_paymentmethods":
    return state.set(status="goto_paymentmethods")