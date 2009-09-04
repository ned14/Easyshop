from zope.formlib import form

from AccessControl.SecurityManagement import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from AccessControl.User import UnrestrictedUser

from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from easyshop.core.config import _, MESSAGES
from easyshop.core.interfaces import IAsynchronPaymentMethod, \
                                     ICartManagement, \
                                     ICheckoutManagement, \
                                     ICustomerManagement, \
                                     IOrderManagement, \
                                     IPaymentInformationManagement, \
                                     IPaymentProcessing, \
                                     IStockManagement
                                     
from easyshop.checkout.browser.order_preview import OrderPreviewForm as OrderPreviewFormBase
from easyshop.payment.config import ERROR, PAYED

class OrderPreviewForm(OrderPreviewFormBase):
    """
    """
    template = ViewPageTemplateFile('order_preview.pt')
    
    @form.action(_(u"label_buy", default=u"Buy"), 
                 validator=OrderPreviewFormBase.validator, 
                 name=u'buy')
    def handle_buy_action(self, action, data):
        """Buys a cart.
        """
        putils = getToolByName(self.context, "plone_utils")
                
        # add order
        om = IOrderManagement(self.context)
        new_order = om.addOrder()

        # Set message to shop owner
        new_order.setMessage(self.context.request.get("form.message", ""))
        
        # process payment
        result = IPaymentProcessing(new_order).process()

        # Need error for payment methods for which the customer has to pay at 
        # any case The order process should not go on if the customer is not 
        # able to pay.
        if result.code == ERROR:
            om.deleteOrder(new_order.id)
            putils.addPortalMessage(result.message, type=u"error")
            ICheckoutManagement(self.context).redirectToNextURL("ERROR_PAYMENT")
            return ""
        elif result.code != "MPAY24":
            # leave cart untouched until payment is successful
            cm = ICartManagement(self.context)

            # Decrease stock
            IStockManagement(self.context).removeCart(cm.getCart())
        
            # Delete cart
            cm.deleteCart()

            # Set order to pending (Mails will be sent)
            wftool = getToolByName(self.context, "portal_workflow")
            wftool.doActionFor(new_order, "submit")
        
            putils.addPortalMessage(MESSAGES["ORDER_RECEIVED"])
                        
        if result.code == PAYED:

            # Set order to payed (Mails will be sent)
            wftool = getToolByName(self.context, "portal_workflow")

            # We need a new security manager here, because this transaction 
            # should usually just be allowed by a Manager except here.
            old_sm = getSecurityManager()
            tmp_user = UnrestrictedUser(
                old_sm.getUser().getId(),
                '', ['Manager'], 
                ''
            )

            portal = getToolByName(self.context, 'portal_url').getPortalObject()
            tmp_user = tmp_user.__of__(portal.acl_users)
            newSecurityManager(None, tmp_user)

            wftool.doActionFor(new_order, "pay_not_sent")
            
            ## Reset security manager
            setSecurityManager(old_sm)
        
        if result.code == "MPAY24":
            """ redirect to payment page
                later the response pages are handling payment success/error/confirmation
            """
            return self.context.request.response.redirect(result.message)
            
        # Redirect
        customer = \
            ICustomerManagement(self.context).getAuthenticatedCustomer()
        selected_payment_method = \
            IPaymentInformationManagement(customer).getSelectedPaymentMethod()
        
        if not IAsynchronPaymentMethod.providedBy(selected_payment_method):
            ICheckoutManagement(self.context).redirectToNextURL("BUYED_ORDER")