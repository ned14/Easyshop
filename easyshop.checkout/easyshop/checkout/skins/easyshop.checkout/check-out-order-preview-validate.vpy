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
confirmation = context.REQUEST.get('confirmation', False)

if confirmation == False:
    errors["confirmation"] = "Please confirm our terms and conditions."

if errors:
    return state.set(status="failure", errors=errors, portal_status_message='Please correct the indicated errors.')
else:
    return state.set(status="success")