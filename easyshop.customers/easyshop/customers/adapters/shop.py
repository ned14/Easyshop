# zope imports
from zope.interface import implements
from zope.component import adapts

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IShop

class CustomerManagement:
    """Provides customer management for shop content objects.
    """
    implements(ICustomerManagement)
    adapts(IShop)

    def __init__(self, context):
        """
        """
        self.context = context
        self.customers = self.context.customers

    def getAuthenticatedCustomer(self):
        """Returns the authenticated Customer

           If it doesn't already exist, creates a new one
        """
        mtool = getToolByName(self.context, "portal_membership")
        member_id = mtool.getAuthenticatedMember().getId()

        # if the customer isn't logged in yet, return a standard customer
        # This is used to calculate shipping prices in cart.
        if member_id is None:
            if self.hasCustomer("standard-customer"):
                customer = getattr(self.context.customers, "standard-customer")
            else:
                self.customers.manage_addProduct["easyshop.shop"].addCustomer("standard-customer")
                customer = getattr(self.customers, "standard-customer")
                customer.setTitle("standard-customer")
                customer.setInvoiceAddressAsString("standard-address")
                customer.setShippingAddressAsString("standard-address")
                                
                customer.manage_addProduct["easyshop.shop"].addAddress("standard-address")
                address = getattr(customer, "standard-address")
                address.setCountry("Deutschland")
                
                customer.reindexObject()
                address.reindexObject()                
        else:    
            if self.hasCustomer(member_id):
                customer = getattr(self.context.customers, member_id)
            else:
                # Todo: Change to invokeFactory
                # self.customers.invokeFactory("Customer", id="member_id", title="member_id")
                self.customers.manage_addProduct["easyshop.shop"].addCustomer(member_id)
                customer = getattr(self.customers, member_id)
                customer.setTitle(member_id)
                customer.at_post_create_script()

        return customer

    def getCustomers(self):
        """Returns all Customers
        """
        # Todo. optimize
        return self.customers.objectValues("Customer")

    def getCustomerById(self, id):
        """Returns a customer by given id
        """
        try:
            return self.customers[id]
        except KeyError:
            return None
        
    def hasCustomer(self, id):
        """Returns true if the customer already exists
        """
        customer_ids = [c.getId() for c in self.getCustomers()]
        if id in customer_ids:
            return True

        return False
