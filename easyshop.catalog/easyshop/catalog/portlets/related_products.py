# zope imports
from zope import schema
from zope.formlib import form
from zope.interface import implements

# plone imports
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

# Five imports
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# CMFPlone imports
from Products.CMFPlone import PloneMessageFactory as _

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import IImageManagement
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IProduct

class IRelatedProductsPortlet(IPortletDataProvider):

    count = schema.Int(title=_(u'Number of products to display'),
                       description=_(u'How many products to list. 0 for all.'),
                       required=True,
                       default=5)

class Assignment(base.Assignment):
    """
    """
    implements(IRelatedProductsPortlet)

    def __init__(self, count=5):
        """
        """
        self.count = count

    @property
    def title(self):
        """
        """
        return _(u"EasyShop: Related Products")

class Renderer(base.Renderer):

    render = ViewPageTemplateFile('related_products.pt')

    @property
    def available(self):
        """
        """
        if IProduct.providedBy(self.context) and (len(self._data()) > 0):
            return True
        else:
            return False

    def related_products(self):
        """
        """
        return self._data()

    @memoize
    def _data(self):
        """
        """
        limit = self.data.count
        if limit != 0:
            products = self.context.getRefs("products_products")[:limit]
        else:
            products = self.context.getRefs("products_products")
            
        result = []
        for product in products:
            
            mtool = getToolByName(self.context, "portal_membership")
            if mtool.checkPermission("View", product) == True:
                
                # Image
                image = IImageManagement(product).getMainImage()
                image_url = image.absolute_url() + "/image_thumb"
            
                # Price
                price = IPrices(product).getPriceGross()
                cm = ICurrencyManagement(product)
                price = cm.priceToString(price)
                        
                result.append({
                    "title"     : product.Title(),
                    "url"       : product.absolute_url(),
                    "image_url" : image_url,
                    "price"     : price,
                })
            
        return result
        
class AddForm(base.AddForm):
    """
    """
    form_fields = form.Fields(IRelatedProductsPortlet)
    label = _(u"Add Related Products Portlet")
    description = _(u"This portlet displays related products.")

    def create(self, data):
        return Assignment(count=data.get('count', 5),)

class EditForm(base.EditForm):
    """
    """
    form_fields = form.Fields(IRelatedProductsPortlet)
    label = _(u"Edit Related Products Portlet")
    description = _(u"This portlet displays related products.")