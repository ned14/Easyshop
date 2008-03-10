# zope imports
from zope import schema
from zope.component import adapts
from zope.formlib import form
from zope.interface import Interface
from zope.interface import implements

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# Five imports
from Products.Five.browser import pagetemplatefile
from Products.Five.formlib import formbase

# easyshop imports
from easyshop.core.config import _
from easyshop.core.interfaces import ICheckoutManagement
from easyshop.core.interfaces import IShop

class IUserAddForm(Interface):
    """
    """
    username = schema.TextLine(
        title=_(u'Username'),
        description=_(u"Username"),
        default=u'',
        required=False,
    )

    password_1 = schema.TextLine(
        title=_(u'Password'),
        description=_(u"Please enter your password."),
        default=u'',
        required=False,
    )

    password_2 = schema.TextLine(
        title=_(u'Password Confirmation'),
        description=_(u"Please confirm your password."),
        default=u'',
        required=False,
    )

class ShopUserAddForm:
    """
    """
    implements(IUserAddForm)
    adapts(IShop)
    
    def __init__(self, context):
        """
        """
        self.context = context

    username   = u""
    password_1 = u""
    password_2 = u""
    
class UserAddForm(formbase.AddForm):
    """
    """
    template = pagetemplatefile.ZopeTwoPageTemplateFile("user.pt")
    form_fields = form.Fields(IUserAddForm)
    
    label = _(u"Add User")
    form_name = _(u"Add User")

    @form.action(_(u"label_save", default=u"Save"), condition=form.haveInputWidgets, name=u'save')
    def handle_save_action(self, action, data):
        """
        """
        self.createAndAdd(data)
            
    def createAndAdd(self, data):
        """
        """
        username = data.get("username")        
        username = username.encode("utf-8")  # rtool doesn't understand unicode.        
        
        password = data.get("password_1")
        request  = self.context.REQUEST
        
        rtool = getToolByName(self.context, "portal_registration")
        rtool.addMember(username, password)
        
        utool = getToolByName(self.context, "portal_url")
        portal_url = utool.getPortalObject().absolute_url()

        # Plone's logged_in script (see below) redirects to given came_from, 
        # hence we just have to pass the next url to it to get to the next url 
        # within the checkout process.
        came_from = ICheckoutManagement(self.context).getNextURL("AFTER_ADDED_USER")

        parameters = {
            "came_from"       : came_from,
            "__ac_name"       : username,
            "__ac_password"   : password,
            "form.submitted"  : "1",
            "js_enabled"      : "1",
            "cookies_enabled" : "1",
            "login_name"      : username,
            "pwd_empty"       : "0",
        }

        temp = []
        for key, value in parameters.items():
            if value != "":
                temp.append("%s=%s" % (key, value))

        url = "%s/logged_in?%s" % (portal_url, "&".join(temp))
        request.RESPONSE.redirect(url)        