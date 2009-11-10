# plone imports
from plone.memoize.instance import memoize

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# Five imports
from Products.Five.browser import BrowserView

# easyshop imports
from easyshop.core.interfaces import ICategoryManagement
from easyshop.core.interfaces import IProduct
from easyshop.core.interfaces import IProductManagement
from easyshop.core.interfaces import IShopManagement


class SitemapView(BrowserView):
    """
    """
    def getCategories(self):
        """
        """
        shop = IShopManagement(self.context).getShop()
        categories = ICategoryManagement(shop).getTopLevelCategories(full_objects=False)

        result = []
        for category in categories:

            klass = ""
            if self._isCurrentItem(category) == True:
                klass += "navTreeCurrentItem"

            result.append({
                "klass"                : klass,
                "url"                  : category.getURL(),
                "description"          : category.Description,
                "title"                : category.Title,
                "amount_of_products"   : category.total_amount_of_products,
                "subcategories"        : self._getSubCategories(category),
                "products"             : self._getProducts(category),
            })

        return result

    def getShopUrl(self):
        """
        """
        shop = IShopManagement(self.context).getShop()
        return shop.absolute_url()

    def _getSubCategories(self, category):
        """
        """
        result = []

        # Use catalog search directly here for speed reasons. Using
        # ICategoryManagement() would force me to get the object out of the brain.
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog(portal_type="Category",
                         path = {"query" : category.getPath(),
                                 "depth" : 1},
                         sort_on = "getObjPositionInParent")

        for category in brains:

            klass = ""
            if self._isCurrentItem(category) == True:
                klass += "navTreeCurrentItem"

            result.append({
                "klass"                : klass,
                "url"                  : category.getURL(),
                "description"          : category.Description,
                "title"                : category.Title,
                "amount_of_products"   : category.total_amount_of_products,
                "subcategories"        : self._getSubCategories(category),
                "products"             : self._getProducts(category),
            })

        return result

    def _getProducts(self, category):
        """
        """
        object = category.getObject()

        products = []
        for product in IProductManagement(object).getProducts():
            products.append({
                "title" : product.Title(),
                "url"   : product.absolute_url()
            })

        return products

    def _isCurrentItem(self, category):
        """Selected category and parent are current categories.
        """
        context_url  = self.context.absolute_url()
        category_url = hasattr(category,'getURL') and category.getURL() or \
            category.absolute_url()

        if context_url.startswith(category_url):
            return True

        elif IProduct.providedBy(self.context):
            try:
                product_category = self.context.getBRefs("categories_products")[0]
            except IndexError:
                return False

            # UID doesn't work here. Don't know why yet.
            category_url = category.getPath()
            context_url  = "/".join(product_category.getPhysicalPath())

            if context_url.startswith(category_url):
                return True

        return False
