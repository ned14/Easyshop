## Controller Python Script ""
##bind container=container
##bind context=context
##bind script=script
##bind subpath=traverse_subpath
##parameters= goto
##title=

if goto == "overview":
    return state.set(status="goto_overview")
if goto == "addressbook":
    return state.set(status="goto_addressbook")
if goto == "manage_payment_methods":
    return state.set(status="goto_manage_payment_methods")
    
    
