## Script (Python) "validateComment"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##

errors = {}
payment_id = context.REQUEST.get('id', "")

if payment_id == "direct_debit_new":    
    if context.REQUEST.get('bank_identification_code') == "":
        errors["bank_identification_code"] = "BIC is required."

    if context.REQUEST.get('account_number') == "":
        errors["account_number"] = "AC is required."

    if context.REQUEST.get('name') == "":
        errors["name"] = "Name is required."

    if context.REQUEST.get('bankname') == "":
        errors["bankname"] = "Bankname is required."

if errors:
    utils = context.plone_utils
    utils.addPortalMessage("Please correct the indicated errors.")
    return state.set(status="failure", errors=errors)
else:
    return state.set(status="success")