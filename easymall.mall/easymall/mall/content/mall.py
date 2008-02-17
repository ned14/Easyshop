# Zope imports
from zope.interface import alsoProvides
from zope.interface import implements
from zope.component import getUtility
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# Archetypes imports
from Products.Archetypes.atapi import *

# ATContentTypes imports
from Products.ATContentTypes.content.folder import ATFolder

# plone.portlets imports
from plone.portlets.constants import CONTEXT_CATEGORY
from plone.portlets.interfaces import ILocalPortletAssignmentManager
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager

# easyshop imports
from easyshop.core.config import *
from easyshop.core.interfaces import IShop
from easyshop.core.interfaces import IImageConversion

from easyshop.catalog.portlets import formatter
from easyshop.shop.content.shop import EasyShop

from easyshop.carts.portlets import cart
from easyshop.customers.portlets import my_account

# easyshop imports
from easymall.catalog.portlets import categories
from easymall.mall.portlets import mall_admin
from easymall.mall.config import *
from easymall.mall.interfaces import IMall

schema = EasyShop.schema.copy()
    
class EasyMall(ATFolder):
    """A mall holds several shops.
    """
    implements(IMall)
    _at_rename_after_creation = True
    schema = schema

    def at_post_create_script(self):
        """Overwritten to create some objects.
        """
        # Add left portlets
        leftColumn = getUtility(IPortletManager, name=u'plone.leftcolumn', context=self)
        left = getMultiAdapter((self, leftColumn,), IPortletAssignmentMapping, context=self)

        if u'portlets.MallAdmin' not in left:
            left[u'portlets.MallAdmin'] = mall_admin.Assignment()
            order = [left.keys()[-1]]+left.keys()[:-1]
            left.updateOrder(list(order))
        
        if u'portlets.MallCategories' not in left:
            left[u'portlets.MallCategories'] = categories.Assignment()
            order = [left.keys()[-1]]+left.keys()[:-1]
            left.updateOrder(list(order))

        # Block default portlets
        assignable = getMultiAdapter((self, leftColumn,), ILocalPortletAssignmentManager)
        assignable.setBlacklistStatus(CONTEXT_CATEGORY, True)
                
        # Add right portlets 
        rightColumn = getUtility(IPortletManager, name=u'plone.rightcolumn', context=self)
        right = getMultiAdapter((self, rightColumn,), IPortletAssignmentMapping, context=self)

        if u'portlets.Formatter' not in right:
            right[u'portlets.Formatter'] = formatter.Assignment()
            order = [right.keys()[-1]]+right.keys()[:-1]
            right.updateOrder(list(order))

        if u'portlets.Cart' not in right:
            right[u'portlets.Cart'] = cart.Assignment()
            order = [right.keys()[-1]]+right.keys()[:-1]
            right.updateOrder(list(order))

        if u'portlets.MyAccount' not in right:
            right[u'portlets.MyAccount'] = my_account.Assignment()
            order = [right.keys()[-1]]+right.keys()[:-1]
            right.updateOrder(list(order))

        # Block default portlets
        assignable = getMultiAdapter((self, rightColumn,), ILocalPortletAssignmentManager)
        assignable.setBlacklistStatus(CONTEXT_CATEGORY, True)

        # Create containers
        self.manage_addProduct["easyshop.shop"].addCartsContainer(id="carts", title="Carts")
        self.manage_addProduct["easyshop.shop"].addCategoriesContainer(id="categories", title="Categories")        
        self.manage_addProduct["easyshop.shop"].addCustomersContainer(id="customers", title="Customers")
        self.manage_addProduct["easyshop.shop"].addSessionsContainer(id="sessions", title="Sessions")
        self.manage_addProduct["easyshop.shop"].addGroupsContainer(id="groups", title="Groups")
        self.manage_addProduct["easyshop.shop"].addTaxesContainer(id="taxes", title="Taxes")

        ### Information        
        self.manage_addProduct["easyshop.shop"].addInformationContainer(id="information", title="Information")
        self.information.manage_addProduct["easyshop.shop"].addInformationPage(
            id="terms-and-conditions", title="Terms And Conditions")

        ### Orders
        self.manage_addProduct["easyshop.shop"].addOrdersContainer(id="orders", title="Orders")
        self.orders.manage_permission('Add portal content', ['Member'], 1)

        ### Payment            
        self.manage_addProduct["easyshop.shop"].addPaymentMethodsContainer(id="paymentmethods", 
            title="Payment Methods")
            
        self.manage_addProduct["easyshop.shop"].addPaymentPricesContainer(
            id="paymentprices", title="Payment Prices")        
        self.paymentmethods.manage_addProduct["easyshop.shop"].addGenericPaymentMethod( 
            id="cash-on-delivery", title="Cash on Delivery")                
        self.paymentmethods.manage_addProduct["easyshop.shop"].addCreditCardPaymentMethod(
            id="credit-card", title="Credit Card")                
        self.paymentmethods.manage_addProduct["easyshop.shop"].addDirectDebitPaymentMethod(
            id="direct-debit", title="Direct Debit")
        self.manage_addProduct["easyshop.shop"].addPayPalPaymentMethod(id="paypal",  title="PayPal")
        self.manage_addProduct["easyshop.shop"].addGenericPaymentMethod(id="prepayment", 
            title="Prepayment")   

        wftool = getToolByName(self, "portal_workflow")
        for payment_method in self.paymentmethods.objectValues():
            wftool.doActionFor(payment_method, "publish")

        ### Shipping    
        self.manage_addProduct["easyshop.shop"].addShippingPricesContainer(id="shippingprices", 
            title="Shipping Prices")
        self.manage_addProduct["easyshop.shop"].addShippingMethodsContainer(id="shippingmethods",
            title="Shipping Methods")
        self.manage_addProduct["easyshop.shop"].addShippingMethod(id="default", title="Default")

        for shipping_method in self.shippingmethods.objectValues():
            wftool.doActionFor(shipping_method, "publish")
        
    def _getCurrenciesAsDL(self):
        """
        """
        dl = DisplayList()
        
        keys = CURRENCIES.keys()
        keys.sort()
        
        for key in keys:
            dl.add(key, CURRENCIES[key]["long"])

        return dl
                
registerType(EasyMall, PROJECTNAME)