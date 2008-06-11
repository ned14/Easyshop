# easyshop imports
from easyshop.order.browser.order_view import OrderView

class MailOrderReceivedView(OrderView):
    """
    """ 
    def getNote(self):
        """
        """
        payment_data = self.getSelectedPaymentData()
        payment_method = payment_data.get("payment_method")
        
        note = payment_method.getNote()
        
        payment_url = self.context.absolute_url() + "/pay"
        note = note.replace("[paypal-link]", payment_url)
        
        return note