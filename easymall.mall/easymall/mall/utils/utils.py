# zope imports
from zope import event

# Five imports
from Products.Five.browser import BrowserView

# Archetypes imports
from Products.Archetypes.event import ObjectInitializedEvent

class UtilsView(BrowserView):
    """
    """ 
    def createTestContent(self):
        """
        """
        # Add Mall
        self.context.invokeFactory(
            "EasyMall", 
            id="mall", 
            title="Mall",
            shopOwner="Mall",
        )
        
        mall = self.context["mall"]
        mall.at_post_create_script()
        event.notify(ObjectInitializedEvent(mall))
        mall._at_creation_flag = False
        
        # Add Shop 1
        mall.invokeFactory(
            "EasyShop", 
            id="shop-1", 
            title="Shop 1",
            shopOwner="Shop 1",
        )
        shop1 = mall["shop-1"]
        shop1.at_post_create_script()
        event.notify(ObjectInitializedEvent(shop1))
        shop1._at_creation_flag = False

        shop1.categories.invokeFactory(
            "Category",
            id="c1",
            title="C1 in Shop1")

        shop1.products.invokeFactory(
            "Product",
            id="p1",
            title="P1 in Shop 1",
            price=10.00)

        # Add Shop 2
        mall.invokeFactory(
            "EasyShop", 
            id="shop-2", 
            title="Shop 2",
            shopOwner="Shop 2",
        )
        shop2 = mall["shop-2"]
        shop2.at_post_create_script()        
        event.notify(ObjectInitializedEvent(shop2))        
        shop2._at_creation_flag = False
        
        shop2.categories.invokeFactory(
            "Category",
            id="c1",
            title="C1 in Shop2")

        shop2.products.invokeFactory(
            "Product",
            id="p1",
            title="P1 in Shop 2",
            price=100.00)

        shop1.categories.c1.addReference(shop1.products.p1, "categories_products")
        shop2.categories.c1.addReference(shop2.products.p1, "categories_products")
                    
        self.request.response.redirect(".")