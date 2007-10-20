# zope imports
from zope.interface import implements
from zope.component import adapts

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports
from Products.EasyShop.interfaces.cart import ICartManagement
from Products.EasyShop.interfaces.item import IItemManagement
from Products.EasyShop.interfaces import IShop

class CartManagement:
    """Provices cart management methods for shop content objects.
    """
    implements(ICartManagement)
    adapts(IShop)
    
    def __init__(self, context):
        """
        """
        self.context = context

    def addCart(self, id):
        """
        """
        self.context.carts.manage_addProduct["EasyShop"].addCart(id = id)
        return self.getCartById(id)

    def createCart(self):
        """
        """
        cart_id = self._getCartId()
        
        self.context.carts.manage_addProduct["EasyShop"].addCart(
            id = cart_id
        )
        
        return self.context.carts[cart_id]
        
    def deleteCart(self, id=None):
        """Deletes a cart
        """
        if id is None:
            mtool = getToolByName(self.context, "portal_membership")
            id = mtool.getAuthenticatedMember().getId()

        # needs no permissions
        self.context.carts._delObject(id)

    def getCart(self):
        """
        """
        mtool = getToolByName(self.context, "portal_membership")
                
        try:
            sid = self.context.REQUEST.SESSION.getId()
        except AttributeError:
            sid = "DUMMY_SESSION"
            
        # get anonymous cart
        try:
            anonymous_cart = self.context.carts[sid]
        except KeyError:
            anonymous_cart = None
        
        if mtool.isAnonymousUser():
            cart = anonymous_cart
        else:
            # If there is a anonymous cart for the actual session, add this
            # cart to the member cart and delete the anonymous cart
            mid = mtool.getAuthenticatedMember().getId()
            if anonymous_cart is None:
                try:
                    cart = self.context.carts[mid]
                except KeyError:
                    cart = None

            else:
                if self.hasCart():
                    cart = self.context.carts[mid]
                else:
                    cart = self.createCart()
                            
                im = IItemManagement(cart).addItemsFromCart(anonymous_cart)
                self.deleteCart(sid)

        return cart

    def getCarts(self, sort_on="created", sort_order="descending"):
        """
        """
        path = "/".join(self.context.carts.getPhysicalPath())
        
        query = {
            "path"        : path,
            "portal_type" : "Cart",
            "sort_on"     : sort_on,
            "sort_order"  : sort_order,
        }

        catalog = getToolByName(self.context, "portal_catalog")
        brains  = catalog.searchResults(query)

        return brains
        
    def getCartById(self, id):
        """Returns a cart by given id.        
        """
        try:
            return self.context.carts[id]
        except KeyError:
            return None

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
            self.context.carts[self._getCartId()]
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
        
        try:
            cart_id = self.context.REQUEST.SESSION.getId()
        except AttributeError:
            # Todo: This is only needed for test purposes. I'm sure this is
            # not very clean but I'm not able to manage to create a (test)
            # session within functional tests. OTOH this is not very invasive
            # and there should be always a SESSION in "normal" browser
            # sessions.
            cart_id = "DUMMY_SESSION"            
        
        return cart_id