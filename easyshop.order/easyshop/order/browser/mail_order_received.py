# easyshop imports
from easyshop.order.browser.order_view import OrderView
from easyshop.core.interfaces import IPaymentInformationManagement

class MailOrderReceivedView(OrderView):
    """
    """ 
    def getNote(self):
        """Returns the note from the selected payment method.
        """
        customer = self.context.getCustomer()
        pm = IPaymentInformationManagement(customer)
        
        selected_payment_method = pm.getSelectedPaymentMethod()

        note =  selected_payment_method.getNote()
        
        payment_url = self.context.absolute_url() + "/pay"
        note = note.replace("[payment-url]", payment_url)
        
        return note