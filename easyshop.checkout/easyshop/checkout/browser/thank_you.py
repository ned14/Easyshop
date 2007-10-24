# Zope imports
from zope.interface import Interface
from zope.interface import implements

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IFormatterInfos
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IOrderManagement
from easyshop.core.interfaces import IPhotoManagement
from easyshop.core.interfaces import IPropertyManagement
from easyshop.core.interfaces import IPrices

from easyshop.shop.subscribers.mailing import sendMultipartMail

class IThankYouPageView(Interface):
    """
    """
    def getFormatInfo():
        """
        """

    def getLatestOrder():
        """Returns the last order id of authenticated customer
        """

    def getMailInfo():
        """
        """

    def getProducts():
        """Returns selected products.
        """

    def getSelectors():
        """
        """

    def sendRecommendation():
        """
        """
 
    def showEditLink():
        """
        """
        
class ThankYouPageView(BrowserView):
    """
    """
    implements(IThankYouPageView)

    def getFormatInfo(self):
        """
        """
        return IFormatterInfos(self.context).getFormatInfosAsDict()

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
                "city"        : address.getCity(),
                "state"       : "",
                "country"     : address.getCountry,
        }
        
        items = []
        for item in IItemManagement(order).getItems():

            # product
            product = item.getProduct()
            
            # category
            category = product.getEasyshopcategories()[0]
            
            items.append({
                "order_id"    : order.getId(),
                "sku"         : product.getArticle_id(),
                "productname" : product.Title(),
                "category"    : category.Title(),
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

            # photo
            pm = IPhotoManagement(product)
            photo = pm.getMainPhoto()
            if photo is None:
                image = None
            else:
                image = "%s/image_shop_small" % photo.absolute_url()

            cm    = ICurrencyManagement(self.context)
            price = IPrices(product).getPriceForCustomer()
            price = cm.priceToString(price)

            # properties view
            property_manager = IPropertyManagement(product)
            if len(property_manager.getProperties()) > 0:
                showSelectPropertiesView = True
            else:    
                showSelectPropertiesView = False
                        
            result.append({
                "title"                    : product.Title(),
                "short_title"              : product.getShortTitle() or product.Title(),                    
                "url"                      : product.absolute_url(),
                "price"                    : price,
                "image"                    : image,
                "showSelectPropertiesView" : showSelectPropertiesView,
            })

        return result

    def getMailInfo(self):
        """
        """
        cm = ICustomerManagement(self.context)
        customer = cm.getAuthenticatedCustomer()
        am = IAddressManagement(customer)
        shipping_address = am.getShippingAddress()

        mtool = getToolByName(self.context, "portal_membership")        
        member = mtool.getAuthenticatedMember()
        
        name  = shipping_address.getFirstname() + " "
        name += shipping_address.getLastname()
                
        return {
            "email" : member.getProperty("email"),
            "name"  : name,
        }
                
    def sendRecommendation(self):
        """
        """
        if self.request.get("email", "") == "":        
            url = "%s/check-out-thanks" % self.context.absolute_url()
            url += "?portal_status_message=Bitte geben Sie eine E-Mail Adresse ein."

        else:
            # get charset
            props = getToolByName(self.context, "portal_properties").site_properties
            charset = props.getProperty("default_charset")

            text = self.context.mail_recommend_shop()
            
            sendMultipartMail(
                context = self.context,
                from_   = self.context.getMailFrom(),
                to      = self.request.get("email"),
                subject = "Empfehlung Demmelhuber Holz und Raum GmbH",
                text    = text,
                charset = charset)

                
            url = "%s/check-out-thanks" % self.context.absolute_url()
            url += "?portal_status_message=Ihre Mail wurde versendet."

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
        # Todo: Optimize
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
                
                # photo
                photo = IPhotoManagement(product).getMainPhoto()
                if photo is not None:
                    image = "%s/image_%s" % (photo.absolute_url(), fi.get("image_size"))

                # properties view
                property_manager = IPropertyManagement(product)
                if len(property_manager.getProperties()) > 0:
                    showSelectPropertiesView = True
                else:    
                    showSelectPropertiesView = False

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
                    "showSelectPropertiesView" : showSelectPropertiesView,
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