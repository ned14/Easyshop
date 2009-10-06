# zope imports
from zope import schema
from zope.component import adapts
from zope.formlib import form
from zope.interface import implements
from zope.interface import Interface

# Five imports
from Products.Five.browser import pagetemplatefile
from Products.Five.formlib import formbase

# CMFPlone imports
from Products.CMFPlone.utils import safe_unicode

# easyshop imports
from easyshop.core.config import _
from easyshop.core.interfaces import ICheckoutManagement
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IShippingMethodManagement
from easyshop.core.interfaces import IShop

class IShippingSelectForm(Interface):
    """
    """
    shipping_method  = schema.TextLine()

class ShopShippingSelectForm:
    """
    """
    implements(IShippingSelectForm)
    adapts(IShop)
    
    def __init__(self, context):
        """
        """
        self.context = context
        
    shipping_method  = u""

# Using here Five's EditForm by heart because plone.app.form would lock the shop 
# which is not desired in this case (because the shop is not modified at all)
class ShippingSelectForm(formbase.EditForm):
    """
    """
    template = pagetemplatefile.ZopeTwoPageTemplateFile("shipping.pt")
    form_fields = form.Fields(IShippingSelectForm)

    @form.action(_(u"label_next", default="Next"), condition=form.haveInputWidgets, name=u'next')
    def handle_next_action(self, action, data):
        """
        """
        customer = ICustomerManagement(self.context).getAuthenticatedCustomer()
        customer.selected_shipping_method  = data.get("shipping_method", "")
        
        ICheckoutManagement(self.context).redirectToNextURL("SELECTED_SHIPPING_METHOD")

    def getShippingMethods(self):
        """
        """
        customer = ICustomerManagement(self.context).getAuthenticatedCustomer()
        selected_shipping_id = customer.selected_shipping_method
        
        sm = IShippingMethodManagement(self.context)
        
        shipping_methods = []
        for shipping in sm.getShippingMethods():

            if selected_shipping_id == safe_unicode(shipping.getId()):
                checked = True
            elif selected_shipping_id == u"" and shipping.getId() == "standard":
                checked = True
            else:
                checked = False
                            
            shipping_methods.append({
                "id" : shipping.getId(),
                "title" : shipping.Title,
                "description" : shipping.Description,
                "checked" : checked,
            })
            
        return shipping_methods