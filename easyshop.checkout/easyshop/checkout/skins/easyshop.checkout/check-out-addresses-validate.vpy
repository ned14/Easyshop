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

if context.REQUEST.get('firstname') == "":
    errors["firstname"] = "This Field is required. Please correct."    

if context.REQUEST.get('lastname') == "":
    errors["lastname"] = "This Field is required. Please correct."

if context.REQUEST.get('address1') == "":
    errors["address1"] = "This Field is required. Please correct."    

if context.REQUEST.get('zipcode') == "":
    errors["zipcode"] = "This Field is required. Please correct."

if context.REQUEST.get('city') == "":
    errors["city"] = "This Field is required. Please correct."

if context.REQUEST.get('country') == "":
    errors["country"] = "This Field is required. Please correct."

if context.REQUEST.get('phone') == "":
    errors["phone"] = "This Field is required. Please correct."


if errors:
    utils = context.plone_utils
    utils.addPortalMessage("Please correct the indicated errors.")
    return state.set(status="failure", errors=errors)
else:
    return state.set(status="success")