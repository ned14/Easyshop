## Controller Python Script "NAME"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=TITLE
##
   
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFCore.utils import getToolByName

rtool = getToolByName(context, "portal_registration")    

errors = {}
if context.REQUEST.get('firstname', "") == "":
    errors["firstname"] = _("Firstname is required. Please correct.")

if context.REQUEST.get('lastname', "") == "":
    errors["lastname"] = _("Lastname is required. Please correct.")

email = context.REQUEST.get('email', "")
if rtool.isValidEmail(email) == False:
    errors["email"] = _(u'You entered an invalid email address.')
    
if errors:
    return state.set(status="failure", errors=errors, portal_status_message=_('Please correct the indicated errors'))
else:
    return state.set(status="success")
