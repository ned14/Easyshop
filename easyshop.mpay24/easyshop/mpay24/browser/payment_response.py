from AccessControl.SecurityManagement import getSecurityManager, \
    newSecurityManager, setSecurityManager
from AccessControl.User import UnrestrictedUser
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import log
from easyshop.core.interfaces import IOrderManagement, \
                                     ICartManagement, \
                                     IStockManagement

class PaymentConfirmation(BrowserView):

    def __call__(self):
        om = IOrderManagement(self.context)
        tid = self.request.get('TID','')
        order = getattr(om.orders,tid,None)
        
        log("\n%s\n%s\n%s" % (order, tid, self.request.get('STATUS')))
        
        if order and self.request.get('STATUS') in ['RESERVED','BILLED']:
            # cleanup shopping cart
            cm = ICartManagement(self.context)

            if cm.getCart():
                # Decrease stock
                IStockManagement(self.context).removeCart(cm.getCart())
            
            # Delete cart
            try:
                cm.deleteCart()
            except:
                pass
            
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

            try:
                # send mails by submitting
                wftool.doActionFor(order, "submit")
                # and set to payed
                wftool.doActionFor(order, "pay_not_sent")
            except Exception, msg:
                self.status = msg

            ## Reset security manager
            setSecurityManager(old_sm)
            
        return "OK: received"