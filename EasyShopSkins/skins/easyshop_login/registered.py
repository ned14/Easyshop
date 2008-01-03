# This is used to get rid of the login button after registration
from Products.CMFCore.utils import getToolByName

utool = getToolByName(context, "portal_url")
portal_url = utool.getPortalObject().absolute_url()
came_from  = context.REQUEST.get("came_from", "")

parameters = {
    "came_from"       : came_from,
    "__ac_name"       : context.REQUEST.get("username", ""),
    "__ac_password"   : context.REQUEST.get("password", ""),
    "form.submitted"  : "1",
    "js_enabled"      : "1",
    "cookies_enabled" : "1",
    "login_name"      : context.REQUEST.get("username", ""),
    "pwd_empty"       : "0",
}

temp = []
for key, value in parameters.items():
    if value != "":
        temp.append("%s=%s" % (key, value))

url = "%s/logged_in?%s" % (portal_url, "&".join(temp))
context.REQUEST.RESPONSE.redirect(url)