# zope imports
from zope.interface import implements
from zope.component import adapts

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import IAddress
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICopyManagement
from easyshop.core.interfaces import ICreditCard
from easyshop.core.interfaces import ICustomer
from easyshop.core.interfaces import IBankAccount
from easyshop.core.interfaces import IPaymentInformationManagement

from easyshop.customers.content import Address
from easyshop.payment.content import BankAccount
from easyshop.customers.content import Customer
from easyshop.payment.content import CreditCard


class CustomerCopyManagement:
    """
    """
    implements(ICopyManagement)
    adapts(ICustomer)

    def __init__(self, context):
        """
        """
        self.context = context                  

    def copyTo(self, target=None, new_id=None):
        """
        """
        if target is None:
            target = self.context.aq_inner.aq_parent

        if new_id is None:
            new_id = self.context.id

        wftool = getToolByName(self.context, "portal_workflow")
        
        new_customer = Customer(new_id)
        for field in ICustomer.names():
            setattr(new_customer, field, getattr(self.context, field))

        # Set object
        target._setObject(new_id, new_customer)
        new_customer = target[new_id]
        
        # NOTE: I know this is not really nice but it helps as there are some
        # permission problems with Zope's copy and paste, when it comes to 
        # copying content as anonymous user, which is needed for anonymous 
        # checkout -> copy the customer object to the new order.

        new_customer.firstname = self.context.firstname
        new_customer.lastname  = self.context.lastname
        new_customer.email     = self.context.email
    
        new_customer.selected_invoice_address     = self.context.selected_invoice_address
        new_customer.selected_shipping_address    = self.context.selected_shipping_address
        new_customer.selected_payment_method      = self.context.selected_payment_method
        new_customer.selected_payment_information = self.context.selected_payment_information
        new_customer.selected_shipping_method     = self.context.selected_shipping_method
        new_customer.selected_country             = self.context.selected_country
        
        # Copy addresses    
        session_addresses = IAddressManagement(self.context).getAddresses()
        for session_address in session_addresses:
            new_address = Address(session_address.id)
            for field in IAddress.names():
                setattr(new_address, field, getattr(session_address, field))
            new_customer._setObject(new_address.id, new_address)
            new_address = new_customer[new_address.id]
            wftool.notifyCreated(new_address)

        # Copy customer payment methods.
        pm = IPaymentInformationManagement(self.context)
        for session_direct_debit in pm.getPaymentInformations(IBankAccount):
            new_direct_debit = BankAccount(session_direct_debit.id)
            for field in IBankAccount.names():
                setattr(new_direct_debit, field, getattr(session_direct_debit, field))
            new_customer._setObject(new_direct_debit.id, new_direct_debit)
            new_direct_debit = new_customer[new_direct_debit.id]
            wftool.notifyCreated(new_direct_debit)

        for session_credit_card in pm.getPaymentInformations(ICreditCard):
            new_credit_card = CreditCard(session_credit_card.id)
            for field in ICreditCard.names():
                setattr(new_credit_card, field, getattr(session_credit_card, field))
            new_customer._setObject(new_credit_card.id, new_credit_card)
            new_credit_card = new_customer[new_credit_card.id]
            wftool.notifyCreated(new_credit_card)
        
        new_customer.reindexObject()
        wftool.notifyCreated(new_customer)
        
        return new_customer