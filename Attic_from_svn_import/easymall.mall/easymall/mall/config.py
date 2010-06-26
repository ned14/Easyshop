from Globals import package_home
from Products.CMFCore.permissions import setDefaultRoles

PROJECTNAME = "easymall.mall"
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
ADD_CONTENT_PERMISSIONS = {
    # "EasyMall" : "EasyMall: Add Mall",
}

# setDefaultRoles('EasyMall: Add Mall', ('Manager',))
product_globals = globals()