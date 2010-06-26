# zope imports
from zope.interface import implements
from zope.component import adapts
from zope.component import getUtility

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import ISessionManagement
from easyshop.core.interfaces import IShop

class CartManagement(object):
    """Adapter which provides ICartManagement for shop content objects.
    """
    implements(ICartManagement)
    adapts(IShop)
    
    def __init__(self, context):
        """
        """
        self.context = context
        self.carts = self.context.carts

    def createCart(self):
        """
        """
        cart_id = self._getCartId()
        self.carts.manage_addProduct["easyshop.core"].addCart(id=cart_id)
        
        return self.carts[cart_id]
        
    def deleteCart(self, id=None):
        """Deletes a cart
        """
        if id is None:
            id = self._getCartId()

        # needs no permissions
        self.carts._delObject(id)

    def getCart(self):
        """
        """
        # Note: generally, carts aren't created until a product is put into the 
        # cart. We create a cart here only when a member logs in and has had
        # already an anonymous cart.
        
        mtool = getToolByName(self.context, "portal_membership")
        sid = getUtility(ISessionManagement).getSID(self.context.REQUEST)                
            
        # Get anonymous cart here, because we need it in any case.
        try:
            anonymous_cart = self.carts[sid]
        except KeyError:
            anonymous_cart = None

        # Note: Using this instead of mtool.isAnonymousUser() because this works
        # even if we exchange the SecurityManager. See here:
        # easyshop.orders.adapters.shop.order_management
        
        if mtool.getAuthenticatedMember().getId() is None:
            cart = anonymous_cart
        else:
            mid = mtool.getAuthenticatedMember().getId()
            
            # If there is no anonymous cart we just return the member cart if 
            # there is one, otherwise we return nothing.
            if anonymous_cart is None:
                try:
                    cart = self.carts[mid]
                except KeyError:
                    cart = None
                    
            # If there is already an anonymous cart we create a member cart and 
            # copy the items from anonymous to member cart.
            else:
                try:
                    cart = self.carts[mid]
                except KeyError:
                    cart = self.createCart()
                            
                im = IItemManagement(cart).addItemsFromCart(anonymous_cart)
                self.deleteCart(sid)

        return cart

    def getCarts(self, sort_on="created", sort_order="descending"):
        """
        """
        path = "/".join(self.carts.getPhysicalPath())
        
        query = {
            "path"        : path,
            "portal_type" : "Cart",
            "sort_on"     : sort_on,
            "sort_order"  : sort_order,
        }

        catalog = getToolByName(self.context, "portal_catalog")
        brains  = catalog.unrestrictedSearchResults(query)
        
        return brains
        
    def getCartById(self, id):
        """
        """
        return self.carts.get(id)

    def getCartByUID(self, uid):
        """Returns a cart by given uid.        
        """
        uid_catalog = getToolByName(self.context, 'uid_catalog')
        lazy_cat = uid_catalog(UID=uid)
        o = lazy_cat[0].getObject()
        return o

    def hasCart(self):
        """
        """ 
        # Note: Using try/except for getting cart to get rid of acquisition
        # (getattr) and to have no need to use of external dependancies like
        # shasattr or aq_base.
        try:
            self.carts[self._getCartId()]
        except KeyError:
            return False
        else:
            return True
            
    def _getCartId(self):
        """Returns cart id for current cart. This is either the session id
        (anonymous user) or the member id of the authenticated user.
        """
        mtool = getToolByName(self.context, "portal_membership")

        cart_id = mtool.getAuthenticatedMember().getId()
        if cart_id is not None:
            return cart_id
        else:
            return getUtility(ISessionManagement).getSID(self.context.REQUEST)