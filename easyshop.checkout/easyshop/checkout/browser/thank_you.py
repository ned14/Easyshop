# zope imports
from zope.component import getMultiAdapter

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.config import _
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IFormats
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IOrderManagement
from easyshop.core.interfaces import IImageManagement
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IShopManagement

from easyshop.shop.utilities.misc import sendMultipartMail

class ThankYouPageView(BrowserView):
    """
    """
    def getFormatInfo(self):
        """
        """
        return IFormats(self.context).getFormats()

    def getLatestOrder(self):
        """Returns the last order id of authenticated customer
        """
        om = IOrderManagement(self.context)
        orders = om.getOrdersForAuthenticatedCustomer()        
        orders.sort(lambda a, b: cmp(b.created(), a.created()))

        order = orders[0]
        
        # Address
        customer = order.getCustomer()
        address  = IAddressManagement(customer).getInvoiceAddress()

        prices = IPrices(order)
        
        transaction = {
                "order_id"    : order.getId(),
                "affiliation" : "",
                "total"       : prices.getPriceForCustomer(),
                "tax"         : (prices.getPriceForCustomer() - prices.getPriceNet()),
                "shipping"    : order.getShippingPriceGross(),
                "city"        : address.city,
                "state"       : "",
                "country"     : address.country,
        }
        
        items = []
        for item in IItemManagement(order).getItems():

            # Product
            product = item.getProduct()
            
            # Category
            try:
                category = product.getCategories()[0]
                category_title = category.Title()
            except IndexError:
                category_title = u""
            
            items.append({
                "order_id"    : order.getId(),
                "sku"         : product.getArticleId(),
                "productname" : product.Title(),
                "category"    : category_title,
                "price"       : item.getProductPriceGross(),
                "quantity"    : item.getProductQuantity()
            })
        
        result = {
            "id"                 : order.getId(),
            "url"                : order.absolute_url(),
            "google_transaction" : transaction, 
            "google_items"       : items,
        }
        
        return result

    def getMyAccountURL(self):
        """
        """
        shop = IShopManagement(self.context).getShop()
        customer = ICustomerManagement(shop).getAuthenticatedCustomer()
        
        return customer.absolute_url() + "/" + "my-account"
        
    def getProducts(self):
        """
        """
        selector = getattr(self.context, "thank-you", None)
        if selector is None: return []
        
        mtool = getToolByName(self.context, "portal_membership")
        
        result = []
        for product in selector.getRefs():

            if mtool.checkPermission("View", product) is None:
                continue

            # image
            pm = IImageManagement(product)
            image = pm.getMainImage()
            if image is None:
                image = None
            else:
                image = "%s/image_shop_small" % image.absolute_url()

            cm    = ICurrencyManagement(self.context)
            price = IPrices(product).getPriceForCustomer()
            price = cm.priceToString(price)

            result.append({
                "title"                    : product.Title(),
                "short_title"              : product.getShortTitle() or product.Title(),                    
                "url"                      : product.absolute_url(),
                "price"                    : price,
                "image"                    : image,
            })

        return result

    def sendRecommendation(self):
        """
        """
        if self.request.get("email", "") == "":        
            utool = getToolByName(self.context, "plone_utils")
            utool.addPortalMessage(_("Please add a e-mail address."))                        
            url = "%s/thank-you" % self.context.absolute_url()

        else:
            # Get charset
            props = getToolByName(self.context, "portal_properties").site_properties
            charset = props.getProperty("default_charset")

            template = getMultiAdapter(
                (self.context, self.request),
                name="send-recommendation-template")
                
            text = template()
            
            sendMultipartMail(
                context = self.context,
                from_   = self.context.getMailFrom(),
                to      = self.request.get("email"),
                subject = "Empfehlung Demmelhuber Holz und Raum GmbH",
                text    = text,
                charset = charset)

            utool = getToolByName(self.context, "plone_utils")
            utool.addPortalMessage(_("Your mail has been sent."))
            url = "%s/thank-you" % self.context.absolute_url()

        self.request.response.redirect(url)
        
    # Todo: Optimize. Factor out. This code (similar) is also used in 
    # selector_view.py
    def getSelectors(self):
        """
        """
        fi = self.getFormatInfo()
        products_per_line = fi.get("products_per_line")
        
        mtool = getToolByName(self.context, "portal_membership")
            
        selectors = []
        for selector in self.context.objectValues("ProductSelector"):

            # ignore thank you selection
            if selector.getId() != "thank-you":
                continue

            products_per_line = products_per_line

            lines = []            
            products = []
            for index, product in enumerate(selector.getRefs()):

                if mtool.checkPermission("View", product) is None:
                    continue

                cm    = ICurrencyManagement(self.context)
                price = IPrices(product).getPriceForCustomer()
                price = cm.priceToString(price)
                
                # image
                image = IImageManagement(product).getMainImage()
                if image is not None:
                    image = "%s/image_%s" % (image.absolute_url(), fi.get("image_size"))

                t = fi.get("text")
                if t == "description":
                    text = product.getDescription()
                elif t == "short_text":
                    text = product.getShortText()
                elif t == "text":
                    text = product.getText()
                else:
                    text = ""

                n = len(selector.getRefs())    
                if index == n-1 and n > 1 and products_per_line > 1:
                    klass = "last"
                else:
                    klass = "notlast"
                                        
                products.append({
                    "title"                    : product.Title(),
                    "short_title"              : product.getShortTitle() or product.Title(),                    
                    "url"                      : product.absolute_url(),
                    "price"                    : price,
                    "image"                    : image,
                    "text"                     : text,
                    "class"                    : klass,
                })
    
                if (index+1) % products_per_line == 0:
                    lines.append(products)
                    products = []

            # the rest
            lines.append(products)

            selectors.append({
                "edit_url"         : "%s/base_edit" % selector.absolute_url(),
                "show_title"       : selector.getShowTitle(),
                "title"            : selector.Title(),
                "lines"            : lines,
                "products_per_line" : products_per_line,
                "td_width"         : "%s%%" % (100 / products_per_line),                
            })

        return selectors      
          
    def showEditLink(self):
        """
        """
        mtool = getToolByName(self.context, "portal_membership")
        if mtool.checkPermission("Manage portal", self.context):
            return True
        return False        