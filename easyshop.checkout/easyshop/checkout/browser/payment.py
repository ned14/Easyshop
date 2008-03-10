# zope imports
from zope import schema
from zope.app.form.interfaces import WidgetInputError
from zope.component import adapts
from zope.formlib import form
from zope.interface import implements

# Five imports
from Products.Five.browser import pagetemplatefile
from Products.Five.formlib import formbase

# CMFPlone imports
from Products.CMFPlone.utils import safe_unicode

# easyshop imports
from easyshop.core.config import _
from easyshop.core.interfaces import IBankAccount
from easyshop.core.interfaces import ICheckoutManagement
from easyshop.core.interfaces import ICreditCard
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IPaymentInformationManagement
from easyshop.core.interfaces import IPaymentMethodManagement
from easyshop.core.interfaces import IShop
from easyshop.core.interfaces import IValidity
from easyshop.payment.content import BankAccount
from easyshop.payment.content import CreditCard

class IPaymentSelectForm(IBankAccount, ICreditCard):
    """
    """
    payment_method  = schema.TextLine()
    
class ShopPaymentSelectForm:
    """
    """
    implements(IPaymentSelectForm)
    adapts(IShop)
    
    def __init__(self, context):
        """
        """
        self.context = context
    
    payment_method  = u""
    account_number = u""
    bank_identification_code = u""
    bank_name = u""
    depositor = u""
    
    card_type = u""
    card_owner = u""
    card_number = u""
    card_expiration_date_month = u""
    card_expiration_date_year  = u""

# Using here Five's EditForm by heart because plone.app.form would lock the shop 
# which is not desired in this case (because the shop is not modified at all)
class PaymentForm(formbase.EditForm):
    """
    """
    template = pagetemplatefile.ZopeTwoPageTemplateFile("payment.pt")
    form_fields = form.Fields(IPaymentSelectForm)

    def validator(self, action, data):
        """
        """
        errors = []
        if self.request.get("form.id") == "direct_debit_new":
            for widget_name in ("account_number", "depositor", "bank_name",
                                "bank_identification_code"):

                if self.request.get("form.%s" % widget_name, u"") == u"":
                    widget = self.widgets[widget_name]
                    error = WidgetInputError(
                        widget.name, widget.label, "%s" +  _(u" is required" % widget.label)
                    )
                    widget._error = error
                    errors.append(error)

        elif self.request.get("form.id") == "credit_card_new":
            for widget_name in ("card_type", "card_owner", "card_number"):

                if self.request.get("form.%s" % widget_name, u"") == u"":
                    widget = self.widgets[widget_name]
                    error = WidgetInputError(
                        widget.name, widget.label, "%s" +  _(u" is required" % widget.label)
                    )
                    widget._error = error
                    errors.append(error)
                
        return errors

    @form.action(_(u"label_next", default="Next"), validator=validator, name=u"next")
    def handle_next_action(self, action, data):
        """
        """        
        customer = ICustomerManagement(self.context).getAuthenticatedCustomer()
        id = self.request.get("form.id")

        # figure out payment method type
        if id.startswith("bank_account"):
            payment_method = "direct-debit"
        elif id.startswith("credit_card"):
            payment_method = "credit-card"
        else:
            payment_method = id
        
        if id == "bank_account_new":
            depositor = self.request.get("form.depositor", u"")
            account_number = self.request.get("form.account_number", u"")
            bank_identification_code = self.request.get("form.bank_identification_code", u"")
            bank_name = self.request.get("form.bank_name", u"")

            id = self.context.generateUniqueId("BankAccount")
            bank_account = BankAccount(id)
            bank_account.account_number = account_number
            bank_account.bank_identification_code = bank_identification_code
            bank_account.bank_name = bank_name
            bank_account.depositor = depositor
        
            customer._setObject(id, bank_account)

        if id == "credit_card_new":            
            card_type = self.request.get("form.card_type", u"")
            card_number = self.request.get("form.card_number", u"")
            card_owner = self.request.get("form.card_owner", u"")
            card_expiration_date_month = self.request.get("form.card_expiration_date_month", u"")
            card_expiration_date_year = self.request.get("form.card_expiration_date_year", u"")
            
            id = self.context.generateUniqueId("CreditCard")
            credit_card = CreditCard(id)
            credit_card.card_type = card_type
            credit_card.card_number = card_number
            credit_card.card_owner = card_owner
            credit_card.card_expiration_date_month = card_expiration_date_month
            credit_card.card_expiration_date_year  = card_expiration_date_year
            
            customer._setObject(id, credit_card)
            
        elif id.startswith("bank_account_existing") or \
             id.startswith("credit_card_existing"):
            id = id.split(":")[1]
                
        customer.selected_payment_method      = payment_method
        customer.selected_payment_information = id
                    
        ICheckoutManagement(self.context).redirectToNextURL("SELECTED_PAYMENT_METHOD")

    def getCreditCards(self):
        """
        """
        if self._isValid("credit-card") == False:
            return []
        
        cm = ICustomerManagement(self.context)
        customer = cm.getAuthenticatedCustomer()

        result = []        
        pm = IPaymentInformationManagement(customer)
        for credit_card in pm.getPaymentInformations(
            interface=ICreditCard, check_validity=True):

            selected_payment_information = \
                pm.getSelectedPaymentInformation(check_validity=True)
                
            if selected_payment_information.getId() == credit_card.getId():
                checked = True
            else:
                checked = False            
            
            exp_date = "%s/%s" % (credit_card.card_expiration_date_month, 
                                  credit_card.card_expiration_date_year)
            result.append({
                "id"               : credit_card.getId(),
                "type"             : credit_card.card_type,
                "owner"            : credit_card.card_owner,
                "number"           : credit_card.card_number,
                "expiration_date"  : exp_date,
                "checked"          : checked,
            })
        
        return result
        
    def getBankAccounts(self):
        """
        """
        if self._isValid("direct-debit") == False:
            return []
        
        cm = ICustomerManagement(self.context)
        customer = cm.getAuthenticatedCustomer()
                
        result = []        
        pm = IPaymentInformationManagement(customer)

        for bank_account in pm.getPaymentInformations(
            interface=IBankAccount, check_validity=True):

            selected_payment_information = \
                pm.getSelectedPaymentInformation(check_validity=True)
                
            if selected_payment_information.getId() == bank_account.getId():
                checked = True
            else:
                checked = False            
            
            result.append({
                "id"         : bank_account.getId(),
                "bic"        : bank_account.bank_identification_code,
                "account_no" : bank_account.account_number,
                "depositor"  : bank_account.depositor,
                "bank_name"  : bank_account.bank_name,
                "checked"    : checked,
            })
        
        return result

    def getSelectablePaymentMethods(self):
        """Returns selectable payment methods.
        """
        customer = ICustomerManagement(self.context).getAuthenticatedCustomer()
        pm = IPaymentInformationManagement(customer)
        
        selected_payment_method = \
            pm.getSelectedPaymentMethod(check_validity=True)
        
        result = []
        pm = IPaymentMethodManagement(self.context)
        for payment in pm.getSelectablePaymentMethods(check_validity=True):

            # Todo: Make default payment method editable. ATM it is prepayment.
            # So if nothing is selected checked is true for prepayment.

            # If id is bank_account_new (this happens when customer wants to 
            # add a new direct debit and is due to validation errors redirected to 
            # the form).
            
            checked = False
            if (self.request.get("form.id", "") not in ("bank_account_new", "credit_card_new")) and \
               (selected_payment_method.getId() == safe_unicode(payment.getId())):
                checked = True
                                
            result.append({                
                "id"          : payment.getId(),
                "title"       : payment.Title(),
                "description" : payment.Description(),               
                "checked"     : checked,
            })
        
        return result

    def getClass(self, expression, true_value, false_value):
        """
        """
        if len(expression) > 0:
            return "widget error"
        else:
            return "widget"

    def showCreditCards(self):
        """
        """
        return self._isValid("credit-card")

    def showBankAccounts(self):
        """
        """
        return self._isValid("direct-debit")
        
    def _isValid(self, name):
        """Returns true if the payment method with given name is valid.
        """
        spm = IPaymentMethodManagement(self.context)
        dd = spm.getPaymentMethod(name)
        
        if dd is None or IValidity(dd).isValid() == False:
            return False
        else:
            return True