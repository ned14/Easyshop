from AccessControl.SecurityManagement import getSecurityManager, \
    newSecurityManager, setSecurityManager
from AccessControl.User import UnrestrictedUser
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import log
from easyshop.mpay24.config import REDIR_COOKIE_NAME
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
                # set to pending (send emails)
                wftool.doActionFor(order, "submit")
                # set to payed
                wftool.doActionFor(order, "pay_not_sent")
            except Exception, msg:
                self.status = msg

            # Reset security manager
            setSecurityManager(old_sm)

        # delete redirection cookie
        self.request.response.expireCookie(REDIR_COOKIE_NAME, path='/')

        return "OK: received"