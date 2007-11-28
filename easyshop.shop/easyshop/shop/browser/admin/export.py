# zope imports
from zope.interface import Interface
from zope.interface import implements

# Five imports
from Products.Five.browser import BrowserView

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IOrderManagement
from easyshop.core.interfaces import IShopManagement

class IExportView(Interface):    
    """
    """
    def getOrders():
        """
        """
       
class ExportView(BrowserView):
    """
    """
    implements(IExportView)
    
    def getOrders(self):
        """
        """
        om = IOrderManagement(IShopManagement(self.context).getShop())
        
        result = []
        for order in om.getOrders():
            
            # omit closed orders
            wftool = getToolByName(self.context, "portal_workflow")
            if wftool.getInfoFor(order, "review_state") == "closed":
                continue
                
            customer = order.getCustomer()

            # am = IAddressManagement(customer)
            # shipping_address = am.getShippingAddress()
            
            im = IItemManagement(order)
            for item in im.getItems():

                product = item.getProduct()
                
                row = (
                    order.getId(),
                    customer.getId(),
                    # shipping_address.getFirstname() + " " + shipping_address.getLastname(),
                    product.getArticleId(),
                    product.Title(),
                    "%s"   % item.getProductQuantity(),
                    "%.2f" % item.getProductPriceGross(),
                    "%.2f" % item.getProductPriceNet(),
                    "%.2f" % item.getProductTax(),
                    "%.2f" % item.getTax(),
                    "%.2f" % item.getTaxRate(),
                    "%.2f" % item.getPriceGross(),
                    "%.2f" % item.getPriceNet(),
                )
                
                # row = ['"%s"' % field for field in row]
                row = ";".join(row)
                
                result.append(row)

        self.request.response.setHeader('Content-type', 'text/plain')
        self.request.response.setHeader(
            'Content-disposition',
            'attachment; filename=%s' % "orders.csv"
        )

        return "\n".join(result)